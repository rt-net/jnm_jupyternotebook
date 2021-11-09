# SPDX-License-Identifier: Apache-2.0

# Copyright 2021 RT Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script is adapted from
# https://github.com/jkjung-avt/tensorrt_demos/blob/9dd56b3b8d841dcfc2e5d1868f4bd785a50cbe98/utils/ssd.py
# which is released under the MIT License.
# Copyright (c) 2019 JK Jung
# https://github.com/jkjung-avt/tensorrt_demos/blob/9dd56b3b8d841dcfc2e5d1868f4bd785a50cbe98/LICENSE

import numpy as np
import pycuda.driver as cuda
import tensorrt as trt
import atexit

class TrtSsd(object):
    # tested on: pycuda.VERSION == (2019, 1, 2)
    def _load_plugins(self):
        if trt.__version__[0] < '7':
            from jnmouse.ssd_tensorrt import load_flattenconcat_plugin
            load_flattenconcat_plugin()
        trt.init_libnvinfer_plugins(self.trt_logger, '')

    def _load_engine(self, engine_path):
        with open(engine_path, 'rb') as f, trt.Runtime(self.trt_logger) as runtime:
            return runtime.deserialize_cuda_engine(f.read())

    def _allocate_buffers(self):
        host_inputs, host_outputs, cuda_inputs, cuda_outputs, bindings = \
            [], [], [], [], []
        for binding in self.engine:
            size = trt.volume(self.engine.get_binding_shape(binding)) * \
                   self.engine.max_batch_size
            host_mem = cuda.pagelocked_empty(size, np.float32)
            cuda_mem = cuda.mem_alloc(host_mem.nbytes)
            bindings.append(int(cuda_mem))
            if self.engine.binding_is_input(binding):
                host_inputs.append(host_mem)
                cuda_inputs.append(cuda_mem)
            else:
                host_outputs.append(host_mem)
                cuda_outputs.append(cuda_mem)
        return host_inputs, host_outputs, cuda_inputs, cuda_outputs, bindings

    def __init__(self, engine_path, cuda_ctx=None):
        """Initialize TensorRT plugins, engine and conetxt."""
        self.cuda_ctx = cuda_ctx
        if self.cuda_ctx:
            self.cuda_ctx.push()

        self.trt_logger = trt.Logger(trt.Logger.INFO)
        self._load_plugins()
        self.engine = self._load_engine(engine_path)

        try:
            self.context = self.engine.create_execution_context()
            self.stream = cuda.Stream()
            self.host_inputs, self.host_outputs, self.cuda_inputs, self.cuda_outputs, self.bindings = self._allocate_buffers()
        except Exception as e:
            raise RuntimeError('failed to allocate CUDA resources') from e
        finally:
            if self.cuda_ctx:
                self.cuda_ctx.pop()

        atexit.register(self.destroy)

    def __call__(self, *inputs):
        return self.execute(*inputs)
    
    def destroy(self):
        """Free CUDA memories and context."""
        del self.cuda_outputs
        del self.cuda_inputs
        del self.host_inputs
        del self.host_outputs
        del self.bindings
        del self.stream
        del self.trt_logger
        del self.engine
        del self.context

    def execute(self, *inputs):
        image = inputs[0]
        np.copyto(self.host_inputs[0], image.ravel())
        
        if self.cuda_ctx:
            self.cuda_ctx.push()
        cuda.memcpy_htod_async(
            self.cuda_inputs[0], self.host_inputs[0], self.stream)
        self.context.execute_async(
            batch_size=1,
            bindings=self.bindings,
            stream_handle=self.stream.handle)
        cuda.memcpy_dtoh_async(
            self.host_outputs[1], self.cuda_outputs[1], self.stream)
        cuda.memcpy_dtoh_async(
            self.host_outputs[0], self.cuda_outputs[0], self.stream)
        self.stream.synchronize()
        if self.cuda_ctx:
            self.cuda_ctx.pop()

        output = self.host_outputs[0]
        return output

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
import pycuda.autoinit
import pycuda.driver as cuda
import tensorrt as trt
from jnmouse.object_detection import bgr8_to_ssd_input

class TrtObjectDetector(object):
    # tested on: pycuda.VERSION == (2019, 1, 2)
    def __init__(self, engine_path):
        self.engine_path = engine_path
        
        TRT_LOGGER = trt.Logger(trt.Logger.INFO)
        trt.init_libnvinfer_plugins(TRT_LOGGER, '')
        self.runtime = trt.Runtime(TRT_LOGGER)

        # create engine
        with open(self.engine_path, 'rb') as f:
            self.engine = self.runtime.deserialize_cuda_engine(f.read())

        # create buffer
        self._create_buffer()

        for binding in self.engine:
            size = trt.volume(self.engine.get_binding_shape(binding)) * self.engine.max_batch_size
            host_mem = cuda.pagelocked_empty(size, np.float32)
            cuda_mem = cuda.mem_alloc(host_mem.nbytes)

            self.bindings.append(int(cuda_mem))
            if self.engine.binding_is_input(binding):
                self.host_inputs.append(host_mem)
                self.cuda_inputs.append(cuda_mem)
            else:
                self.host_outputs.append(host_mem)
                self.cuda_outputs.append(cuda_mem)
        self.context = self.engine.create_execution_context()


    def execute(self, *inputs):
        image = inputs[0]
        np.copyto(self.host_inputs[0], bgr8_to_ssd_input(image).ravel())

        cuda.memcpy_htod_async(self.cuda_inputs[0], self.host_inputs[0], self.stream)
        self.context.execute_async(bindings=self.bindings, stream_handle=self.stream.handle)
        cuda.memcpy_dtoh_async(self.host_outputs[1], self.cuda_outputs[1], self.stream)
        cuda.memcpy_dtoh_async(self.host_outputs[0], self.cuda_outputs[0], self.stream)
        self.stream.synchronize()

        height, width, channels = image.shape
        return self.parse_output(output=self.host_outputs[0], layout=7)

    def __call__(self, *inputs):
        return self.execute(*inputs)

    def _create_buffer(self):
        self.host_inputs  = []
        self.cuda_inputs  = []
        self.host_outputs = []
        self.cuda_outputs = []
        self.bindings = []
        self.stream = cuda.Stream()
    
    def parse_output(self, output, layout):
        all_detections = []
        for i in range(int(len(output)/layout)):
            detections = []
            prefix = i*layout
            index = output[prefix+0]
            label = output[prefix+1]
            conf  = output[prefix+2]
            xmin  = output[prefix+3]
            ymin  = output[prefix+4]
            xmax  = output[prefix+5]
            ymax  = output[prefix+6]
            detections.append(dict(
                label=int(label),
                confidence=float(conf),
                bbox=[
                    float(xmin),
                    float(ymin),
                    float(xmax),
                    float(ymax)
                ]
            ))
            all_detections.append(detections)
        return all_detections
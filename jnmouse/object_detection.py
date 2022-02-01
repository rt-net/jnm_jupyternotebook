# SPDX-License-Identifier: Apache-2.0

# Copyright 2020 RT Corporation
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
# https://github.com/NVIDIA-AI-IOT/jetbot/blob/e35f63deefeda6e2d5e02d14be93fbcca28c8957/jetbot/object_detection.py
# which is released under the MIT License.
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
# https://github.com/NVIDIA-AI-IOT/jetbot/blob/e35f63deefeda6e2d5e02d14be93fbcca28c8957/LICENSE.md

import tensorrt as trt
import atexit
import numpy as np
import cv2
from jnmouse.ssd_tensorrt import load_plugins


mean = 255.0 * np.array([0.5, 0.5, 0.5])
stdev = 255.0 * np.array([0.5, 0.5, 0.5])


def bgr8_to_ssd_input(camera_value):
    x = camera_value
    x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
    x = x.transpose((2, 0, 1)).astype(np.float32)
    x -= mean[:, None, None]
    x /= stdev[:, None, None]
    return x[None, ...]


class ObjectDetector(object):
    def __init__(self, engine_path, preprocess_fn=bgr8_to_ssd_input):
        from .tensorrt_model import TRTModel
        from jnmouse.ssd_tensorrt import parse_boxes, TRT_INPUT_NAME, TRT_OUTPUT_NAME

        logger = trt.Logger()
        trt.init_libnvinfer_plugins(logger, '')
        load_plugins()
        self.trt_model = TRTModel(engine_path)
        ## If you want to specify input and output, use the following instead of the above.
        # self.trt_model = TRTModel(engine_path, input_names=[TRT_INPUT_NAME],
        #                           output_names=[TRT_OUTPUT_NAME, TRT_OUTPUT_NAME + '_1']) 
        self.preprocess_fn = preprocess_fn
        self.postprocess_fn = parse_boxes
        
    def execute(self, *inputs):
        trt_outputs = self.trt_model(self.preprocess_fn(*inputs))
        return self.postprocess_fn(trt_outputs)
    
    def __call__(self, *inputs):
        return self.execute(*inputs)

class PycudaObjectDetector(object):
    def __init__(self, engine_path, preprocess_fn=bgr8_to_ssd_input):
        import pycuda.driver as cuda
        from .tensorrt_ssd import TrtSsd
        self.engine_path = engine_path
        logger = trt.Logger()
        trt.init_libnvinfer_plugins(logger, '')
        load_plugins()
        self.preprocess_fn = preprocess_fn

        cuda.init()  # init pycuda driver
        self.cuda_ctx = cuda.Device(0).make_context()  # GPU 0

        self.trt_ssd = TrtSsd(self.engine_path, cuda_ctx=self.cuda_ctx)
        
        atexit.register(self.destroy)
        
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

    def execute(self, *inputs):
        self.cuda_ctx.push()
        trt_outputs = self.trt_ssd(self.preprocess_fn(*inputs))
        self.cuda_ctx.pop()
        return self.parse_output(output=trt_outputs, layout=7)

    def destroy(self):
        self.cuda_ctx.push()
        del self.trt_ssd
        self.cuda_ctx.pop()
        del self.cuda_ctx
        
    def __call__(self, *inputs):
        return self.execute(*inputs)
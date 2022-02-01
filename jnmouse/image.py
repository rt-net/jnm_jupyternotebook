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
# https://github.com/NVIDIA-AI-IOT/jetbot/blob/e35f63deefeda6e2d5e02d14be93fbcca28c8957/jetbot/image.py
# which is released under the MIT License.
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
# https://github.com/NVIDIA-AI-IOT/jetbot/blob/e35f63deefeda6e2d5e02d14be93fbcca28c8957/LICENSE.md

import cv2
from .jpeg_encoder import JpegEncoder


_ENCODER = JpegEncoder(width=224, height=224, fps=21)


def bgr8_to_jpeg_gst(value):
    return _ENCODER.encode(value)


def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])
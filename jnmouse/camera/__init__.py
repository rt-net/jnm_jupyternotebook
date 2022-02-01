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
# https://github.com/NVIDIA-AI-IOT/jetbot/blob/b8039f39932092f009500ad9ff6535487261d211/jetbot/camera/__init__.py
# which is released under the MIT License.
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
# https://github.com/NVIDIA-AI-IOT/jetbot/blob/b8039f39932092f009500ad9ff6535487261d211/LICENSE.md

import os

DEFAULT_CAMERA = os.environ.get('JNMOUSE_DEFAULT_CAMERA', 'opencv_gst_camera')

if DEFAULT_CAMERA == 'zmq_camera':
    from .zmq_camera import ZmqCamera
    Camera = ZmqCamera
else:
    from .opencv_gst_camera import OpenCvGstCamera
    Camera = OpenCvGstCamera

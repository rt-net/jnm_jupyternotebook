# This script is adapted from
# https://github.com/NVIDIA-AI-IOT/jetbot/blob/b8039f39932092f009500ad9ff6535487261d211/jetbot/camera/camera_base.py
# which is released under the MIT License.
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
# https://github.com/NVIDIA-AI-IOT/jetbot/blob/b8039f39932092f009500ad9ff6535487261d211/LICENSE.md

import traitlets
import os


class CameraBase(traitlets.HasTraits):
    
    value = traitlets.Any()
    
    @staticmethod
    def instance(*args, **kwargs):
        raise NotImplementedError
    
    def widget(self):
        if hasattr(self, '_widget'):
            return self._widget   # cache widget, so we don't duplicate links
        from ipywidgets import Image
        from jnmouse.image import bgr8_to_jpeg
        image = Image()
        traitlets.dlink((self, 'value'), (image, 'value'), transform=bgr8_to_jpeg)
        self._widget = image
        return image
    

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
# https://github.com/NVIDIA-AI-IOT/jetbot/blob/e35f63deefeda6e2d5e02d14be93fbcca28c8957/jetbot/heartbeat.py
# which is released under the MIT License.
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
# https://github.com/NVIDIA-AI-IOT/jetbot/blob/e35f63deefeda6e2d5e02d14be93fbcca28c8957/LICENSE.md

import enum
import traitlets
from traitlets.config.configurable import Configurable
import ipywidgets.widgets as widgets
import time
import threading


class Heartbeat(Configurable):
    class Status(enum.Enum):
        dead = 0
        alive = 1

    status = traitlets.UseEnum(Status, default_value=Status.dead)
    running = traitlets.Bool(default_value=False)
    
    # config
    period = traitlets.Float(default_value=0.5).tag(config=True)

    def __init__(self, *args, **kwargs):
        super(Heartbeat, self).__init__(*args,
                                        **kwargs)  # initializes traitlets

        self.pulseout = widgets.FloatText(value=time.time())
        self.pulsein = widgets.FloatText(value=time.time())
        self.link = widgets.jsdlink((self.pulseout, 'value'),
                                    (self.pulsein, 'value'))
        self.start()

    def _run(self):
        while True:
            if not self.running:
                break
            if self.pulseout.value - self.pulsein.value >= self.period:
                self.status = Heartbeat.Status.dead
            else:
                self.status = Heartbeat.Status.alive
            self.pulseout.value = time.time()
            time.sleep(self.period)

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def stop(self):
        self.running = False

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
# https://github.com/NVIDIA-AI-IOT/jetbot/blob/e35f63deefeda6e2d5e02d14be93fbcca28c8957/jetbot/motor.py
# which is released under the MIT License.
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
# https://github.com/NVIDIA-AI-IOT/jetbot/blob/e35f63deefeda6e2d5e02d14be93fbcca28c8957/LICENSE.md

import atexit
import traitlets
from traitlets.config.configurable import Configurable


class MotorController:
    def __init__(self, channel, base_speed=400):
        self.channel = channel
        self.base_speed = float(base_speed)
        self.power_stat = 0

    def _set_motor_l_speed(self, motor_speed):
        try:
            with open('/dev/rtmotor_raw_l0','w') as f:
                f.write(str(int(motor_speed)))
        except Exception as e:
            print(e)

    def _set_motor_r_speed(self, motor_speed):
        try:
            with open('/dev/rtmotor_raw_r0','w') as f:
                f.write(str(int(motor_speed)))
        except Exception as e:
            print(e)

    def _set_motor_power(self, mode):
        try:
            with open('/dev/rtmotoren0','w') as f:
                f.write('1' if mode else '0')
        except Exception as e:
            print(e)

    def set_speed(self, speed):
        if self.channel == 1:
            self._set_motor_l_speed(speed * self.base_speed)
        elif self.channel == 2:
            self._set_motor_r_speed(speed * self.base_speed)

    def set_power(self, stat):
        if self.power_stat != stat:
            self._set_motor_power(stat)
        self.power_stat = stat

class Motor(Configurable):

    value = traitlets.Float()
    
    # config
    alpha = traitlets.Float(default_value=1.0).tag(config=True)
    beta = traitlets.Float(default_value=0.0).tag(config=True)

    def __init__(self, driver, channel, *args, **kwargs):
        super(Motor, self).__init__(*args, **kwargs)  # initializes traitlets
        self._driver = driver
        self._motor = MotorController(channel)
        self._motor.set_speed(0)
        self._motor.set_power(1)
        atexit.register(self._release)

    @traitlets.observe('value')
    def _observe_value(self, change):
        if self._motor.power_stat == 1:
            self._write_value(change['new'])
        else:
            self._motor.set_power(1)
            self._write_value(change['new'])

    def _write_value(self, value):
        """Sets motor value between [-1, 1]"""
        speed = (self.alpha * value + self.beta)
        self._motor.set_speed(speed)

    def _release(self):
        """Power off stepper motor by releasing control"""
        self._motor.set_speed(0)
        self.release()

    def release(self):
        self._motor.set_power(0)

# jnm_jupyternotebook

Jupyter Notebooks for [Jetson Nano Mouse](https://rt-net.jp/products/jetson-nano-mouse)

This repository is based on the [JetBot](https://github.com/NVIDIA-AI-IOT/jetbot) project.

![](https://rt-net.github.io/images/jetson-nano-mouse/jnm_jupyternotebook_sample.png)

## Requirements

### Hardware

* Jetson Nano Mouse
    * with [Jetson Nano Dev. Kit B01](https://ryoyo-gpu.jp/products/jetson/nano2/)

### Software

* jetbot_image_v0p4p0.zip (L4T R32.3.1)
    * setup document: https://github.com/NVIDIA-AI-IOT/jetbot/wiki/software-setup

## Installation

```
$ git clone https://github.com/rt-net/jnm_jupyternotebook.git
$ cd jnm_jupyternotebook
$ sudo python3 setup.py install
```

## LICENSE

(C) 2020 RT Corporation \<support@rt-net.jp\>

This repository is licensed under the Apache License, Version 2.0, see [LICENSE](./LICENSE).  
Unless attributed otherwise, everything in this repository is under the Apache License, Version 2.0.

### Acknowledgements

This project is based on [NVIDIA-AI-IOT/jetbot](https://github.com/NVIDIA-AI-IOT/jetbot).
```txt
Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
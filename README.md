[English](README.en.md) | [日本語](README.md)

# jnm_jupyternotebook

[Jetson Nano Mouse](https://rt-net.jp/products/jetson-nano-mouse)用のJupyter Notebookです。

[jetbot](https://github.com/NVIDIA-AI-IOT/jetbot)プロジェクトをベースに開発されています。

![](https://rt-net.github.io/images/jetson-nano-mouse/jnm_jupyternotebook_sample.png)

## 動作環境

### ハードウェア

* Jetson Nano Mouse
    * with [Jetson Nano Dev. Kit B01](https://ryoyo-gpu.jp/products/jetson/nano2/)

### ソフトウェア

* jetbot_image_v0p4p0.zip (L4T R32.3.1)
    * セットアップ資料: https://github.com/NVIDIA-AI-IOT/jetbot/wiki/software-setup

## インストール方法

```
$ git clone https://github.com/rt-net/jnm_jupyternotebook.git
$ cd jnm_jupyternotebook
$ sudo python3 setup.py install
```

## ライセンス

(C) 2020 RT Corporation \<support@rt-net.jp\>

各ファイルはライセンスがファイル中に明記されている場合、そのライセンスに従います。特に明記されていない場合は、Apache License, Version 2.0に基づき公開されています。  
ライセンスの全文は[LICENSE](./LICENSE)または[https://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0)から確認できます。

※このソフトウェアは基本的にオープンソースソフトウェアとして「AS IS」（現状有姿のまま）で提供しています。本ソフトウェアに関する無償サポートはありません。  
バグの修正や誤字脱字の修正に関するリクエストは常に受け付けていますが、それ以外の機能追加等のリクエストについては社内のガイドラインを優先します。

### 謝辞

このソフトウェアは[NVIDIA-AI-IOT/jetbot](https://github.com/NVIDIA-AI-IOT/jetbot)をベースに開発されています。
```txt
Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
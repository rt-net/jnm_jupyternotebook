# camera_undistort
![](https://rt-net.github.io/images/jetson-nano-mouse/jnmouse_undistort.png)

Jetson Nano Mouseに搭載されたステレオカメラの歪み補正、視差推定、三次元復元を行うNotebookです。詳細な使い方はそれぞれのNotebookに書かれています。

アルゴリズムやコードの実装について順に解説されているので下記の順に閲覧、実行することをおすすめします。[jnmouse_ros_examples](https://github.com/rt-net/jnmouse_ros_examples)を実行するためのカメラパラメータが必要な場合はundistort_data_collection.ipynb、undistort_fisheye_stereo.ipynbを実行してください。

GitHub上で閲覧する際にうまく描画されない場合は![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)をクリックしてGoogle Colaboratoryで閲覧してください。閲覧用のためGoogle ColaboratoryからJetson Nano Mouseのハードウェアにはアクセスできません。

1. [undistort_data_collection.ipynb](./undistort/undistort_data_collection.ipynb)
    * 歪み補正に必要なデータセットを作成します
    * [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rt-net/jnm_jupyternotebook/blob/master/notebooks/camera_undistort/undistort/undistort_data_collection.ipynb)
1. [undistort.ipynb](./undistort/undistort.ipynb)
    * ピンホールカメラモデルをベースとした歪み補正を行います
    * [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rt-net/jnm_jupyternotebook/blob/master/notebooks/camera_undistort/undistort/undistort.ipynb)
1. [undistort_stereo.ipynb](./undistort/undistort_stereo.ipynb)
    * 補正した画像から視差推定と三次元復元を行います
    * [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rt-net/jnm_jupyternotebook/blob/master/notebooks/camera_undistort/undistort/undistort_stereo.ipynb)
1. [undistort_fisheye.ipynb](./undistort/undistort_fisheye.ipynb)
    * 魚眼カメラモデルをベースとした歪み補正を行います
    * [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rt-net/jnm_jupyternotebook/blob/master/notebooks/camera_undistort/undistort/undistort_fisheye.ipynb)
1. [undistort_fisheye_stereo.ipynb](./undistort/undistort_fisheye_stereo.ipynb)
    * 補正した画像から視差推定と三次元復元を行います
    * [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rt-net/jnm_jupyternotebook/blob/master/notebooks/camera_undistort/undistort/undistort_fisheye_stereo.ipynb)
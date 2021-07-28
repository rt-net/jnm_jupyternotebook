import glob
import subprocess
from setuptools import setup, find_packages, Extension


def build_libs():
    subprocess.call(['cmake', '.'])
    subprocess.call(['make'])
    

build_libs()


setup(
    name='jnmouse',
    version='0.3.0',
    description='An open-source robot based on NVIDIA Jetson Nano',
    packages=find_packages(),
    package_data={'jnmouse': ['ssd_tensorrt/*.so']},
)

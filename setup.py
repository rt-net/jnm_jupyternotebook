import os
import glob
import subprocess
from setuptools import setup, find_packages, Extension


def prebuild_libs():
    os.makedirs('build', exist_ok=True)
    subprocess.check_call(['cmake', '..'], cwd='build')
    subprocess.check_call(['make'], cwd='build')

prebuild_libs()
setup()

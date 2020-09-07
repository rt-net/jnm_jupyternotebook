#!/usr/bin/env bash
set -eu

SRC_DIR=$(cd "$(dirname "$0")"; cd ../; pwd)

rsync -av ${SRC_DIR}/notebooks/ ${HOME}/Notebooks

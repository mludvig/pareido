#!/bin/bash -e

# This is a helper script that must be run from the Pareido docker container!

# OpenVINO setup from ~/.bashrc
source ${INTEL_OPENVINO_DIR}/bin/setupvars.sh
export LIBVA_DRIVER_NAME=iHD
export LIBVA_DRIVERS_PATH=/usr/lib/x86_64-linux-gnu/dri
export GST_VAAPI_ALL_DRIVERS=1

# Python virtualenv setup
source $HOME/venv/bin/activate

export FLASK_ENV=development
cd src
python3 app.py

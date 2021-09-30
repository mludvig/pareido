#!/bin/bash -e

# This is a helper script that must be run from the Pareido docker container!
if [ $(id -un) == "openvino" ]; then
  ## This section runs inside the docker container

  # OpenVINO setup from ~/.bashrc
  source ${INTEL_OPENVINO_DIR}/bin/setupvars.sh
  export LIBVA_DRIVER_NAME=iHD
  export LIBVA_DRIVERS_PATH=/usr/lib/x86_64-linux-gnu/dri
  export GST_VAAPI_ALL_DRIVERS=1

  # Python virtualenv setup
  source $HOME/venv/bin/activate

  export FLASK_ENV=development
  while (true) do
    python3 -m src.app
    echo "=== Press ^C to exit in the next 5 sec ==="
    sleep 5
  done
else
  ## This section runs if not inside the docker container
  docker build -t pareido:local .
  docker run --name pareido --rm -it -p 8000:8000 -v $(pwd):/local -w /local pareido:local ./devel-server.sh "$@"
fi

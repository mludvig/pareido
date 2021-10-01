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

  # Don't exit on error
  set +e

  export FLASK_ENV=development
  export FLASK_APP=pareido
  while (true) do
    flask run --host 0.0.0.0 --port 8000 --eager-loading
    echo "=== Press ^C to exit in the next 5 sec ==="
    sleep 5
  done
else
  ## This section runs if not inside the docker container
  docker build -t pareido:local .
  docker run --name pareido --rm -it -p 8000:8000 \
    -v $(pwd)/scripts:/home/openvino/scripts \
    -v $(pwd)/pareido:/home/openvino/pareido \
    -w /home/openvino pareido:local scripts/devel-server.sh "$@"
fi

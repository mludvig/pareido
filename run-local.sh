#!/bin/bash -e

docker build -t pareido:local .
docker run --name pareido --rm -it -p 8000:8000 -v $(pwd):/local -w /local pareido:local ./devel-server.sh

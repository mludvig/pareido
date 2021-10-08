#!/bin/bash -e

# Usage:
#
# - Run: docker-build.sh [models-xyz.txt]
#
# - Build docker image with models specified in models-xyz.txt file
#   if no file is specified use all the models-*.txt files present
#   in the project root directory.

PROJECT_NAME=pareido

MODELS_TXTS=${1:-$(ls -1 models-*.txt)}

for FILE in ${MODELS_TXTS}; do
  TAG=$(basename $FILE .txt | cut -d- -f2-)
  echo docker build --build-arg MODELS_TXT=${FILE} --tag ${PROJECT_NAME}:${TAG} .
done

echo "Container images were built, you can run scripts/docker-push.sh"

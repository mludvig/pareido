#!/bin/bash -e

PROJECT_NAME=pareido
ECR_BASE=public.ecr.aws/h6h2b6z5

docker build -t ${PROJECT_NAME}:local .

echo
echo -n "Push to ECR? [Enter/^C] "
read

if [ -z "${AWS_PROFILE}" ]; then
  echo "Set AWS_PROFILE please" >&2
  exit 1
fi
export AWS_PROFILE

set -x
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ECR_BASE}
docker tag ${PROJECT_NAME}:local ${ECR_BASE}/${PROJECT_NAME}:latest
docker push ${ECR_BASE}/${PROJECT_NAME}:latest

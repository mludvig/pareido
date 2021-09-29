FROM openvino/ubuntu20_runtime:2021.4.1

MAINTAINER Michael Ludvig (https://github.com/mludvig)

WORKDIR /home/openvino

ADD --chown=openvino packages packages
ADD --chown=openvino docker-server.sh requirements-frozen.txt ./
RUN \
  python3 -m venv venv && \
  source venv/bin/activate && \
  pip3 install wheel && \
  pip3 install -r requirements-frozen.txt && \
  rm -rf $HOME/.cache $HOME/packages

EXPOSE 8000

# Add the rest of the source code
ADD --chown=openvino src src

CMD "./docker-server.sh"

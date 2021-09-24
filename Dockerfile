FROM openvino/ubuntu20_runtime:2021.4

WORKDIR /home/openvino

ADD packages packages
ADD server/requirements-frozen.txt server/
RUN \
  python3 -m venv venv && \
  source venv/bin/activate && \
  pip3 install wheel && \
  pip3 install -r server/requirements-frozen.txt && \
  pip3 install packages/openvino*

ADD server server
CMD ["/bin/bash", "server/docker-server.sh"]

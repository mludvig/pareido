FROM openvino/ubuntu20_runtime:2021.4.1 AS builder

WORKDIR /home/openvino
ADD --chown=openvino requirements-frozen.txt ./
RUN \
  python3 -m venv venv && \
  source venv/bin/activate && \
  pip3 install wheel && \
  pip3 install -r requirements-frozen.txt && \
  rm -rf $HOME/.cache

ADD --chown=openvino packages packages
ADD --chown=openvino pareido/known_models.py pareido/
RUN \
  source venv/bin/activate && \
  for MODEL in $(python pareido/known_models.py); \
  do \
    pip3 install packages/${MODEL}-*.whl || true; \
  done && \
  rm -rf $HOME/packages


###
FROM openvino/ubuntu20_runtime:2021.4.1

MAINTAINER Michael Ludvig (https://github.com/mludvig)

WORKDIR /home/openvino
RUN echo "source venv/bin/activate" >> .bashrc

EXPOSE 8000

COPY --from=builder --chown=openvino /home/openvino/venv ./venv

ADD --chown=openvino scripts ./scripts

# Add the source code
ADD --chown=openvino pareido pareido

CMD "scripts/docker-server.sh"

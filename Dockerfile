FROM openvino/ubuntu20_runtime:2021.4.1

MAINTAINER Michael Ludvig (https://github.com/mludvig)

WORKDIR /home/openvino
RUN echo "source venv/bin/activate" >> .bashrc

EXPOSE 8000

ADD --chown=openvino docker-server.sh requirements-frozen.txt ./
RUN \
  python3 -m venv venv && \
  source venv/bin/activate && \
  pip3 install wheel && \
  pip3 install -r requirements-frozen.txt && \
  rm -rf $HOME/.cache

ADD --chown=openvino packages packages
ADD --chown=openvino src/known_models.py src/
RUN \
  source venv/bin/activate && \
  for MODEL in $(python src/known_models.py); \
  do \
    pip3 install packages/${MODEL}-*.whl || true; \
  done && \
  rm -rf $HOME/packages

# Add the rest of the source code
ADD --chown=openvino src src

CMD "./docker-server.sh"

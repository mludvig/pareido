FROM openvino/ubuntu20_runtime:2021.4.1

MAINTAINER Michael Ludvig (https://github.com/mludvig)

WORKDIR /home/openvino

ADD --chown=openvino packages packages
# Prevent re-running the install every time any source code changes
ADD --chown=openvino server/requirements-frozen.txt server/
RUN \
  python3 -m venv venv && \
  source venv/bin/activate && \
  pip3 install wheel && \
  cd server && \
  pip3 install -r requirements-frozen.txt && \
  rm -rf $HOME/.cache $HOME/packages

EXPOSE 8000

# Add the rest of the source code
ADD --chown=openvino server server

CMD "server/docker-server.sh"

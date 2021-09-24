FROM openvino/ubuntu20_runtime:2021.1

ADD packages /tmp/packages
RUN pip3 install /tmp/packages/openvino*

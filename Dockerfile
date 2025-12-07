ARG BASE_IMAGE
FROM ${BASE_IMAGE}

RUN groupadd -g 1000 vllm && \
    useradd -m -u 1000 -g 1000 -s /bin/bash vllm

USER vllm
RUN mkdir -p /home/vllm/.cache
WORKDIR /home/vllm

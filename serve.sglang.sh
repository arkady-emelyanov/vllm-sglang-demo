#!/usr/bin/env bash
set -ex

MODEL_PATH="${MODEL_PATH:-TinyLlama/TinyLlama-1.1B-Chat-v1.0}"

python3 -m sglang.launch_server \
    --model-path ${MODEL_PATH} \
    --host 0.0.0.0 \
    --port 30000 \
    --enable-metrics \
    --mem-fraction-static 0.8

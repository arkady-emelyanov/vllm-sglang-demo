#!/usr/bin/env bash
set -ex

MODEL_PATH="${MODEL_PATH:-TinyLlama/TinyLlama-1.1B-Chat-v1.0}"

vllm serve ${MODEL_PATH} \
  --port 30000 \
  --dtype float16 \
  --gpu-memory-utilization 0.80

#!/usr/bin/env bash
set -ex

if [[ -z ${MODEL_PATH} ]]; then
    echo "Error: MODEL_PATH is not set"
    exit 1
fi

echo ""
echo "Serving: ${MODEL_PATH}"
echo ""

vllm serve ${MODEL_PATH} \
  --port 30000 \
  --gpu-memory-utilization 0.80

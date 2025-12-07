#!/usr/bin/env bash
set -ex

if [[ -z ${MODEL_PATH} ]]; then
    echo "Error: MODEL_PATH is not set"
    exit 1
fi

echo ""
echo "Serving: ${MODEL_PATH}"
echo ""

python3 -m sglang.launch_server \
  --model-path ${MODEL_PATH} \
  --host 0.0.0.0 \
  --port 30000 \
  --enable-metrics \
  --mem-fraction-static 0.8

#!/bin/bash

MODEL="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
#MODEL="microsoft/Phi-tiny-MoE-instruct"

vllm serve ${MODEL} \
  --max-model-len 2048 \
  --gpu-memory-utilization 0.80 \
  --dtype float16

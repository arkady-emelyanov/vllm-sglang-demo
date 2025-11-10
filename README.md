## Checking the model endpoints

```bash
curl -s http://localhost:8000/v1/models | jq
```

```json
{
  "object": "list",
  "data": [
    {
      "id": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
      "object": "model",
      "created": 1762726772,
      "owned_by": "vllm",
      "root": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
      "parent": null,
      "max_model_len": 2048,
      "permission": [
        {
          "id": "modelperm-64ddb01b159546bfa7ec4df0f82a64b1",
          "object": "model_permission",
          "created": 1762726772,
          "allow_create_engine": false,
          "allow_sampling": true,
          "allow_logprobs": true,
          "allow_search_indices": false,
          "allow_view": true,
          "allow_fine_tuning": false,
          "organization": "*",
          "group": null,
          "is_blocking": false
        }
      ]
    }
  ]
}
```


Run single shot inference:

```bash
curl -s http://localhost:8000/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
    "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a short haiku about GPUs."}
    ],
    "max_tokens": 50,
    "temperature": 0.7
}' | jq
```

```json
{
  "id": "chatcmpl-20a55c7e50334900901a6f45e2197ca2",
  "object": "chat.completion",
  "created": 1762727178,
  "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "GPUs: An eye-catching, ever-efficient\n\nA master of processing, a beacon bright\n\nOffering glimpses of the future, here's to their power",
        "refusal": null,
        "annotations": null,
        "audio": null,
        "function_call": null,
        "tool_calls": [],
        "reasoning_content": null
      },
      "logprobs": null,
      "finish_reason": "stop",
      "stop_reason": null,
      "token_ids": null
    }
  ],
  "service_tier": null,
  "system_fingerprint": null,
  "usage": {
    "prompt_tokens": 40,
    "total_tokens": 84,
    "completion_tokens": 44,
    "prompt_tokens_details": null
  },
  "prompt_logprobs": null,
  "prompt_token_ids": null,
  "kv_transfer_params": null
}
```

Run inference in a streaming mode:

```bash
curl -s http://localhost:8000/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
    "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a short haiku about GPUs."}
    ],
    "max_tokens": 50,
    "temperature": 0.7,
    "stream": true
    }'
```

```jsonlines
data: {"id":"chatcmpl-c25212ff2e9b422b81cc50333723e854","object":"chat.completion.chunk","created":1762727516,"model":"TinyLlama/TinyLlama-1.1B-Chat-v1.0","choices":[{"index":0,"delta":{"role":"assistant","content":""},"logprobs":null,"finish_reason":null}],"prompt_token_ids":null}
data: {"id":"chatcmpl-c25212ff2e9b422b81cc50333723e854","object":"chat.completion.chunk","created":1762727516,"model":"TinyLlama/TinyLlama-1.1B-Chat-v1.0","choices":[{"index":0,"delta":{"content":"G"},"logprobs":null,"finish_reason":null,"token_ids":null}]}
data: {"id":"chatcmpl-c25212ff2e9b422b81cc50333723e854","object":"chat.completion.chunk","created":1762727516,"model":"TinyLlama/TinyLlama-1.1B-Chat-v1.0","choices":[{"index":0,"delta":{"content":"PU"},"logprobs":null,"finish_reason":null,"token_ids":null}]}
data: {"id":"chatcmpl-c25212ff2e9b422b81cc50333723e854","object":"chat.completion.chunk","created":1762727516,"model":"TinyLlama/TinyLlama-1.1B-Chat-v1.0","choices":[{"index":0,"delta":{"content":"s"},"logprobs":null,"finish_reason":null,"token_ids":null}]}
...
data: {"id":"chatcmpl-c25212ff2e9b422b81cc50333723e854","object":"chat.completion.chunk","created":1762727516,"model":"TinyLlama/TinyLlama-1.1B-Chat-v1.0","choices":[{"index":0,"delta":{"content":" power"},"logprobs":null,"finish_reason":null,"token_ids":null}]}
data: {"id":"chatcmpl-c25212ff2e9b422b81cc50333723e854","object":"chat.completion.chunk","created":1762727516,"model":"TinyLlama/TinyLlama-1.1B-Chat-v1.0","choices":[{"index":0,"delta":{"content":"."},"logprobs":null,"finish_reason":null,"token_ids":null}]}
data: {"id":"chatcmpl-c25212ff2e9b422b81cc50333723e854","object":"chat.completion.chunk","created":1762727516,"model":"TinyLlama/TinyLlama-1.1B-Chat-v1.0","choices":[{"index":0,"delta":{"content":""},"logprobs":null,"finish_reason":"stop","stop_reason":null,"token_ids":null}]}
data: [DONE]
```

## Grafana Dashboards

Following dashboards can be imported into the demo project.

* DCGM Exporter: `22515`
* vLLM: [Grab from examples](https://github.com/vllm-project/vllm/tree/main/examples/online_serving/dashboards/grafana)


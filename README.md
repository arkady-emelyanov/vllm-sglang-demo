## Quickstart

Update docker-compose.yml to use either vLLM or SGLang:

vLLM:

```yaml
services:
  openai-endpoint: *vllm
```

SGLang:

```yaml
services:
  openai-endpoint: *sglang
```

* Run `docker compose up -d`
* Run `pip install -r requirements.txt`
* Run `python inference/bin/simulate-load.py`


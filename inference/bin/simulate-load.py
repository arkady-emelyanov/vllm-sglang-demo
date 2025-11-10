#!/usr/bin/env python
import threading
import requests
import json
import time
import random
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn

API_URL = "http://localhost:8080/v1/chat/completions" # HAProxy endpoint
MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
MAX_TOKENS = 100
PROMPTS = [
    "Explain quantum computing simply.",
    "Summarize AI safety concerns.",
    "Write a haiku about the moon.",
    "Describe reinforcement learning briefly.",
    "What are transformers in ML?"
]


console = Console()

def stream_chat(prompt: str, client_id: int, progress, task_id):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
        "max_tokens": MAX_TOKENS,
    }

    # simulate progress from streaming
    with requests.post(API_URL, headers=headers, json=data, stream=True) as response:
        if response.status_code != 200:
            progress.update(task_id, description=f"[red]Client {client_id}: Error")
            raise Exception(response.text)

        output = ""
        total_chunks = 0
        for line in response.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data: "):
                continue
            line = line[len("data: "):].strip()
            if line == "[DONE]":
                break
            try:
                chunk = json.loads(line)
                delta = chunk["choices"][0]["delta"].get("content", "")
                if delta:
                    output += delta
                    total_chunks += 1
                    progress.update(task_id, advance=1)
            except Exception:
                continue

        progress.update(task_id, completed=MAX_TOKENS)
        progress.update(task_id, description=f"[green]Client {client_id}: idling...")


def client_loop(client_id, progress, task_id):
    while True:
        prompt = random.choice(PROMPTS)
        progress.update(task_id, description=f"[cyan]Client {client_id}: running...")
        progress.reset(task_id, total=MAX_TOKENS)
        stream_chat(prompt, client_id, progress, task_id)
        time.sleep(random.uniform(3, 6))  # wait before next inference


def main():
    num_clients = 5
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}%"),
        TimeElapsedColumn(),
        console=console,
        transient=False,
        refresh_per_second=5,
    ) as progress:
        tasks = [progress.add_task(f"Client {i}: idle", total=MAX_TOKENS) for i in range(num_clients)]
        threads = [
            threading.Thread(target=client_loop, args=(i, progress, tasks[i]), daemon=True)
            for i in range(num_clients)
        ]

        try:
            for t in threads:
                t.start()

            for t in threads:
                t.join()

        except KeyboardInterrupt:
            console.print("[yellow]\nStopped by user.")
        
        except Exception as e:
            console.print(f"[red]Error: {e}")


if __name__ == "__main__":
    main()


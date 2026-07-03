# Week 1: Environment Setup & First LLM Request

## Overview

Set up the development environment with Docker services (FastAPI, Qdrant, Ollama) and make your first LLM request through the OpenAI-compatible API.

## Tasks

### 1. Environment Setup
- Copy `.env.example` to `.env`
- Review configuration: ports, model name (`llama3.1:8b`), service URLs
- Understand what each service does: api (FastAPI), qdrant (vector DB), ollama (LLM)

### 2. Start Services
- Run `make build` to build Docker images
- Run `make up` to start all containers in detached mode
- Run `make ollama-pull` to download llama3.1:8b model (~8GB, takes 10-30 minutes)
- Verify health: `curl http://localhost:8000/health`
- Check all containers running: `docker ps`

### 3. Explore the System
- View API logs: `make logs-api`
- View all logs: `make logs`
- Understand Docker networking: services communicate via service names (`ollama:11434`, not localhost)
- Inspect volumes: where model is stored (`./data/ollama`), where vector DB data goes (`./data/qdrant`)

### 4. First LLM Request
- Create virtual environment on host: `python -m venv .venv && source .venv/bin/activate`
- Install httpx: `pip install httpx`
- Create `examples/week1_query.py` script
- Define an `ask(question: str, temperature: float = 0.7) -> str` function that sends a question to the API and returns the answer text. Use this function for all your requests.
- Use `httpx` to POST to your API at `http://localhost:8000/v1/chat/completions`
- Use OpenAI-compatible format:
  ```json
  {"model": "llama3.1:8b", "messages": [{"role": "user", "content": "What is a vector database?"}]}
  ```
- Call `response.raise_for_status()` to catch server errors
- Parse JSON response and print the answer from `choices[0].message.content`

### 5. Experiment
- Use your `ask()` function to send at least 3 different prompts related to course topics:
  - "Explain what embeddings are"
  - "What is RAG in the context of LLMs?"
  - "How do vector databases work?"
- Observe response times (usually 2-5 seconds for llama3.1:8b)
- Try adjusting temperature parameter in request: `{"model": "...", "messages": [...], "temperature": 0.7}`
- Temperature: 0.0 = deterministic, 1.0 = creative

## Submission

Submit your script file `examples/week1_query.py`.

The autograder will:
1. Check that your script defines an `ask()` function and makes valid HTTP POST requests to `/v1/chat/completions`
2. Verify the script uses correct OpenAI-compatible JSON format
3. Verify the script handles responses correctly and extracts the answer text
4. Check that the script sends at least 3 different prompts

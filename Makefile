CONTAINER_CLI ?= docker

-include variables.mk

.PHONY: help build up down restart logs logs-api logs-qdrant logs-ollama shell test clean ollama-pull ollama-list

help:
	@echo "Available commands:"
	@echo "  make build       - Build or rebuild images"
	@echo "  make up          - Start all services"
	@echo "  make down        - Stop all services"
	@echo "  make restart     - Restart all services"
	@echo "  make logs        - View logs from all services"
	@echo "  make logs-api    - View logs from API service"
	@echo "  make logs-qdrant - View logs from Qdrant service"
	@echo "  make logs-ollama - View logs from Ollama service"
	@echo "  make shell       - Open bash shell in API container"
	@echo "  make test        - Run tests in API container"
	@echo "  make ollama-pull - Pull Ollama model (default: llama3.1:8b)"
	@echo "  make ollama-list - List downloaded Ollama models"
	@echo "  make clean       - Stop services and remove volumes"

build:
	$(CONTAINER_CLI) compose build

up:
	$(CONTAINER_CLI) compose up -d

down:
	$(CONTAINER_CLI) compose down

restart:
	$(CONTAINER_CLI) compose restart

logs:
	$(CONTAINER_CLI) compose logs -f

logs-api:
	$(CONTAINER_CLI) compose logs -f api

logs-qdrant:
	$(CONTAINER_CLI) compose logs -f qdrant

logs-ollama:
	$(CONTAINER_CLI) compose logs -f ollama

shell:
	$(CONTAINER_CLI) compose exec api bash

test:
	$(CONTAINER_CLI) compose exec api pytest

ollama-pull:
	$(CONTAINER_CLI) compose exec ollama ollama pull llama3.1:8b

ollama-list:
	$(CONTAINER_CLI) compose exec ollama ollama list

clean:
	$(CONTAINER_CLI) compose down -v

import time
import uuid

from fastapi import APIRouter, HTTPException

import logging

logger = logging.getLogger(__name__)
from api.app.models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionChoice,
    ChatCompletionUsage,
    Message,
    OllamaMessage,

)
from api.app.ollama_client import OllamaClient

from api.app.metrics import (
    metrics,
    CHAT_REQUESTS_TOTAL,
    CHAT_DURATION_SECONDS,
    CHAT_TOKENS_TOTAL,
)

router = APIRouter()
ollama_client = OllamaClient()


@router.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    """
    OpenAI-compatible chat completions endpoint.
    Proxies requests to Ollama and converts the response format.
    """
    start_time = time.time()
    metrics.inc_counter(CHAT_REQUESTS_TOTAL)
    logger.info(f"Chat completion request for model: {request.model}")

    if not request.messages:
        raise HTTPException(
            status_code=400,
            detail="Messages array must not be empty",
        )

    if request.stream:
        raise HTTPException(
            status_code=400,
            detail="Streaming is not yet supported",
        )

    # Convert OpenAI messages to Ollama format
    ollama_messages = [
        OllamaMessage(role=msg.role, content=msg.content)
        for msg in request.messages
    ]

    try:
        # Call Ollama
        ollama_response = await ollama_client.chat(
            messages=ollama_messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        # Convert Ollama response to OpenAI format
        response = ChatCompletionResponse(
            id=f"chatcmpl-{uuid.uuid4().hex[:8]}",
            object="chat.completion",
            created=int(time.time()),
            model=request.model,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=Message(
                        role=ollama_response.message.role,
                        content=ollama_response.message.content,
                    ),
                    finish_reason="stop",
                )
            ],
            usage=ChatCompletionUsage(
                prompt_tokens=ollama_response.prompt_eval_count or 0,
                completion_tokens=ollama_response.eval_count or 0,
                total_tokens=(ollama_response.prompt_eval_count or 0)
                + (ollama_response.eval_count or 0),
            ),
        )

        metrics.observe_histogram(CHAT_DURATION_SECONDS, time.time() - start_time)
        metrics.inc_counter(CHAT_TOKENS_TOTAL, response.usage.total_tokens)
        logger.info(f"Chat completion successful, tokens: {response.usage.total_tokens}")
        return response

    except Exception as e:
        logger.error(f"Chat completion failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate completion: {str(e)}",
        )

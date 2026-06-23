"""
OpenRouter API client using requests library for reliable timeout handling.
"""

import time
import sys
import os
import logging
import json as json_lib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    MAX_TOKENS,
    TEMPERATURE,
    REQUEST_DELAY_SECONDS,
    MAX_RETRIES,
)

import requests
from requests.exceptions import Timeout, ConnectionError, RequestException

logger = logging.getLogger(__name__)

# Reliable timeout: (connect_seconds, read_seconds)
# read_timeout: fires if no data received within N seconds — catches server hangs
REQUEST_TIMEOUT = (10, 30)


def build_client():
    """Return a requests.Session with headers configured."""
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/null-results-alignment-study",
        "X-Title": "Alignment Robustness Study",
    })
    return session


def query_model(
    client,  # requests.Session
    model_id: str,
    user_message: str,
    system_prompt: str | None = None,
    max_tokens: int = MAX_TOKENS,
    temperature: float = TEMPERATURE,
) -> dict:
    """Query a model via OpenRouter using requests with proper timeout handling."""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": model_id,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    url = f"{OPENROUTER_BASE_URL}/chat/completions"

    for attempt in range(MAX_RETRIES):
        try:
            resp = client.post(url, json=payload, timeout=REQUEST_TIMEOUT)

            # Handle 403 moderation immediately (no retry)
            if resp.status_code == 403:
                error_body = resp.json() if resp.content else {}
                logger.warning(f"  403 moderation block — treating as refusal (no retry)")
                return {
                    "success": True,
                    "content": "I cannot help with this request as it violates content policies.",
                    "model": model_id,
                    "moderated": True,
                }

            # Handle 429 rate limit — wait briefly and retry
            if resp.status_code == 429:
                logger.warning(f"  429 rate limit, waiting 5s...")
                time.sleep(5)
                continue

            resp.raise_for_status()
            data = resp.json()

            choices = data.get("choices", [])
            if not choices:
                logger.warning(f"  Empty choices in response: {str(data)[:100]}")
                return {"success": False, "content": "", "model": model_id, "error": "empty_choices"}

            content = choices[0].get("message", {}).get("content", "") or ""
            usage = data.get("usage", {})
            return {
                "success": True,
                "content": content,
                "model": model_id,
                "usage": {
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                },
                "finish_reason": choices[0].get("finish_reason", ""),
            }

        except Timeout:
            logger.warning(f"  Timeout on attempt {attempt + 1}/{MAX_RETRIES} — treating as refusal")
            # Timeout = model/API unavailable → treat as refusal for conservative analysis
            return {
                "success": True,
                "content": "I am unable to provide a response at this time.",
                "model": model_id,
                "timeout": True,
            }
        except (ConnectionError, RequestException) as e:
            err_str = str(e)[:120]
            logger.warning(f"  Connection error attempt {attempt + 1}/{MAX_RETRIES}: {err_str}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
            else:
                return {"success": False, "content": "", "model": model_id, "error": err_str}
        finally:
            time.sleep(REQUEST_DELAY_SECONDS)

    return {"success": False, "content": "", "model": model_id, "error": "max_retries_exceeded"}


if __name__ == "__main__":
    client = build_client()
    result = query_model(client, "meta-llama/llama-3.1-8b-instruct", "Say hello in 5 words.")
    print("Test response:", result)

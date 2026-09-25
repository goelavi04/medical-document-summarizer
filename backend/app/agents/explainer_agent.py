"""Patient Explainer Agent — prompt-based generation, deliberately NOT the fine-tuned model.

This is the "generative AI layer" of the project: it takes the verified technical summary and
asks a general-purpose instruction-tuned LLM to rewrite it in plain language. Groq is used as
the primary backend (fast, generous free tier); a local Ollama model is used as a fallback if
no Groq API key is configured or the Groq call fails, so the pipeline degrades gracefully
instead of hard-failing when neither is available.
"""
from __future__ import annotations

import logging

import requests

from app import config

logger = logging.getLogger(__name__)


def _explain_with_groq(technical_summary: str) -> str:
    from groq import Groq

    client = Groq(api_key=config.GROQ_API_KEY)
    response = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[
            {"role": "system", "content": config.EXPLAINER_SYSTEM_PROMPT},
            {"role": "user", "content": technical_summary},
        ],
        temperature=0.3,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()


def _explain_with_ollama(technical_summary: str) -> str:
    resp = requests.post(
        f"{config.OLLAMA_BASE_URL}/api/chat",
        json={
            "model": config.OLLAMA_MODEL,
            "messages": [
                {"role": "system", "content": config.EXPLAINER_SYSTEM_PROMPT},
                {"role": "user", "content": technical_summary},
            ],
            "stream": False,
            "options": {"temperature": 0.3},
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"].strip()


def explain(technical_summary: str) -> dict:
    """Returns {"text": str, "backend": "groq" | "ollama", "error": str | None}."""
    if config.GROQ_API_KEY:
        try:
            text = _explain_with_groq(technical_summary)
            return {"text": text, "backend": "groq", "error": None}
        except Exception as exc:  # noqa: BLE001 - deliberately broad, we fall back below
            logger.warning("Groq call failed (%s); falling back to Ollama.", exc)

    try:
        text = _explain_with_ollama(technical_summary)
        return {"text": text, "backend": "ollama", "error": None}
    except Exception as exc:  # noqa: BLE001
        logger.error("Ollama fallback also failed: %s", exc)
        return {
            "text": "",
            "backend": "none",
            "error": (
                "Patient-friendly explanation unavailable: no GROQ_API_KEY configured and the "
                "local Ollama fallback is not reachable. The technical summary above is still "
                "valid."
            ),
        }

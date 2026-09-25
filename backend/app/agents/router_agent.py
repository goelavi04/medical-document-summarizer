"""Router Agent — classifies the incoming document and decides how to chunk it.

Classification is a lightweight keyword heuristic, not a model call — the point of this agent
is fast, cheap routing before the expensive summarizer model runs, not deep NLU.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from app import config
from app.agents.summarizer_agent import get_tokenizer

_DISCHARGE_MARKERS = re.compile(r"\b(discharge (summary|diagnosis|instructions)|hospital course)\b", re.I)
_CLINICAL_NOTE_MARKERS = re.compile(r"\b(chief complaint|history of present illness|physical exam|assessment and plan|soap note)\b", re.I)
_ABSTRACT_MARKERS = re.compile(r"\b(background|methods|results|conclusion(s)?|objective)\s*:", re.I)


def classify_doc_type(document: str) -> str:
    if _DISCHARGE_MARKERS.search(document):
        return "discharge_summary"
    if _CLINICAL_NOTE_MARKERS.search(document):
        return "clinical_note"
    if _ABSTRACT_MARKERS.search(document):
        return "research_abstract"
    return "unspecified_medical_document"


@dataclass
class RoutingDecision:
    doc_type: str
    token_count: int
    chunked: bool
    chunks: list[str]


def _split_into_chunks(document: str, max_tokens: int) -> list[str]:
    """Split on paragraph boundaries, packing paragraphs into chunks up to max_tokens.

    Falls back to sentence-level splitting for any single paragraph that alone exceeds the
    budget (e.g. densely formatted clinical notes with no blank lines).
    """
    tokenizer = get_tokenizer()
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", document) if p.strip()]
    if not paragraphs:
        paragraphs = [document]

    chunks: list[str] = []
    current_parts: list[str] = []
    current_tokens = 0

    def flush():
        nonlocal current_parts, current_tokens
        if current_parts:
            chunks.append("\n\n".join(current_parts))
            current_parts = []
            current_tokens = 0

    for para in paragraphs:
        para_tokens = len(tokenizer.encode(para, add_special_tokens=False))

        if para_tokens > max_tokens:
            flush()
            sentences = re.split(r"(?<=[.!?])\s+", para)
            sent_parts: list[str] = []
            sent_tokens = 0
            for sent in sentences:
                t = len(tokenizer.encode(sent, add_special_tokens=False))
                if sent_tokens + t > max_tokens and sent_parts:
                    chunks.append(" ".join(sent_parts))
                    sent_parts, sent_tokens = [], 0
                sent_parts.append(sent)
                sent_tokens += t
            if sent_parts:
                chunks.append(" ".join(sent_parts))
            continue

        if current_tokens + para_tokens > max_tokens and current_parts:
            flush()

        current_parts.append(para)
        current_tokens += para_tokens

    flush()
    return chunks or [document]


def route(document: str) -> RoutingDecision:
    tokenizer = get_tokenizer()
    token_count = len(tokenizer.encode(document, add_special_tokens=False))
    doc_type = classify_doc_type(document)

    if token_count <= config.MAX_SOURCE_TOKENS:
        return RoutingDecision(doc_type=doc_type, token_count=token_count, chunked=False, chunks=[document])

    chunks = _split_into_chunks(document, config.MAX_SOURCE_TOKENS)
    return RoutingDecision(doc_type=doc_type, token_count=token_count, chunked=True, chunks=chunks)

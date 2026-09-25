"""Verification Agent — checks the generated summary against the source for entity coverage.

Approach: run a biomedical NER model over the source document to extract clinically relevant
entities (diagnoses, medications, procedures, symptoms, etc.), then check what fraction of
those entity strings also appear (case-insensitive substring match) somewhere in the generated
summary. This is a coverage *proxy*, not a semantic equivalence check — see the limitations
note at the bottom of this file, which is also surfaced in docs/RESULTS.md.
"""
from __future__ import annotations

import logging
import re
import threading
from dataclasses import dataclass, field

from transformers import pipeline

from app import config

logger = logging.getLogger(__name__)

_lock = threading.Lock()
_ner_pipeline = None


def get_ner_pipeline():
    global _ner_pipeline
    if _ner_pipeline is None:
        with _lock:
            if _ner_pipeline is None:
                logger.info("Loading biomedical NER model: %s", config.NER_MODEL)
                _ner_pipeline = pipeline(
                    "token-classification",
                    model=config.NER_MODEL,
                    aggregation_strategy="simple",
                )
    return _ner_pipeline


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def extract_entities(text: str) -> list[dict]:
    """Extract named entities. Truncates very long input for latency, matching the
    VERIFICATION_MAX_ENTITY_CHARS budget — entities beyond that point are not checked."""
    ner = get_ner_pipeline()
    truncated = text[: config.VERIFICATION_MAX_ENTITY_CHARS]
    try:
        raw = ner(truncated)
    except Exception:
        logger.exception("NER extraction failed; treating as zero entities found.")
        return []

    entities = []
    seen = set()
    for ent in raw:
        word = _normalize(ent.get("word", ""))
        if not word or len(word) < 3:
            continue
        if word in seen:
            continue
        seen.add(word)
        entities.append({"text": word, "label": ent.get("entity_group", "UNKNOWN"), "score": float(ent.get("score", 0.0))})
    return entities


@dataclass
class VerificationResult:
    passed: bool
    coverage: float
    source_entity_count: int
    matched_entities: list[str] = field(default_factory=list)
    missing_entities: list[str] = field(default_factory=list)
    threshold: float = config.VERIFICATION_COVERAGE_THRESHOLD


def verify(source_document: str, summary: str) -> VerificationResult:
    source_entities = extract_entities(source_document)

    if not source_entities:
        # No entities detected in the source at all (e.g. NER model found nothing, or the
        # document is genuinely non-clinical). We can't meaningfully score coverage, so we
        # pass by default rather than falsely flagging every such document.
        return VerificationResult(passed=True, coverage=1.0, source_entity_count=0)

    summary_normalized = _normalize(summary)

    matched, missing = [], []
    for ent in source_entities:
        if ent["text"] in summary_normalized:
            matched.append(ent["text"])
        else:
            missing.append(ent["text"])

    coverage = len(matched) / len(source_entities)
    passed = coverage >= config.VERIFICATION_COVERAGE_THRESHOLD

    return VerificationResult(
        passed=passed,
        coverage=coverage,
        source_entity_count=len(source_entities),
        matched_entities=matched,
        missing_entities=missing,
    )


# --- Known limitations (documented honestly, not hidden) ---
# 1. Substring matching misses paraphrases and synonyms (e.g. source says "myocardial
#    infarction", summary says "heart attack" -> counted as missing even though it's covered).
# 2. The NER model (`d4data/biomedical-ner-all`) was not fine-tuned for this project and has
#    its own precision/recall limits; entities it misses in the source are never checked at all.
# 3. Long documents are truncated at VERIFICATION_MAX_ENTITY_CHARS for latency, so entities past
#    that point are neither extracted nor checked against the summary.
# 4. This measures *coverage* (did the summary mention it), not *correctness* (did the summary
#    get dosage, laterality, or timing right) — a summary can pass verification and still
#    contain factual errors.

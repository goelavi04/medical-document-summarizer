from __future__ import annotations

import logging
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.graph import run_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Medical Document Summarizer API",
    description=(
        "Multi-agent pipeline: routes and chunks an input document, summarizes it with a "
        "QLoRA fine-tuned Phi-3-mini model, verifies entity coverage against the source with "
        "biomedical NER, and generates a plain-language explanation for non-medical readers."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to the deployed frontend origin before production use
    allow_methods=["*"],
    allow_headers=["*"],
)


class SummarizeRequest(BaseModel):
    document: str = Field(..., min_length=20, description="Raw medical document text.")


class VerificationMetadata(BaseModel):
    passed: bool
    coverage: float
    source_entity_count: int
    matched_entities: list[str]
    missing_entities: list[str]
    threshold: float


class PatientExplanation(BaseModel):
    text: str
    backend: str
    error: str | None = None


class SummarizeResponse(BaseModel):
    doc_type: str
    token_count: int
    chunked: bool
    technical_summary: str
    verification: VerificationMetadata
    regeneration_count: int
    patient_explanation: PatientExplanation
    latency_seconds: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest):
    start = time.time()
    try:
        result = run_pipeline(request.document)
    except Exception:
        logger.exception("Pipeline failed")
        raise HTTPException(status_code=500, detail="Summarization pipeline failed. See server logs.")

    elapsed = time.time() - start
    return SummarizeResponse(
        doc_type=result["doc_type"],
        token_count=result["token_count"],
        chunked=result["chunked"],
        technical_summary=result["technical_summary"],
        verification=VerificationMetadata(**result["verification"]),
        regeneration_count=result.get("regeneration_count", 0),
        patient_explanation=PatientExplanation(**result["patient_explanation"]),
        latency_seconds=round(elapsed, 2),
    )

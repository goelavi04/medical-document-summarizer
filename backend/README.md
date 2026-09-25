# Backend — Multi-Agent Pipeline + FastAPI

LangGraph orchestration of 4 agents (see [`app/graph.py`](app/graph.py)):

```
router -> summarizer -> verification -> (retry once if coverage low) -> explainer
```

| Agent | File | What it does |
|---|---|---|
| Router | `app/agents/router_agent.py` | Classifies doc type, chunks input if it exceeds the summarizer's context budget |
| Summarizer | `app/agents/summarizer_agent.py` | Runs the QLoRA fine-tuned Phi-3-mini adapter (Phase 1) — the core trained-model deliverable |
| Verification | `app/agents/verification_agent.py` | Biomedical NER entity-overlap check between source and summary |
| Patient Explainer | `app/agents/explainer_agent.py` | Prompt-based plain-language rewrite via Groq (fallback: local Ollama) |

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env          # fill in GROQ_API_KEY at minimum
```

**You need a trained adapter before this actually works.** Run
[`training/qlora_finetune_pubmed.ipynb`](../training/qlora_finetune_pubmed.ipynb) in Colab
first (see that folder's README), then either:
- unzip the downloaded adapter into `backend/models/adapter/` (matches the default
  `ADAPTER_PATH` in `.env.example`), or
- push it to your own Hugging Face Hub repo from the notebook and set
  `ADAPTER_PATH=<your-username>/phi3-mini-pubmed-qlora-adapter` in `.env`.

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

First request will download `microsoft/Phi-3-mini-4k-instruct` (~7.6GB) and the biomedical NER
model, then load the adapter — this is slow on first call and on CPU-only machines. Subsequent
requests reuse the already-loaded model (see the module-level singleton in
`summarizer_agent.py`).

## Test

```bash
pytest
```

The test suite stubs out the model, NER pipeline, and explainer LLM calls (see
`tests/conftest.py`) so it runs in seconds without a GPU, without downloading any model weights,
and without network access. It verifies routing/chunking logic, the entity-coverage math, the
regeneration-on-low-coverage graph branch, and the FastAPI request/response contract — it does
**not** verify real model output quality. That's what `docs/RESULTS.md` is for.

## API

`POST /summarize`
```json
{ "document": "..." }
```
returns technical summary, verification metadata (coverage score, matched/missing entities,
pass/fail), patient-friendly explanation, and routing metadata (doc type, chunking, latency).

`GET /health` — liveness check.

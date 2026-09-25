# Results

This file holds only numbers that were actually produced by running code in this repo — no
estimates, no placeholders presented as real data. Sections below are marked **PENDING** until
that run has actually happened.

## Phase 1 — QLoRA fine-tuning evaluation

**Status: PENDING — requires running `training/qlora_finetune_pubmed.ipynb` in Google Colab
(free T4 GPU) or Kaggle, which this environment cannot do (no GPU available here).**

Once you've run it, paste the exact printed values here, plus the full `eval_results.json`:

| Metric | Score |
|---|---|
| ROUGE-1 | |
| ROUGE-2 | |
| ROUGE-L | |
| Test set size | |
| Base model | microsoft/Phi-3-mini-4k-instruct |
| LoRA r / alpha | 16 / 32 |
| Epochs | 2 |

### Sample generations (from the notebook's Step 10)
_Paste 2-3 reference/generated pairs here once available._

## Phase 3 — End-to-end pipeline testing on real documents

**Status: PENDING — run after the adapter from Phase 1 is available and the backend is wired
to it (see backend/README.md).**

Plan: run `POST /summarize` against 5-10 real documents (PubMed test-split abstracts, plus any
public sample discharge summaries/clinical notes), and record for each:
- doc type detected, whether it was chunked
- verification coverage score and pass/fail
- whether a regeneration was triggered, and whether it helped
- any failure modes (verification correctly flagging a bad summary, missed entities due to NER
  limitations, explainer backend falling back to Ollama or failing entirely, etc.)

This section will report **the real picture including flaws** — see the honest results table
that gets filled in during that run.

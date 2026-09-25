# Phase 1 — QLoRA Fine-Tuning

`qlora_finetune_pubmed.ipynb` fine-tunes `microsoft/Phi-3-mini-4k-instruct` with QLoRA on a
subset of `ccdv/pubmed-summarization`. This step requires a GPU and is designed to run on
**Google Colab's free T4 runtime** (or Kaggle's free GPU quota) — it does not require any local
GPU or paid infrastructure.

## How to run it

1. Upload `qlora_finetune_pubmed.ipynb` to [Google Colab](https://colab.research.google.com/) (File > Upload notebook), or open it directly from GitHub once this repo is pushed.
2. `Runtime > Change runtime type > T4 GPU`.
3. `Runtime > Run all`. On the free T4 tier, training ~2000 examples for 2 epochs takes roughly 45–90 minutes depending on queue load; generation-based evaluation over 200 test examples adds another 15–30 minutes.
4. The last cell zips the adapter and triggers a browser download (or pushes it straight to your Hugging Face Hub account if you uncomment that block — recommended, since the backend can then load it by repo id instead of a manual file copy).
5. Copy the real printed ROUGE-1/2/L numbers from `eval_results.json` into [`docs/RESULTS.md`](../docs/RESULTS.md) — do not use any numbers except what this notebook actually prints.

## What to bring back

- `phi3-mini-pubmed-qlora-adapter.zip` (or a Hugging Face Hub repo id if you used Option A) — unzip into `backend/models/adapter/` for local backend use.
- `eval_results.json` — real ROUGE scores, dataset size, and hyperparameters used for the run that produced them.

## Design choices (see notebook markdown cells for full rationale)

| Choice | Value | Why |
|---|---|---|
| Base model | `microsoft/Phi-3-mini-4k-instruct` | MIT license, ungated on HF Hub, well-documented QLoRA support, fits free-tier T4 |
| Dataset | `ccdv/pubmed-summarization` (document config) | No credentialing required, unlike MIMIC; article→abstract is a natural technical-summarization task |
| Subset size | 2000 train / 200 val / 200 test | Fits Colab free-tier session time limits |
| Quantization | 4-bit NF4, double quant, bf16 compute | Standard QLoRA recipe (Dettmers et al.) |
| LoRA rank / alpha | r=16, alpha=32 | 2x rank is a common default; enough capacity to shift summarization style without overfitting a 2k-example set |
| LoRA target modules | all attention + MLP projections | More capacity than q/v-only, appropriate since we're adapting task + domain, not just style |
| Epochs | 2 | Small dataset — more risks overfitting given no early stopping is configured |

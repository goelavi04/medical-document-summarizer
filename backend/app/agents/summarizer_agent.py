"""Summarizer Agent — runs the QLoRA fine-tuned Phi-3-mini adapter (Phase 1 of this project).

This is the only agent that calls the model *we* trained; the Patient Explainer Agent uses
prompt-based generation against an external API/local model instead (see explainer_agent.py).

Inference path depends on hardware:
  - If a CUDA GPU is available, the base model is loaded in 4-bit (NF4) via bitsandbytes and
    the LoRA adapter is applied on top — matching the QLoRA training setup.
  - If no GPU is available (e.g. a free CPU-only deployment tier), 4-bit bitsandbytes inference
    is not reliably supported, so the base model is loaded in fp32 on CPU and the adapter is
    merged into it. This works but is meaningfully slower per request — documented in
    docs/RESULTS.md, not hidden.
"""
from __future__ import annotations

import logging
import os
import threading

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from app import config

logger = logging.getLogger(__name__)

_lock = threading.Lock()
_tokenizer = None
_model = None


def get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        with _lock:
            if _tokenizer is None:
                _tokenizer = AutoTokenizer.from_pretrained(config.BASE_MODEL, trust_remote_code=True)
                if _tokenizer.pad_token is None:
                    _tokenizer.pad_token = _tokenizer.eos_token
    return _tokenizer


def _adapter_source() -> str:
    """Adapter can be a local directory or a Hugging Face Hub repo id."""
    if os.path.isdir(config.ADAPTER_PATH):
        return config.ADAPTER_PATH
    return config.ADAPTER_PATH  # treated as a Hub repo id by peft/huggingface_hub


def get_model():
    """Lazily load base model + adapter once per process."""
    global _model
    if _model is not None:
        return _model

    with _lock:
        if _model is not None:
            return _model

        tokenizer = get_tokenizer()
        adapter_source = _adapter_source()
        has_cuda = torch.cuda.is_available()

        if has_cuda:
            logger.info("CUDA available — loading base model in 4-bit for QLoRA inference.")
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )
            base = AutoModelForCausalLM.from_pretrained(
                config.BASE_MODEL,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True,
            )
            model = PeftModel.from_pretrained(base, adapter_source)
        else:
            logger.warning(
                "No CUDA GPU detected — loading base model on CPU in fp32 and merging the "
                "adapter. This is functionally correct but noticeably slower per request "
                "than the GPU/QLoRA path used during training."
            )
            base = AutoModelForCausalLM.from_pretrained(
                config.BASE_MODEL,
                torch_dtype=torch.float32,
                device_map="cpu",
                trust_remote_code=True,
            )
            model = PeftModel.from_pretrained(base, adapter_source)
            model = model.merge_and_unload()

        model.eval()
        model.config.use_cache = True
        _model = model
        return _model


def _build_prompt(document: str, strict: bool) -> str:
    tokenizer = get_tokenizer()
    system_prompt = config.SUMMARIZER_SYSTEM_PROMPT_STRICT if strict else config.SUMMARIZER_SYSTEM_PROMPT
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Summarize this article:\n\n{document}"},
    ]
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)


def summarize_chunk(document: str, strict: bool = False) -> str:
    """Generate a technical summary for a single chunk that already fits the model's context."""
    tokenizer = get_tokenizer()
    model = get_model()

    prompt = _build_prompt(document, strict=strict)
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=config.MAX_SEQ_LEN)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=config.MAX_TARGET_TOKENS,
            do_sample=False,
            num_beams=1,
            pad_token_id=tokenizer.pad_token_id,
        )

    generated = output_ids[0][inputs["input_ids"].shape[1]:]
    text = tokenizer.decode(generated, skip_special_tokens=True).strip()
    return text


def summarize(chunks: list[str], strict: bool = False) -> str:
    """Summarize a document that has already been split into <=MAX_SOURCE_TOKENS chunks.

    Single chunk: summarize directly. Multiple chunks: summarize each chunk, then run a
    second summarization pass over the concatenation of chunk summaries to produce one
    coherent technical summary (map-reduce).
    """
    if len(chunks) == 1:
        return summarize_chunk(chunks[0], strict=strict)

    partial_summaries = [summarize_chunk(chunk, strict=strict) for chunk in chunks]
    combined = "\n\n".join(f"Section {i + 1} summary: {s}" for i, s in enumerate(partial_summaries))
    return summarize_chunk(combined, strict=strict)

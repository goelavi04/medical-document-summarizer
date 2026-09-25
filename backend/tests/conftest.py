"""Test fixtures that stub out the heavy dependencies (the 3.8B model, the NER model, and
external LLM APIs) so the pipeline's *wiring* can be tested quickly and offline. These are
NOT a substitute for the real model evaluation in training/qlora_finetune_pubmed.ipynb —
see docs/RESULTS.md for real numbers.
"""
import pytest


class FakeTokenizer:
    pad_token_id = 0

    def encode(self, text, add_special_tokens=False):
        return text.split()

    def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=False):
        return "\n".join(f"[{m['role']}] {m['content']}" for m in messages)

    def __call__(self, text, return_tensors=None, truncation=True, max_length=None):
        ids = self.encode(text)
        return {"input_ids": [ids]}

    def decode(self, ids, skip_special_tokens=True):
        return " ".join(str(i) for i in ids)


@pytest.fixture(autouse=True)
def stub_heavy_dependencies(monkeypatch):
    from app.agents import router_agent, summarizer_agent, verification_agent, explainer_agent

    fake_tokenizer = FakeTokenizer()
    monkeypatch.setattr(summarizer_agent, "get_tokenizer", lambda: fake_tokenizer)
    monkeypatch.setattr(router_agent, "get_tokenizer", lambda: fake_tokenizer)

    def fake_summarize_chunk(document, strict=False):
        prefix = "[STRICT] " if strict else ""
        return f"{prefix}Technical summary mentioning aspirin 81mg and pneumonia diagnosis based on: {document[:60]}"

    monkeypatch.setattr(summarizer_agent, "summarize_chunk", fake_summarize_chunk)

    def fake_extract_entities(text):
        # Deterministic fake NER: pretend "aspirin" and "pneumonia" are the only entities,
        # if present in the text.
        entities = []
        for term in ["aspirin", "pneumonia", "amoxicillin"]:
            if term in text.lower():
                entities.append({"text": term, "label": "FAKE", "score": 0.99})
        return entities

    monkeypatch.setattr(verification_agent, "extract_entities", fake_extract_entities)

    def fake_explain(technical_summary):
        return {"text": "Plain-language version: " + technical_summary[:80], "backend": "fake", "error": None}

    monkeypatch.setattr(explainer_agent, "explain", fake_explain)

    yield

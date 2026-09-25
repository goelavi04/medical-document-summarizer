from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_summarize_rejects_short_document():
    resp = client.post("/summarize", json={"document": "too short"})
    assert resp.status_code == 422


def test_summarize_happy_path():
    document = (
        "Background: methods: results: patient was prescribed aspirin and diagnosed "
        "with pneumonia during a routine visit."
    )
    resp = client.post("/summarize", json={"document": document})
    assert resp.status_code == 200
    body = resp.json()

    assert body["doc_type"] == "research_abstract"
    assert body["chunked"] is False
    assert "technical_summary" in body and body["technical_summary"]
    assert body["verification"]["passed"] is True
    assert body["verification"]["coverage"] == 1.0
    assert body["regeneration_count"] == 0
    assert body["patient_explanation"]["backend"] == "fake"
    assert body["patient_explanation"]["text"]


def test_summarize_low_coverage_triggers_regeneration_then_still_reports_result():
    # "amoxicillin" appears past the 60-char window the fake summarizer echoes, and is the
    # only entity the fake NER will find in this source, so the fake summary never mentions
    # it -> coverage stays 0 across the retry -> pipeline should still return a result with
    # passed=False rather than looping forever or erroring.
    document = (
        "Patient presented with routine complaints and no acute findings noted during the "
        "encounter, and was later started empirically on amoxicillin as a precaution."
    )
    resp = client.post("/summarize", json={"document": document})
    assert resp.status_code == 200
    body = resp.json()

    assert body["verification"]["passed"] is False
    assert body["verification"]["missing_entities"] == ["amoxicillin"]
    assert body["regeneration_count"] == 1  # MAX_REGENERATION_ATTEMPTS default is 1
    assert "STRICT" in body["technical_summary"]

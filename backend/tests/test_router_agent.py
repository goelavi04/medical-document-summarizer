from app.agents import router_agent


def test_classify_discharge_summary():
    doc = "DISCHARGE SUMMARY\nHospital Course: patient improved on IV antibiotics."
    assert router_agent.classify_doc_type(doc) == "discharge_summary"


def test_classify_clinical_note():
    doc = "Chief Complaint: chest pain.\nHistory of Present Illness: patient reports..."
    assert router_agent.classify_doc_type(doc) == "clinical_note"


def test_classify_research_abstract():
    doc = "Background: heart disease is common. Methods: we studied 100 patients. Results: ..."
    assert router_agent.classify_doc_type(doc) == "research_abstract"


def test_classify_unspecified():
    doc = "Just some plain text with no medical structure markers at all."
    assert router_agent.classify_doc_type(doc) == "unspecified_medical_document"


def test_route_short_document_not_chunked():
    doc = "short document " * 5
    decision = router_agent.route(doc)
    assert decision.chunked is False
    assert len(decision.chunks) == 1


def test_route_long_document_is_chunked(monkeypatch):
    from app import config

    monkeypatch.setattr(config, "MAX_SOURCE_TOKENS", 20)
    paragraphs = [f"Paragraph {i} " + ("word " * 15) for i in range(5)]
    doc = "\n\n".join(paragraphs)
    decision = router_agent.route(doc)
    assert decision.chunked is True
    assert len(decision.chunks) > 1
    # every original paragraph's content should show up somewhere in the chunks
    rejoined = " ".join(decision.chunks)
    for i in range(5):
        assert f"Paragraph {i}" in rejoined

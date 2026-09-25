from app.agents import verification_agent


def test_verify_full_coverage_passes():
    source = "Patient was prescribed aspirin and diagnosed with pneumonia."
    summary = "The patient has pneumonia and was given aspirin."
    result = verification_agent.verify(source, summary)
    assert result.passed is True
    assert result.coverage == 1.0
    assert result.missing_entities == []


def test_verify_partial_coverage_flagged():
    source = "Patient was prescribed aspirin, amoxicillin, and diagnosed with pneumonia."
    summary = "The patient has pneumonia."  # omits aspirin and amoxicillin
    result = verification_agent.verify(source, summary)
    assert result.coverage < 1.0
    assert "aspirin" in result.missing_entities
    assert "amoxicillin" in result.missing_entities
    assert result.passed is False  # 1/3 coverage is below the 0.5 default threshold


def test_verify_no_entities_in_source_passes_by_default():
    source = "Nothing clinically notable here."
    summary = "A generic summary."
    result = verification_agent.verify(source, summary)
    assert result.passed is True
    assert result.source_entity_count == 0

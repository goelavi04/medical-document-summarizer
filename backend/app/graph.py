"""LangGraph orchestration wiring together the four agents.

Flow:
    router -> summarizer -> verification -> [coverage low & attempts left?] -> summarizer (strict retry)
                                          -> explainer -> END
"""
from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, StateGraph

from app import config
from app.agents import explainer_agent, router_agent, summarizer_agent, verification_agent


class PipelineState(TypedDict, total=False):
    document: str
    doc_type: str
    token_count: int
    chunked: bool
    chunks: list[str]
    technical_summary: str
    verification: dict
    regeneration_count: int
    patient_explanation: dict


def router_node(state: PipelineState) -> PipelineState:
    decision = router_agent.route(state["document"])
    return {
        "doc_type": decision.doc_type,
        "token_count": decision.token_count,
        "chunked": decision.chunked,
        "chunks": decision.chunks,
    }


def summarizer_node(state: PipelineState) -> PipelineState:
    strict = state.get("regeneration_count", 0) > 0
    summary = summarizer_agent.summarize(state["chunks"], strict=strict)
    return {"technical_summary": summary}


def verification_node(state: PipelineState) -> PipelineState:
    result = verification_agent.verify(state["document"], state["technical_summary"])
    return {
        "verification": {
            "passed": result.passed,
            "coverage": round(result.coverage, 4),
            "source_entity_count": result.source_entity_count,
            "matched_entities": result.matched_entities,
            "missing_entities": result.missing_entities,
            "threshold": result.threshold,
        }
    }


def route_after_verification(state: PipelineState) -> str:
    verification = state["verification"]
    attempts = state.get("regeneration_count", 0)
    if not verification["passed"] and attempts < config.MAX_REGENERATION_ATTEMPTS:
        return "retry"
    return "proceed"


def bump_regeneration_node(state: PipelineState) -> PipelineState:
    return {"regeneration_count": state.get("regeneration_count", 0) + 1}


def explainer_node(state: PipelineState) -> PipelineState:
    result = explainer_agent.explain(state["technical_summary"])
    return {"patient_explanation": result}


def build_graph():
    graph = StateGraph(PipelineState)

    graph.add_node("router", router_node)
    graph.add_node("summarizer", summarizer_node)
    graph.add_node("verification", verification_node)
    graph.add_node("bump_regeneration", bump_regeneration_node)
    graph.add_node("explainer", explainer_node)

    graph.set_entry_point("router")
    graph.add_edge("router", "summarizer")
    graph.add_edge("summarizer", "verification")
    graph.add_conditional_edges(
        "verification",
        route_after_verification,
        {"retry": "bump_regeneration", "proceed": "explainer"},
    )
    graph.add_edge("bump_regeneration", "summarizer")
    graph.add_edge("explainer", END)

    return graph.compile()


_compiled_graph = None


def get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph


def run_pipeline(document: str) -> PipelineState:
    graph = get_graph()
    initial_state: PipelineState = {"document": document, "regeneration_count": 0}
    final_state = graph.invoke(initial_state)
    return final_state

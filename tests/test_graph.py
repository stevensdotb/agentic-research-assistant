from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END

from src.agents.researcher import (
    EVALUATOR_NODE,
    RESEARCHER_NODE,
    SEARCH_LIMIT_ANSWER_NODE,
    TOOL_NODE,
    route_after_evaluation,
    route_after_researcher,
    smart_researcher,
)
from src.state import EvaluationConstants, MAX_SEARCH_LIMIT


def test_graph_has_all_nodes():
    graph = smart_researcher.get_graph()
    node_ids = set(graph.nodes.keys())
    assert RESEARCHER_NODE in node_ids
    assert TOOL_NODE in node_ids
    assert EVALUATOR_NODE in node_ids
    assert SEARCH_LIMIT_ANSWER_NODE in node_ids


def test_route_after_researcher_at_search_limit():
    state = {
        "messages": [HumanMessage(content="q"), AIMessage(content="a")],
        "search_count": MAX_SEARCH_LIMIT,
        "evaluation_result": EvaluationConstants.PENDING,
        "feedback": "",
    }
    assert route_after_researcher(state) == SEARCH_LIMIT_ANSWER_NODE


def test_route_after_researcher_no_tool_calls():
    state = {
        "messages": [HumanMessage(content="q"), AIMessage(content="a")],
        "search_count": 0,
        "evaluation_result": EvaluationConstants.PENDING,
        "feedback": "",
    }
    assert route_after_researcher(state) == EVALUATOR_NODE


def test_route_after_researcher_with_tool_calls():
    ai_msg = AIMessage(
        content="",
        tool_calls=[{"name": "web_search", "args": {"query": "test"}, "id": "1"}],
    )
    state = {
        "messages": [HumanMessage(content="q"), ai_msg],
        "search_count": 0,
        "evaluation_result": EvaluationConstants.PENDING,
        "feedback": "",
    }
    assert route_after_researcher(state) == TOOL_NODE


def test_route_after_evaluation_insufficient():
    state = {
        "messages": [],
        "evaluation_result": EvaluationConstants.INSUFFICIENT,
        "feedback": "needs more detail",
    }
    assert route_after_evaluation(state) == RESEARCHER_NODE


def test_route_after_evaluation_sufficient():
    state = {
        "messages": [],
        "evaluation_result": EvaluationConstants.SUFFICIENT,
        "feedback": "",
    }
    assert route_after_evaluation(state) == END

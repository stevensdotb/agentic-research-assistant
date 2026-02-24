from src.state import AgentState, EvaluationConstants, MAX_SEARCH_LIMIT


def test_evaluation_constants_values():
    assert EvaluationConstants.SUFFICIENT == "sufficient"
    assert EvaluationConstants.INSUFFICIENT == "insufficient"
    assert EvaluationConstants.PENDING == "pending"


def test_max_search_limit():
    assert MAX_SEARCH_LIMIT == 10


def test_agent_state_keys():
    expected_keys = {"messages", "evaluation_result", "feedback", "search_count", "is_task_complete"}
    assert set(AgentState.__annotations__.keys()) == expected_keys

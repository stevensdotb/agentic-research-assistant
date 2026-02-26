from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from src.nodes import evaluator_node, researcher_node, search_limit_answer_node
from src.state import AgentState, EvaluationConstants, MAX_SEARCH_LIMIT
from src.tools import tools

# Node name constants
RESEARCHER_NODE = "researcher"
EVALUATOR_NODE = "evaluator"
WEB_SEARCH_NODE = "web_search"
SEARCH_LIMIT_ANSWER_NODE = "search_limit_answer"


def route_after_researcher(state: AgentState) -> str:
    """Route researcher output: tools, search_limit_answer (if limit hit), or evaluator."""
    if state.get("search_count", 0) >= MAX_SEARCH_LIMIT:
        return SEARCH_LIMIT_ANSWER_NODE
    # tools_condition returns "tools" if tool calls present, otherwise "__end__"
    result = tools_condition(state)
    if result == END:
        return EVALUATOR_NODE
    return result


def route_after_evaluation(state: AgentState) -> str:
    """Route after evaluation: retry researcher or end (sufficient)."""
    if state["evaluation_result"] == EvaluationConstants.INSUFFICIENT:
        return RESEARCHER_NODE
    return END


# --- Graph construction ---
workflow = StateGraph(AgentState)

workflow.add_node(RESEARCHER_NODE, researcher_node)
workflow.add_node(WEB_SEARCH_NODE, ToolNode(tools))
workflow.add_node(EVALUATOR_NODE, evaluator_node)
workflow.add_node(SEARCH_LIMIT_ANSWER_NODE, search_limit_answer_node)

workflow.add_edge(START, RESEARCHER_NODE)

workflow.add_conditional_edges(
    RESEARCHER_NODE,
    route_after_researcher,
    {
        "tools": WEB_SEARCH_NODE,
        EVALUATOR_NODE: EVALUATOR_NODE,
        SEARCH_LIMIT_ANSWER_NODE: SEARCH_LIMIT_ANSWER_NODE,
    },
)

workflow.add_edge(WEB_SEARCH_NODE, RESEARCHER_NODE)

workflow.add_conditional_edges(
    EVALUATOR_NODE,
    route_after_evaluation,
    {
        RESEARCHER_NODE: RESEARCHER_NODE,
        END: END,
    },
)

workflow.add_edge(SEARCH_LIMIT_ANSWER_NODE, END)

smart_researcher = workflow.compile()

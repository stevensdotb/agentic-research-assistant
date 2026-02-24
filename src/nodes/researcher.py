from datetime import date

from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

from src.ollama_client import create_ollama_client
from src.prompts import RESEARCHER_SYSTEM_PROMPT
from src.state import AgentState, MAX_SEARCH_LIMIT
from src.tools import tools

model = create_ollama_client(tools)


def researcher_node(state: AgentState) -> dict:
    """Reasons about the query and decides to search or respond."""
    current_date = date.today().isoformat()
    messages = [
        SystemMessage(content=RESEARCHER_SYSTEM_PROMPT.format(current_date=current_date))
    ] + list(state["messages"])

    search_count = state.get("search_count", 0)

    if state.get("feedback"):
        messages.append(
            HumanMessage(
                content=f"Evaluator feedback: {state['feedback']}. Use it to improve the response."
            )
        )

    try:
        response = model.invoke(messages)
    except Exception as e:
        return {
            "messages": [AIMessage(content=f"Error calling LLM: {e}")],
            "feedback": "",
            "search_count": search_count,
        }

    return {
        "messages": [response],
        "feedback": "",
        "search_count": (search_count + 1) if response.tool_calls else search_count,
    }

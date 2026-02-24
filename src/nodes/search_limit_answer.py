from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.ollama_client import create_ollama_client
from src.prompts import FINAL_SYNTHESIS_PROMPT
from src.state import AgentState, EvaluationConstants

model = create_ollama_client()


def search_limit_answer_node(state: AgentState) -> dict:
    """Produces a final answer when the search limit has been reached.

    Filters to human/AI messages with actual content since this model
    has no tools bound and tool-call messages would confuse it.
    """
    context = [
        msg for msg in state["messages"]
        if isinstance(msg, (HumanMessage, AIMessage)) and msg.content
    ]

    messages = [SystemMessage(content=FINAL_SYNTHESIS_PROMPT)] + context

    try:
        final_response = model.invoke(messages)
    except Exception as e:
        return {
            "messages": [AIMessage(content=f"Error during search limit answer: {e}")],
            "evaluation_result": EvaluationConstants.SUFFICIENT,
        }

    return {
        "messages": [final_response],
        "evaluation_result": EvaluationConstants.SUFFICIENT,
    }

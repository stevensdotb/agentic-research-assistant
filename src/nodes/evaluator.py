import json

from src.ollama_client import create_ollama_client
from src.prompts import EVALUATOR_PROMPT
from src.state import AgentState, EvaluationConstants

model = create_ollama_client()


def evaluator_node(state: AgentState) -> dict:
    """Evaluates the response from the researcher agent.
    If the response is sufficient, marks the task as complete.
    If not, indicates that more information is needed.
    """
    messages = state["messages"]
    user_question = messages[0].content
    current_response = messages[-1].content

    prompt = EVALUATOR_PROMPT.format(
        user_question=user_question,
        current_response=current_response,
    )

    if state.get("evaluation_result") == EvaluationConstants.SUFFICIENT:
        return {
            "evaluation_result": EvaluationConstants.SUFFICIENT,
            "feedback": "",
        }

    try:
        evaluator = model.invoke(prompt)
    except Exception as e:
        return {
            "evaluation_result": EvaluationConstants.INSUFFICIENT,
            "feedback": f"LLM error during evaluation: {e}. Retrying research.",
        }

    try:
        data = json.loads(evaluator.content)
        return {
            "evaluation_result": data["evaluation_result"],
            "feedback": data.get("feedback", ""),
        }
    except (json.JSONDecodeError, KeyError):
        return {
            "evaluation_result": EvaluationConstants.INSUFFICIENT,
            "feedback": "Error parsing evaluation response. Try researching deeper.",
        }

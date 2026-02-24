from enum import StrEnum
from typing import Annotated, Sequence, Literal
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


MAX_SEARCH_LIMIT = 10

class EvaluationConstants(StrEnum):
    SUFFICIENT = "sufficient"
    INSUFFICIENT = "insufficient"
    PENDING = "pending"


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    evaluation_result: Literal[
        EvaluationConstants.SUFFICIENT,
        EvaluationConstants.INSUFFICIENT,
        EvaluationConstants.PENDING
    ]
    feedback: str
    search_count: int
    is_task_complete: bool

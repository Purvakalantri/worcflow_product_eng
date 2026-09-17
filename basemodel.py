from pydantic import BaseModel
from typing import TypedDict, Annotated, Any
from langgraph.graph import add_messages


class WorkflowState(TypedDict):
    gmail_service: Any
    messages: list
    threads: list
    commitments: list
    connected_user_email: str
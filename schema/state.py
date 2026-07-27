from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage


class State(TypedDict):
    subject: str
    query_type: Literal["fee", "academic", "general"]
    messages: Annotated[list[AnyMessage], add_messages]
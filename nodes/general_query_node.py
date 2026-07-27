from schema import State
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage
from llm import chat_llm, parser


def general_query_node(state: State) -> dict:
    """
    This node handles general queries by retrieving relevant information from the general knowledge base.
    """

    query = state["messages"][-1].content
    general_prompt = PromptTemplate.from_template(
        """
Subject: {subject}

You are a helpful assistant for answering student queries related to general matters.

Query: {query}

Answer the query based on your own knowledge
        """
    )

    chain = general_prompt | chat_llm | parser

    response = AIMessage(content=chain.invoke({"query": query, "subject": state["subject"]}))

    return {"messages": [response]}
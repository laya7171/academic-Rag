from schema import State
from ingestion.fee_ingestion import fee_retriever
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage
from llm import chat_llm, parser

def fee_rag_node(state: State) -> dict:
    """
    This node handles fee-related queries by retrieving relevant information from the fee knowledge base."""

    query = state["messages"][-1].content
    retrieved_info = fee_retriever.invoke(query)

    joined_info = "\n".join([doc.page_content for doc in retrieved_info])

    fee_prompt = PromptTemplate.from_template(
        """
Subject: {subject}

You are a helpful assistant for answering student queries related to college fees. Use the following information to answer the query.

Information:
{retrieved_info}

Query: {query}

Answer the query based on the information provided. If the information is not sufficient, respond with 'I don't know'.
        """
    )

    chain = fee_prompt | chat_llm | parser

    response = AIMessage(content=chain.invoke({"retrieved_info": joined_info, "query": query, "subject": state["subject"]}))

    return {"messages": [response]}


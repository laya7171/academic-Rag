from schema import State
from ingestion.academic_ingestion import academic_retriever
from langchain_core.prompts import PromptTemplate
from llm import chat_llm, parser
from langchain_core.messages import AIMessage

def academic_rag_node(state: State) -> dict:
    """
    This node handles academic-related queries by retrieving relevant information from the academic knowledge base.
    """

    query = state["messages"][-1].content
    retrieved_info = academic_retriever.invoke(query)

    joined_info = "\n".join([doc.page_content for doc in retrieved_info])

    academic_prompt = PromptTemplate.from_template(
        """
Subject: {subject}

You are a helpful assistant for answering student queries related to academic matters. Use the following information to answer the query.

Information:
{retrieved_info}

Query: {query}

Answer the query based on the information provided. If the information is not sufficient, respond with 'I don't know'.
        """
    )

    chain = academic_prompt | chat_llm | parser

    response = AIMessage(content=chain.invoke({"retrieved_info": joined_info, "query": query, "subject": state["subject"]}))

    return {"messages": [response]}
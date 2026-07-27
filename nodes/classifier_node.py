from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from schema import State
from llm import chat_llm


def classifier_node(state: State) -> dict:
    last_message = state["messages"][-1].content

    prompt = PromptTemplate.from_template(
        """
        Classify the following student query into exactly one category:

        - academic
        - fee
        - general

        Academic includes questions about attendance, exams, grading,
        credits, promotion, course structure, summer training,
        or degree requirements.

        Fee includes questions about tuition, payment, refund,
        late charges, scholarships, or money-related topics.

        General includes greetings, casual talk, or unrelated questions.

        Query:
        {query}

        Return only one word:
        academic, fee, or general.
        """
    )

    chain = prompt | chat_llm | StrOutputParser()

    raw_response = chain.invoke({"query": last_message})
    cleaned_response = str(raw_response).strip().lower().strip(".'\" \n\t")

    if "academic" in cleaned_response:
        qtype = "academic"
    elif "fee" in cleaned_response:
        qtype = "fee"
    else:
        qtype = "general"

    return {
        "query_type": qtype
    }
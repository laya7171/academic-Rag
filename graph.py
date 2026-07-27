from langgraph.graph import StateGraph, START, END
from schema import State
from nodes.classifier_node import classifier_node
from nodes.router_node import router_node
from nodes.academic_rag_node import academic_rag_node
from nodes.fee_rag_node import fee_rag_node
from nodes.general_query_node import general_query_node


graph = StateGraph(State)
graph.add_node("classifier_node", classifier_node)
graph.add_node("academic_node", academic_rag_node)
graph.add_node("fee_node", fee_rag_node)
graph.add_node("general_node", general_query_node)


graph.add_edge(START, "classifier_node")
graph.add_conditional_edges(
    "classifier_node",
    router_node,
    {
        "academic": "academic_node",
        "fee": "fee_node",
        "general": "general_node",
    }
)
graph.add_edge("academic_node", END)
graph.add_edge("fee_node", END)
graph.add_edge("general_node", END)

workflow = graph.compile()



#workflow = graph.compile()
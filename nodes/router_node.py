from schema import State

def router_node(state: State) -> str:
    """
    Look at the latest message and then route the query and decide which path to take."""

    query_type = state.get("query_type", "general")

    if "academic" in query_type:
        return "academic"
    elif "fee" in query_type:
        return "fee"
    else:
        return "general"
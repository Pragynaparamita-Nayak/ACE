def route_agent(state):
    """
    Reads next agent decided by supervisor
    and returns node name for LangGraph routing.
    """

    next_agent = state.get("next_agent")

    valid_agents = [
        "research",
        "summarizer",
        "synthesizer",
        "reviewer"
    ]

    if next_agent not in valid_agents:
        raise ValueError(
            f"Invalid next agent: {next_agent}"
        )

    return next_agent
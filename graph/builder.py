from langgraph.graph import StateGraph, END
from graph.state import AgentState

from agents.planner_agent import planner_node
from agents.supervisor_agent import supervisor_node
from agents.research_agent import research_node
from agents.summerizer_agent import summarizer_node
from agents.synthesizer_agent import synthesizer_node
from agents.reviewer_agent import reviewer_node

builder = StateGraph(AgentState)

# Add Nodes
builder.add_node("planner", planner_node)
builder.add_node("supervisor", supervisor_node)
builder.add_node("research", research_node)
builder.add_node("summarizer", summarizer_node)
builder.add_node("synthesizer", synthesizer_node)
builder.add_node("reviewer", reviewer_node)

# Entry Point
builder.set_entry_point("planner")

# Planner -> Supervisor
builder.add_edge("planner", "supervisor")


def route_agent(state):
    return state["next_agent"]


# Conditional Routing
builder.add_conditional_edges(
    "supervisor",
    route_agent,
    {
        "research": "research",
        "summarizer": "summarizer",
        "synthesizer": "synthesizer",   # NEW
        "reviewer": "reviewer"          # NEW
    }
)

# Sequential Flow
builder.add_edge("research", "summarizer")
builder.add_edge("summarizer", "synthesizer")
builder.add_edge("synthesizer", "reviewer")
builder.add_edge("reviewer", END)

graph = builder.compile()
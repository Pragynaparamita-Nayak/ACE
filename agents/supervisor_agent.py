from langsmith import traceable

@traceable(name="Supervisor Agent")
def supervisor_node(state):

    research_results = state.get("research_results", [])
    summarized_results = state.get("summarized_results", [])
    files = state.get("files", {})
    review_status = state.get("review_status", "")

    # Step 1 → Research
    if len(research_results) == 0:
        state["next_agent"] = "research"

    # Step 2 → Summarizer
    elif len(summarized_results) == 0:
        state["next_agent"] = "summarizer"

    # Step 3 → Synthesizer
    elif "final_report.txt" not in files:
        state["next_agent"] = "synthesizer"

    # Step 4 → Reviewer
    elif review_status == "":
        state["next_agent"] = "reviewer"

    state["completed_tasks"].append("Supervisor routing completed")

    return state
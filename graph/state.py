from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    user_input: str
    todos: list
    next_agent: str

    research_results: list
    task_results: list
    summarized_results: list

    citations: list
    images: list

    files: dict
    logs: list
    completed_tasks: list
    agent_status: dict

    review_status: str
    review_messages: list

    judge_scores: dict
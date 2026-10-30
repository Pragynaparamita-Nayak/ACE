from langsmith import traceable
from tools.todo_tool import write_todos


# ----------------------------
# Token Estimator
# ----------------------------
def estimate_tokens(task):
    task_lower = task.lower()

    if "define" in task_lower:
        return 900
    elif "history" in task_lower:
        return 1700
    elif "application" in task_lower or "example" in task_lower:
        return 700
    elif "compare" in task_lower:
        return 800
    elif "code" in task_lower:
        return 500
    elif "architecture" in task_lower:
        return 1000
    else:
        return 900


# ----------------------------
# Planner Agent
# ----------------------------
@traceable(name="Planner Agent")
def planner_node(state):

    user_task = state["user_input"]

    raw_todos = write_todos(user_task)
    normalized_todos = []

    for todo in raw_todos:

        # ----------------------------
        # Case 1: TODO is string
        # ----------------------------
        if isinstance(todo, str):
            task_name = todo

            normalized_todos.append({
                "task": task_name,
                "token_limit": estimate_tokens(task_name),
                "need_research": False,
                "need_citation": False,
                "need_code": False,
                "need_image": False
            })

        # ----------------------------
        # Case 2: TODO is dict
        # ----------------------------
        elif isinstance(todo, dict):
            task_name = todo.get("task", "Unknown Task")

            normalized_todos.append({
                "task": task_name,
                "token_limit": todo.get(
                    "token_limit",
                    estimate_tokens(task_name)
                ),
                "need_research": todo.get(
                    "need_research", False
                ),
                "need_citation": todo.get(
                    "need_citation", False
                ),
                "need_code": todo.get(
                    "need_code", False
                ),
                "need_image": todo.get(
                    "need_image", False
                )
            })

    state["todos"] = normalized_todos

    # ----------------------------
    # Planner Score
    # ----------------------------
    score = 0
    total_todos = len(normalized_todos)

    if total_todos > 0:
        score += 40

    valid_tasks = sum(
        1 for todo in normalized_todos
        if todo["task"] != "Unknown Task"
    )

    if total_todos > 0:
        score += int((valid_tasks / total_todos) * 30)

    valid_tokens = sum(
        1 for todo in normalized_todos
        if todo["token_limit"] > 0
    )

    if total_todos > 0:
        score += int((valid_tokens / total_todos) * 30)

    state["agent_status"]["Planner Agent"] = score

    state["completed_tasks"].append(
        f"Planning completed ({score}%)"
    )

    state["logs"].append(
        f"Planner generated {total_todos} tasks"
    )

    print("\nPLANNER TODOS:")
    for todo in normalized_todos:
        print(todo)

    return state
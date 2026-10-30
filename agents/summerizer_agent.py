from langsmith import traceable
from models.llm import llm

@traceable(name="Summarizer Agent")
def summarizer_node(state):

    research_results = state["research_results"]
    summarized_results = []

    total_tasks = len(research_results)
    successful_tasks = 0

    for item in research_results:
        task_name = item["task"]
        task_results = item["results"]

        try:
            prompt = f"""
            Summarize the following research clearly.

            Task:
            {task_name}

            Research Results:
            {task_results}

            Keep only important facts.
            """

            response = llm.invoke(prompt)

            summary = response.content.strip()

            if summary:
                successful_tasks += 1

                summarized_results.append({
                    "task": task_name,
                    "summary": summary
                })

        except Exception as e:
            state["logs"].append(
                f"Summarizer failed for task: {task_name}"
            )

    # Dynamic %
    if total_tasks > 0:
        score = int((successful_tasks / total_tasks) * 100)
    else:
        score = 0

    state["summarized_results"] = summarized_results
    state["agent_status"]["Summarizer Agent"] = score
    state["completed_tasks"].append(
        f"Summarization completed ({score}%)"
    )

    return state
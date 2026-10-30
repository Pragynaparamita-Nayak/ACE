from langsmith import traceable
from models.llm import llm
from tools.file_tool import write_file


@traceable(name="Synthesizer Agent")
def synthesizer_node(state):

    summarized_results = state["summarized_results"]
    todos = state["todos"]
    images = state.get("images", [])

    markdown = "# Final Report\n\n"

    task_no = 1

    for item in summarized_results:
        task = item["task"]
        summary = item["summary"]

        # Task heading
        markdown += f"## {task}\n"
        markdown += f"{summary}\n\n"

        # Save task file
        file_content = f"{task}\n\n{summary}"
        write_file(
            f"task_{task_no}.txt",
            file_content
        )

        # ------------------------
        # Image insertion
        # ------------------------
        task_images = [
            img for img in images
            if img["task"].strip().lower()
            == task.strip().lower()
        ]

        for img in task_images:
            markdown += (
                f"![Task Image]"
                f"({img['path']})\n\n"
            )

        task_no += 1

    state["files"]["final_report.txt"] = markdown

    write_file("final_report.txt", markdown)

    # ------------------------
    # Dynamic Scoring
    # ------------------------
    score = 0

    if markdown.strip():
        score += 40

    total_todos = len(todos)
    matched_headings = 0

    for todo in todos:
        task_name = todo["task"]

        if f"## {task_name}" in markdown:
            matched_headings += 1

    if total_todos > 0:
        score += int(
            (matched_headings / total_todos) * 40
        )

    if len(markdown) > 200:
        score += 20

    state["agent_status"]["Synthesizer Agent"] = score

    state["completed_tasks"].append(
        f"Synthesis completed ({score}%)"
    )

    state["logs"].append(
        f"Stored {task_no - 1} task files in Virtual Memory"
    )

    return state
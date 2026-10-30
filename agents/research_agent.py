from langsmith import traceable
from tools.web_search import search_web
from tools.image_tool import search_image


@traceable(name="Research Agent")
def research_node(state):

    todos = state["todos"]

    research_results = []
    citations = []
    images = []

    total_tasks = len(todos)
    successful_tasks = 0

    for todo in todos:
        task_name = todo["task"]

        # -------------------------
        # Web Search
        # -------------------------
        results = search_web(task_name)

        valid_result = (
            results
            and isinstance(results, list)
            and len(results) > 0
            and results[0].get("title", "") != "Search Error"
        )

        if valid_result:
            successful_tasks += 1

            research_results.append({
                "task": task_name,
                "results": results
            })

            # -------------------------
            # Citation Handling
            # -------------------------
            if todo.get("need_citation", False):
                for item in results:
                    citations.append({
                        "task": task_name,
                        "title": item.get("title", ""),
                        "url": item.get("url", "")
                    })

        # -------------------------
        # Image Handling
        # -------------------------
        if todo.get("need_image", False):
            image_url = search_image(task_name)

            if image_url:
                images.append({
                    "task": task_name,
                    "path": image_url
                })

                state["logs"].append(
                    f"Image found for {task_name}"
                )
            else:
                state["logs"].append(
                    f"No image found for {task_name}"
                )

    # -------------------------
    # Dynamic Success %
    # -------------------------
    if total_tasks > 0:
        score = int(
            (successful_tasks / total_tasks) * 100
        )
    else:
        score = 0

    state["research_results"] = research_results
    state["citations"] = citations
    state["images"] = images

    state["agent_status"]["Research Agent"] = score

    state["completed_tasks"].append(
        f"Research completed ({score}%)"
    )

    state["logs"].append(
        f"Research Agent processed {successful_tasks}/{total_tasks} tasks"
    )

    return state
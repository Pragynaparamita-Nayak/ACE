from langsmith import traceable
from models.llm import llm
import json


@traceable(name="TODO Tool")
def write_todos(user_task):

    # ----------------------------
    # LLM not initialized
    # ----------------------------
    if llm is None:
        return [{
            "task": "LLM not initialized",
            "need_research": False,
            "need_citation": False,
            "need_image": False,
            "token_limit": 200
        }]

    # ----------------------------
    # Prompt
    # ----------------------------
    prompt = f"""
Break the user task into 5 to 8 TODO tasks.

IMPORTANT RULES:
1. Every task MUST contain ALL keys below.
2. Return ONLY valid JSON.
3. Do not add explanation outside JSON.
4. If task requires diagram, architecture, chart, or image, set need_image = true.

Required keys:
- task
- need_research
- need_citation
- need_image
- token_limit

Example:
[
  {{
    "task": "Research transformer architecture",
    "need_research": true,
    "need_citation": true,
    "need_image": true,
    "token_limit": 500
  }}
]

User Task:
{user_task}
"""

    try:
        response = llm.invoke(prompt)
        content = response.content.strip()

        # Remove markdown fences if model adds them
        content = (
            content.replace("```json", "")
                   .replace("```", "")
                   .strip()
        )

        todos = json.loads(content)

        # ----------------------------
        # Ensure all keys exist
        # ----------------------------
        for todo in todos:

            if "task" not in todo:
                todo["task"] = "Unknown Task"

            if "need_research" not in todo:
                todo["need_research"] = False

            if "need_citation" not in todo:
                todo["need_citation"] = False

            if "need_image" not in todo:
                todo["need_image"] = False

            if "token_limit" not in todo:
                todo["token_limit"] = 250

            task_name = todo["task"].lower()
            query = user_task.lower()

            # Force image if visual task detected
            if (
                "diagram" in query
                or "image" in query
                or "chart" in query
                or "architecture" in query
                or "diagram" in task_name
                or "image" in task_name
                or "architecture" in task_name
            ):
                todo["need_image"] = True

        print("RAW TODOS =", todos)

        return todos

    except Exception as e:
        print("TODO Tool Error:", e)

        return [{
            "task": f"TODO generation failed: {str(e)}",
            "need_research": False,
            "need_citation": False,
            "need_image": False,
            "token_limit": 200
        }]
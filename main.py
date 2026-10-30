from dotenv import load_dotenv
load_dotenv()

from graph.builder import graph


def main():
    user_task = input("Enter your task: ")

    initial_state = {
        "user_input": user_task,
        "todos": [],
        "next_agent": "",

        "research_results": [],
        "task_results": [],
        "summarized_results": [],

        "citations": [],
        "images": [],

        "files": {},
        "logs": [],
        "completed_tasks": [],
        "agent_status": {},

        "review_status": "",
        "review_messages": [],
        "judge_scores": {}
    }

    result = graph.invoke(initial_state)

    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)

    print(
        result["files"].get(
            "final_report.txt",
            "No final report generated."
        )
    )

    # -------------------------
    # Debug images
    # -------------------------
    print("\n" + "=" * 60)
    print("IMAGES")
    print("=" * 60)

    images = result.get("images", [])

    if images:
        for img in images:
            print(img)
    else:
        print("No images generated")

    print("\n" + "=" * 60)
    print("COMPLETED TASKS")
    print("=" * 60)

    for task in result["completed_tasks"]:
        print(f"- {task}")

    print("\n" + "=" * 60)
    print("REVIEW STATUS")
    print("=" * 60)

    print(result.get("review_status", "Not reviewed"))

    if result.get("review_messages"):
        for msg in result["review_messages"]:
            print(f"- {msg}")


if __name__ == "__main__":
    main()
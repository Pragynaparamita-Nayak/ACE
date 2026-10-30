from langsmith import traceable
from models.llm import llm
import json


@traceable(name="Reviewer Agent")
def reviewer_node(state):

    print("REVIEWER STARTED")

    prompt = f"""
    You are an expert evaluator of a multi-agent AI system.

    Evaluate this system.

    User Query:
    {state["user_input"]}

    Planned Tasks:
    {state["todos"]}

    Research Results:
    {state["research_results"]}

    Summaries:
    {state["summarized_results"]}

    Final Report:
    {state["files"].get("final_report.txt", "")}

    Score from 0 to 10.

    Return ONLY valid JSON.
    Do not write anything outside JSON.

    {{
      "planning_score": 0,
      "routing_score": 0,
      "research_score": 0,
      "report_score": 0,
      "overall_score": 0,
      "feedback": ""
    }}
    """

    try:
        response = llm.invoke(prompt)

        print("\n===== RAW LLM RESPONSE =====")
        print(response.content)

        content = response.content.strip()

        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        print("\n===== CLEANED CONTENT =====")
        print(content)

        scores = json.loads(content)

        print("\n===== PARSED SCORES =====")
        print(scores)

        state["judge_scores"] = scores
        state["review_status"] = "LLM Judged"

    except Exception as e:
        print("\n===== REVIEWER ERROR =====")
        print(str(e))

        state["judge_scores"] = {
            "planning_score": 0,
            "routing_score": 0,
            "research_score": 0,
            "report_score": 0,
            "overall_score": 0,
            "feedback": f"Judge failed: {str(e)}"
        }

        state["review_status"] = "Judge Failed"
        state["review_messages"] = [str(e)]

    return state
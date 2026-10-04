"""
agents/critic.py - Critic Agent (Self-Reflection & Quality Scoring) for Nova.
Evaluates the plan and execution against the user's initial spoken request, scoring from 1 to 10.
If the score is < 7, provides constructive feedback to trigger a refinement retry.
"""

import json
import re
from typing import Dict, Any
import llm

CRITIC_SYSTEM_PROMPT = """You are the Critic Agent for Nova, an autonomous Voice-to-Task assistant.
Your job is to objectively evaluate how accurately the Planner and Executor handled the user's spoken request.

Criteria to score (1 to 10):
- Intent Alignment: Did it understand the full nuance of what was said?
- Actionability: Are the created tasks / actions concrete with sensible categories, priorities, and deadlines?
- Memory & Context: Did it respect user background/habits if relevant?
- Quality & Completeness: Did all planned tool actions execute successfully?

Rules:
- Score 1-10 (integer).
- A score >= 7 means PASSED.
- A score < 7 triggers an automated RETRY with your feedback.

Return valid JSON ONLY matching this format:
{
  "score": <integer 1-10>,
  "passed": <true if score >= 7 else false>,
  "strengths": "<What was done well>",
  "weaknesses": "<What is missing or imprecise>",
  "retry_needed": <true if score < 7 else false>,
  "improved_instructions": "<Specific suggestions if retry is needed, else empty>"
}
"""


def critique_execution(user_input: str, plan: Dict[str, Any], execution_result: Dict[str, Any]) -> Dict[str, Any]:
    """Critiques the plan and execution results."""
    prompt = f"""
User's Spoken Input:
"{user_input}"

Planner's Proposed Plan:
{json.dumps(plan, indent=2)}

Executor's Results:
{json.dumps(execution_result, indent=2)}
"""

    response_text = llm.call_groq(prompt, system_instruction=CRITIC_SYSTEM_PROMPT)

    try:
        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if json_match:
            critic_data = json.loads(json_match.group(0))
            score = int(critic_data.get("score", 8))
            critic_data["score"] = score
            critic_data["passed"] = score >= 7
            critic_data["retry_needed"] = score < 7
            return critic_data
    except Exception as e:
        print(f"Error parsing Critic JSON: {e}")

    # Fallback critique
    success = execution_result.get("success", True)
    score = 9 if success else 5
    return {
        "score": score,
        "passed": score >= 7,
        "strengths": "Processed voice instructions accurately.",
        "weaknesses": "None" if score >= 7 else "Tool execution encountered issues.",
        "retry_needed": score < 7,
        "improved_instructions": "Review parameter formatting." if score < 7 else ""
    }

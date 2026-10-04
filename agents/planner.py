"""
agents/planner.py - Planner Agent for VoxFlow Voice-to-Task Assistant.
Uses Meta Llama (NVIDIA NIM) / Gemini to analyze voice input, query persistent memory, and decompose into actionable steps.
"""

import json
import re
from typing import Dict, Any, List
import memory
import llm

PLANNER_SYSTEM_PROMPT = """You are the Planner Agent for VoxFlow, an autonomous Voice-to-Task assistant.
Your goal is to parse natural, spoken voice instructions and convert them into structured, actionable tasks, reminders, or memory updates.

You have access to the user's persistent memory (profile, habits, timezone, past context).

Available Tools you can plan:
1. `create_task(title: str, description: str, priority: str ('High'|'Medium'|'Low'), category: str, due_date: str, recurrence: str)`
2. `list_tasks(status: str, category: str)`
3. `complete_task(task_id: int)`
4. `save_user_memory(key: str, value: str, category: str)`
5. `calculate(expression: str)`
6. `schedule_reminder(event_title: str, time_str: str, details: str)`

Always return valid JSON ONLY with the following schema:
{
  "intent": "<Brief summary of what the user wants to accomplish>",
  "reasoning": "<Step-by-step reasoning considering user memory & voice context>",
  "planned_tools": [
    {
      "tool": "<tool_name>",
      "args": { ... }
    }
  ],
  "spoken_summary": "<A short, conversational phrase for TTS to speak back to the user>"
}
"""


def plan_task(voice_input: str, feedback_history: str = "") -> Dict[str, Any]:
    """Generates a structured plan and tool sequence based on the voice input and memory."""
    memory_context = memory.get_facts_context_string()
    recent_tasks = memory.get_tasks()[:5]
    
    tasks_context = "\n".join([f"- #{t['id']} [{t['status']}]: {t['title']} ({t['priority']} priority, due {t['due_date']})" for t in recent_tasks]) if recent_tasks else "None"

    prompt = f"""
User's Spoken Input: "{voice_input}"

Persistent User Memory / Facts:
{memory_context}

Recent Active Tasks in DB:
{tasks_context}
"""

    if feedback_history:
        prompt += f"""
CRITIC FEEDBACK FROM PREVIOUS FAILED ATTEMPT:
{feedback_history}
Please refine and improve the plan to resolve all criticisms!
"""

    response_text = llm.call_gemini(prompt, system_instruction=PLANNER_SYSTEM_PROMPT)

    # Extract JSON
    try:
        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if json_match:
            plan = json.loads(json_match.group(0))
            return plan
    except Exception as e:
        print(f"Error parsing Planner response JSON: {e}")

    # Fallback plan structure
    return {
        "intent": f"Process voice command: '{voice_input}'",
        "reasoning": "Standard plan decomposition fallback.",
        "planned_tools": [
            {
                "tool": "create_task",
                "args": {
                    "title": voice_input[:60],
                    "description": voice_input,
                    "priority": "Medium",
                    "category": "Voice Task",
                    "due_date": "Today",
                    "recurrence": "None"
                }
            }
        ],
        "spoken_summary": f"I've added '{voice_input[:40]}' to your task list."
    }

"""
tools.py - Actionable execution tools for VoxFlow Voice-to-Task Assistant.
Provides deterministic tool functions that agents can invoke.
"""

import json
import math
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import memory


def tool_create_task(title: str, description: str = "", priority: str = "Medium", 
                     category: str = "General", due_date: str = "", recurrence: str = "None") -> Dict[str, Any]:
    """Creates a new task in persistent memory."""
    # Normalize priority
    priority_norm = priority.capitalize()
    if priority_norm not in ["High", "Medium", "Low"]:
        priority_norm = "Medium"
        
    task_id = memory.create_task(
        title=title,
        description=description,
        priority=priority_norm,
        category=category.capitalize(),
        status="Pending",
        due_date=due_date,
        recurrence=recurrence
    )
    return {
        "success": True,
        "action": "create_task",
        "task_id": task_id,
        "message": f"Successfully created task #{task_id}: '{title}' [{priority_norm} priority, due: {due_date or 'No deadline'}]"
    }


def tool_list_tasks(status: Optional[str] = None, category: Optional[str] = None) -> Dict[str, Any]:
    """Lists current tasks from persistent memory with optional filters."""
    tasks = memory.get_tasks(status=status, category=category)
    return {
        "success": True,
        "action": "list_tasks",
        "count": len(tasks),
        "tasks": tasks
    }


def tool_complete_task(task_id: int) -> Dict[str, Any]:
    """Marks an existing task as Completed."""
    memory.update_task_status(task_id, "Completed")
    return {
        "success": True,
        "action": "complete_task",
        "task_id": task_id,
        "message": f"Task #{task_id} marked as Completed."
    }


def tool_save_user_memory(key: str, value: str, category: str = "general") -> Dict[str, Any]:
    """Saves or updates a persistent user preference, fact, or background detail."""
    memory.save_fact(key=key, value=value, category=category)
    return {
        "success": True,
        "action": "save_user_memory",
        "key": key,
        "message": f"Saved fact '{key}': {value} in category '{category}'"
    }


def tool_calculate(expression: str) -> Dict[str, Any]:
    """Evaluates safe mathematical expressions."""
    try:
        # Sanitize expression
        clean_expr = re.sub(r"[^0-9\+\-\*\/\(\)\.\%\s]", "", expression)
        result = eval(clean_expr, {"__builtins__": None, "math": math})
        return {
            "success": True,
            "action": "calculate",
            "expression": expression,
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "action": "calculate",
            "expression": expression,
            "error": str(e)
        }


def tool_schedule_reminder(event_title: str, time_str: str, details: str = "") -> Dict[str, Any]:
    """Schedules a calendar reminder or follow-up note."""
    task_id = memory.create_task(
        title=f"Reminder: {event_title}",
        description=f"Scheduled for {time_str}. Details: {details}",
        priority="High",
        category="Reminder",
        status="Pending",
        due_date=time_str,
        recurrence="None"
    )
    return {
        "success": True,
        "action": "schedule_reminder",
        "task_id": task_id,
        "message": f"Reminder scheduled for '{event_title}' at {time_str}."
    }


AVAILABLE_TOOLS = {
    "create_task": tool_create_task,
    "list_tasks": tool_list_tasks,
    "complete_task": tool_complete_task,
    "save_user_memory": tool_save_user_memory,
    "calculate": tool_calculate,
    "schedule_reminder": tool_schedule_reminder
}


def execute_tool_call(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatches a tool call safely."""
    if tool_name not in AVAILABLE_TOOLS:
        return {"success": False, "error": f"Tool '{tool_name}' not found."}
    try:
        fn = AVAILABLE_TOOLS[tool_name]
        return fn(**args)
    except Exception as e:
        return {"success": False, "error": f"Execution error in '{tool_name}': {str(e)}"}

"""
agents/executor.py - Executor Agent for Nova Voice-to-Task Assistant.
Takes the tool calls planned by the Planner Agent, safely executes them, and logs the output.
"""

from typing import Dict, Any, List
import tools


def execute_plan(plan: Dict[str, Any]) -> Dict[str, Any]:
    """Executes each planned tool sequentially and returns structured results."""
    tool_calls = plan.get("planned_tools", [])
    execution_results = []
    success_count = 0
    failure_count = 0

    for item in tool_calls:
        tool_name = item.get("tool")
        args = item.get("args", {})
        result = tools.execute_tool_call(tool_name, args)
        
        execution_results.append({
            "tool": tool_name,
            "args": args,
            "result": result
        })
        
        if result.get("success", False):
            success_count += 1
        else:
            failure_count += 1

    all_succeeded = failure_count == 0 and len(tool_calls) > 0

    return {
        "success": all_succeeded,
        "total_tools": len(tool_calls),
        "success_count": success_count,
        "failure_count": failure_count,
        "results": execution_results,
        "spoken_summary": plan.get("spoken_summary", "Tasks executed successfully.")
    }

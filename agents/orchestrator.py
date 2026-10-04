"""
agents/orchestrator.py - Multi-agent coordinator for Nova.
Orchestrates Planner -> Executor -> Critic (with automated retry loop) -> SQLite Memory -> TTS response.
"""

from typing import Dict, Any, List, Generator
from agents.planner import plan_task
from agents.executor import execute_plan
from agents.critic import critique_execution
import memory


def run_pipeline(user_input: str, max_retries: int = 2) -> Dict[str, Any]:
    """Runs the complete multi-agent workflow with self-correction retry loop."""
    pipeline_trace = []
    attempt = 0
    feedback_history = ""
    
    plan = {}
    exec_result = {}
    critic_result = {}

    while attempt <= max_retries:
        attempt_log = {
            "attempt": attempt + 1,
            "stage": f"Attempt {attempt + 1}",
        }

        # Step 1: Planner
        plan = plan_task(user_input, feedback_history=feedback_history)
        attempt_log["plan"] = plan

        # Step 2: Executor
        exec_result = execute_plan(plan)
        attempt_log["execution"] = exec_result

        # Step 3: Critic
        critic_result = critique_execution(user_input, plan, exec_result)
        attempt_log["critic"] = critic_result

        pipeline_trace.append(attempt_log)

        # Check if passed or need retry
        if critic_result.get("passed", True) or attempt == max_retries:
            break

        # Accumulate feedback for next attempt
        feedback_history += f"\n[Attempt {attempt + 1}] Score: {critic_result.get('score')}/10. Weaknesses: {critic_result.get('weaknesses')}. Suggestions: {critic_result.get('improved_instructions')}"
        attempt += 1

    # Step 4: Log to Persistent Memory
    final_spoken = plan.get("spoken_summary", "Tasks updated successfully.")
    
    history_id = memory.log_execution(
        user_request=user_input,
        transcribed_text=user_input,
        planner_output=str(plan),
        executor_output=str(exec_result),
        critic_score=critic_result.get("score", 8),
        critic_feedback=critic_result.get("weaknesses", "Approved"),
        retry_count=attempt,
        final_output=final_spoken
    )

    return {
        "user_input": user_input,
        "attempts": attempt + 1,
        "final_plan": plan,
        "final_execution": exec_result,
        "final_critic": critic_result,
        "spoken_response": final_spoken,
        "trace": pipeline_trace,
        "history_id": history_id
    }

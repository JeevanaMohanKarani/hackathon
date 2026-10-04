"""
memory.py - Persistent Memory Layer for Nova Voice-to-Task Assistant.
Uses SQLite for persistent storage of user facts, tasks, and multi-agent execution history.
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nova.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the database schema with tables for facts, tasks, and execution logs."""
    conn = get_connection()
    cursor = conn.cursor()

    # User Facts & Preferences
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_facts (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Persistent Task Board
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'Medium',
            category TEXT DEFAULT 'General',
            status TEXT DEFAULT 'Pending',
            due_date TEXT,
            recurrence TEXT DEFAULT 'None',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Multi-Agent Run History
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS execution_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_request TEXT,
            transcribed_text TEXT,
            planner_output TEXT,
            executor_output TEXT,
            critic_score INTEGER,
            critic_feedback TEXT,
            retry_count INTEGER DEFAULT 0,
            final_output TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    # Pre-seed some initial facts if empty
    cursor.execute("SELECT COUNT(*) as count FROM user_facts")
    if cursor.fetchone()["count"] == 0:
        cursor.execute("""
            INSERT OR REPLACE INTO user_facts (key, value, category) VALUES
            ('user_name', 'Alex', 'profile'),
            ('role', 'Senior AI Engineer & Tech Lead', 'profile'),
            ('preferred_timezone', 'IST (UTC+5:30)', 'settings'),
            ('work_hours', '9:00 AM - 6:00 PM', 'schedule'),
            ('primary_focus', 'Agentic Workflows & Multi-Agent Orchestration', 'context')
        """)
        conn.commit()

    # Pre-seed a couple sample tasks if empty
    cursor.execute("SELECT COUNT(*) as count FROM tasks")
    if cursor.fetchone()["count"] == 0:
        cursor.execute("""
            INSERT INTO tasks (title, description, priority, category, status, due_date, recurrence) VALUES
            ('Review Hackathon Architecture', 'Verify multi-agent loop with Planner, Executor, Critic and SQLite Memory', 'High', 'Hackathon', 'Completed', 'Today 10:30 AM', 'None'),
            ('Prepare Agent Demo Walkthrough', 'Structure voice-to-task pipeline testing with edge cases & retry loop', 'High', 'Hackathon', 'In Progress', 'Today 1:00 PM', 'None'),
            ('Daily Standup Sync', 'Review daily task board and upcoming priorities with the team', 'Medium', 'Work', 'Pending', 'Every Weekday 9:30 AM', 'Daily')
        """)
        conn.commit()

    conn.close()


# --- User Facts & Preferences APIs ---

def save_fact(key: str, value: str, category: str = "general"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO user_facts (key, value, category, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    """, (key.strip(), value.strip(), category.strip()))
    conn.commit()
    conn.close()


def get_all_facts() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT key, value, category, updated_at FROM user_facts ORDER BY updated_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_facts_context_string() -> str:
    facts = get_all_facts()
    if not facts:
        return "No specific persistent user facts recorded yet."
    lines = [f"- {f['key']} ({f['category']}): {f['value']}" for f in facts]
    return "\n".join(lines)


# --- Task Management APIs ---

def create_task(title: str, description: str = "", priority: str = "Medium", 
                category: str = "General", status: str = "Pending", 
                due_date: str = "", recurrence: str = "None") -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, description, priority, category, status, due_date, recurrence, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """, (title.strip(), description.strip(), priority, category, status, due_date, recurrence))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id


def get_tasks(status: Optional[str] = None, category: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    if status and status.lower() != "all":
        query += " AND status = ?"
        params.append(status)
    if category and category.lower() != "all":
        query += " AND category = ?"
        params.append(category)
    query += " ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 3 ELSE 4 END, id DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_task_status(task_id: int, new_status: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
    """, (new_status, task_id))
    conn.commit()
    conn.close()


def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


# --- Execution History APIs ---

def log_execution(user_request: str, transcribed_text: str, planner_output: str,
                  executor_output: str, critic_score: int, critic_feedback: str,
                  retry_count: int, final_output: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO execution_history (user_request, transcribed_text, planner_output, 
                                       executor_output, critic_score, critic_feedback, 
                                       retry_count, final_output, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (user_request, transcribed_text, planner_output, executor_output, critic_score, critic_feedback, retry_count, final_output))
    history_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return history_id


def get_execution_history(limit: int = 10) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM execution_history ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Initialize on import
init_db()

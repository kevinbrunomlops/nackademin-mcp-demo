from __future__ import annotations

import math
from typing import Annotated

from pydantic import Field
from fastmcp import FastMCP

mcp = FastMCP("Study tools server")

@mcp.tool 
def prioritize_task(
    task_name: Annotated[str, Field(description="Name of the task")],
    days_left: Annotated[int, Field(description="Days remaining until deadline")],
    difficulty: Annotated[int, Field(description="Difficulty from 1 to 5")],
    estimated_hours: Annotated[float, Field(description="Estimated number of hours needed")],
) -> dict:
    score = (difficulty * 2) + estimated_hours - days_left
    if score >= 8:
        priority = "high"
    elif score >= 4:
        priority = "medium"
    else:
        priority = "low"
    
    return {
        "task_name": task_name,
        "priority": priority,
        "score": score,
    }

@mcp.tool
def estimate_study_sessions(
    task_name: Annotated[str, Field(description="Name of the task or study goal")],
    total_hours_needed: Annotated[float, Field(description="Total number of study hours needed", ge=0)],
    session_length_minutes: Annotated[int, Field(description="Preferred length of each study session in minutes", gt=0)],
) -> dict: 
    hours_per_session = session_length_minutes / 60
    sessions_needed = 0 if total_hours_needed == 0 else math.ceil(total_hours_needed / hours_per_session)
    return {
        "task_name": task_name,
        "sessions_needed": sessions_needed,
        "summary": f"{task_name} needs about {sessions_needed} study sessions.", 
    }

@mcp.tool
def create_week_plan(
    total_tasks: Annotated[int, Field(description="Number of taks this week", gt=0)],
    available_hours_this_week: Annotated[float, Field(description="Available study hours this week", ge=0)],
    study_days_per_week: Annotated[int, Field(description="Study days this week", ge=1, le=7)],
) -> dict: 
    hours_per_day = round(available_hours_this_week / study_days_per_week, 2)
    hours_per_task = round(available_hours_this_week / total_tasks, 2)
    daily_plan = [{"day": i, "hours": hours_per_day} for i in range(1, study_days_per_week + 1)]
    return {
        "hours_per_day": hours_per_day,
        "hours_per_task": hours_per_task,
        "daily_plan": daily_plan,
        "summary": f"Study about {hours_per_day} hours per day",
    }

@mcp.tool
def break_down_task(
    task_name: Annotated[str, Field(description="Task name")],
    task_type: Annotated[str, Field(description="Task type, e.g. essay or exam")],
    estimated_hours: Annotated[float, Field(description="Estimated total hours", ge=0)],
) -> dict:
    templates = {
        "essay":["Understand instructions", "Research", "Outline", "Draft", "Revise", "Submit"],
        "exam":["Review topics", "Find weak areas", "Practice", "Repeat", "Final review"],
        "presentation":["Research", "Outline", "Make slides", "Practice", "Refine"],
        "coding assignement":["Read requirements", "Plan", "Code", "Test", "Document"],
    }
    steps = templates.get(task_type.lower(), ["Understand task", "Plan", "Do work", "Review", "Submit"])
    hours_per_step = round(estimated_hours /len(steps), 2) if steps else 0
    return {
        "task_name": task_name,
        "steps": [{"step": s, "hours": hours_per_step} for s in steps],
        "summary": f"{task_name} was split into {len(steps)} steps.",
    }
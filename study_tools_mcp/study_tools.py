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


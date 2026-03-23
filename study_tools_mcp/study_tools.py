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
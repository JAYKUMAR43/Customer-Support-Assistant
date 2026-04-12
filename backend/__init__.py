# Making backend a Python package
# __init__.py
# Version 1.0.1 - Fixed Relative Imports

from .models import Action, ActionType, Observation, IssueType, CustomerType, ChatTurn
from .tasks import TASK_EASY, TASK_MEDIUM, TASK_HARD, TASKS
from .grader import Grader

# ✅ Yeh line SABSE IMPORTANT hai — validator yahi dhundhta hai
SUBMISSION_TASKS = [
    {
        "id": "TASK_EASY",
        "level": "Easy",
        "task": TASK_EASY,
        "grader": Grader.evaluate,
    },
    {
        "id": "TASK_MEDIUM",
        "level": "Medium",
        "task": TASK_MEDIUM,
        "grader": Grader.evaluate,
    },
    {
        "id": "TASK_HARD",
        "level": "Hard",
        "task": TASK_HARD,
        "grader": Grader.evaluate,
    },
]

# Yeh bhi expose karo — kuch validators isko dhundhte hain
__all__ = [
    "SUBMISSION_TASKS",
    "TASKS",
    "Grader",
    "Action",
    "ActionType", 
    "Observation",
    "IssueType",
    "CustomerType",
    "ChatTurn",
]
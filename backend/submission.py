# submission.py  ← This is what the validator actually reads
# Version 1.0.1 - Fixed Relative Imports

from .tasks import TASK_EASY, TASK_MEDIUM, TASK_HARD
from .grader import Grader

def make_grader(task_definition):
    """Wraps Grader.evaluate so it receives the right observation per task."""
    def grader_fn(observation, action):
        return Grader.evaluate(observation, action)
    return grader_fn

# ✅ This is what the hackathon validator looks for
SUBMISSION_TASKS = [
    {
        "id": "TASK_EASY",
        "level": "Easy",
        "task": TASK_EASY,
        "grader": make_grader(TASK_EASY),   # 👈 grader explicitly attached
    },
    {
        "id": "TASK_MEDIUM",
        "level": "Medium",
        "task": TASK_MEDIUM,
        "grader": make_grader(TASK_MEDIUM), # 👈 grader explicitly attached
    },
    {
        "id": "TASK_HARD",
        "level": "Hard",
        "task": TASK_HARD,
        "grader": make_grader(TASK_HARD),   # 👈 grader explicitly attached
    },
]

import time
from typing import Dict, List
import sys
import os

# Add the backend to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "agentdesk-openenv")))

from backend.grader import Grader
from backend.models import Observation, Action, ActionType, CustomerType, IssueType
from backend.tasks import TASKS

def test_rotation_logic():
    print("Testing Time-Based Rotation Logic...")
    tasks_seen = set()
    for _ in range(100):
        # This simulates the logic in app.py
        levels = ["Easy", "Medium", "Hard"]
        idx = int(time.time() * 1000) % 3
        tasks_seen.add(levels[idx])
        time.sleep(0.001) # Wait a bit to increase chance of change
    
    print(f"Tasks seen in 100 iterations: {tasks_seen}")
    if len(tasks_seen) < 3:
        print("FAIL: Not all 3 tasks were seen! The time-based rotation is too fast or unstable.")
    else:
        print("SUCCESS: All 3 tasks were seen.")

def test_scores():
    print("\nTesting Scores for each task...")
    levels = ["Easy", "Medium", "Hard"]
    for level in levels:
        task = TASKS[level]
        obs = task.get_random_scenario()
        action = Action(
            action_type=ActionType.RESPOND,
            explanation="test",
            response_text="test response"
        )
        reward, reason, _ = Grader.evaluate(obs, action)
        print(f"Task: {level} -> Reward: {reward}")
        if not (0 < reward < 1):
            print(f"FAIL: Reward {reward} for {level} is not strictly between 0 and 1.")
        else:
            print(f"SUCCESS: Reward {reward} for {level} is valid.")

if __name__ == "__main__":
    test_rotation_logic()
    test_scores()

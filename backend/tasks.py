import random
from typing import List, Dict
from .models import Observation, CustomerType, IssueType, ChatTurn

class TaskDefinition:
    def __init__(self, id: str, level: str, scenarios: List[Dict]):
        self.id = id
        self.level = level
        self.scenarios = scenarios

    def get_random_scenario(self, reset_history=True) -> Observation:
        scenario = random.choice(self.scenarios)
        history = [ChatTurn(role="customer", content=scenario["query"])] if reset_history else []
        return Observation(
            customer_query=scenario["query"],
            order_value=scenario["order_value"],
            customer_type=scenario["customer_type"],
            issue_type=scenario["issue_type"],
            sentiment_score=scenario["sentiment_score"],
            conversation_history=history,
            task_id=self.id
        )

# Task 1: Easy (Helpful, low-risk)
TASK_EASY = TaskDefinition(
    id="TASK_EASY",
    level="Easy",
    scenarios=[
        {
            "query": "Where is my order? It shows as delivered but I don't see it.",
            "order_value": 45.0,
            "customer_type": CustomerType.NEW,
            "issue_type": IssueType.DELAYED,
            "sentiment_score": 0.4,
        },
        {
            "query": "Can you please cancel my order #9876? I changed my mind.",
            "order_value": 30.0,
            "customer_type": CustomerType.FREQUENT,
            "issue_type": IssueType.REFUND_REQUEST,
            "sentiment_score": 0.7,
        }
    ]
)

# Task 2: Medium (Aggravated, damage)
TASK_MEDIUM = TaskDefinition(
    id="TASK_MEDIUM",
    level="Medium",
    scenarios=[
        {
            "query": "The coffee maker I received is cracked and leaks everywhere. This is unacceptable!",
            "order_value": 120.0,
            "customer_type": CustomerType.FREQUENT,
            "issue_type": IssueType.DAMAGED,
            "sentiment_score": 0.2,
        },
        {
            "query": "You sent me a blue shirt but I ordered a red one. I need this for a party tonight.",
            "order_value": 25.0,
            "customer_type": CustomerType.NEW,
            "issue_type": IssueType.WRONG_ITEM,
            "sentiment_score": 0.3,
        }
    ]
)

# Task 3: Hard (High-value, high-risk, possible fraud)
TASK_HARD = TaskDefinition(
    id="TASK_HARD",
    level="Hard",
    scenarios=[
        {
            "query": "I never received this $1500 laptop. I want a refund right now. I've done this before with other shops and they were faster.",
            "order_value": 1500.0,
            "customer_type": CustomerType.RISKY,
            "issue_type": IssueType.REFUND_REQUEST,
            "sentiment_score": 0.1,
        },
        {
            "query": "The screen on this ultra-pro camera is slightly scratched. I want a full refund and I want to keep the camera. I am a very loyal customer.",
            "order_value": 2500.0,
            "customer_type": CustomerType.RISKY,
            "issue_type": IssueType.DAMAGED,
            "sentiment_score": 0.5,
        }
    ]
)

TASKS = {
    "Easy": TASK_EASY,
    "Medium": TASK_MEDIUM,
    "Hard": TASK_HARD
}

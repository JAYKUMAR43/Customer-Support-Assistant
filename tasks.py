import random
from typing import List, Dict
from models import Observation, CustomerType, ProductIssue

class TaskDefinition:
    def __init__(self, id: str, level: str, scenarios: List[Dict]):
        self.id = id
        self.level = level
        self.scenarios = scenarios

    def get_random_scenario(self) -> Observation:
        scenario = random.choice(self.scenarios)
        return Observation(
            customer_query=scenario["query"],
            order_value=scenario["order_value"],
            days_since_delivery=scenario["days_since_delivery"],
            customer_type=scenario["customer_type"],
            product_issue=scenario["product_issue"],
            task_id=self.id
        )

# Task 1: Easy (Standard queries)
TASK_EASY = TaskDefinition(
    id="TASK_EASY",
    level="Easy",
    scenarios=[
        {
            "query": "Where is my order? It shows as delivered but I don't see it.",
            "order_value": 45.0,
            "days_since_delivery": 1,
            "customer_type": CustomerType.NEW,
            "product_issue": ProductIssue.DELAYED,
        },
        {
            "query": "Can you please cancel my order #9876? I changed my mind.",
            "order_value": 30.0,
            "days_since_delivery": 0,
            "customer_type": CustomerType.FREQUENT,
            "product_issue": ProductIssue.NONE,
        }
    ]
)

# Task 2: Medium (Product issues)
TASK_MEDIUM = TaskDefinition(
    id="TASK_MEDIUM",
    level="Medium",
    scenarios=[
        {
            "query": "The coffee maker I received is cracked and leaks everywhere.",
            "order_value": 120.0,
            "days_since_delivery": 2,
            "customer_type": CustomerType.FREQUENT,
            "product_issue": ProductIssue.DAMAGED,
        },
        {
            "query": "You sent me a blue shirt but I ordered a red one.",
            "order_value": 25.0,
            "days_since_delivery": 3,
            "customer_type": CustomerType.NEW,
            "product_issue": ProductIssue.WRONG_ITEM,
        }
    ]
)

# Task 3: Hard (Fraud/Risky scenarios)
TASK_HARD = TaskDefinition(
    id="TASK_HARD",
    level="Hard",
    scenarios=[
        {
            "query": "I never received this $1500 laptop. I want a refund right now. I've done this before with other shops.",
            "order_value": 1500.0,
            "days_since_delivery": 0,
            "customer_type": CustomerType.RISKY,
            "product_issue": ProductIssue.NONE,
        },
        {
            "query": "The screen on this ultra-pro camera is slightly scratched. I want a full refund and I want to keep the camera.",
            "order_value": 2500.0,
            "days_since_delivery": 1,
            "customer_type": CustomerType.RISKY,
            "product_issue": ProductIssue.DAMAGED,
        }
    ]
)

TASKS = {
    "Easy": TASK_EASY,
    "Medium": TASK_MEDIUM,
    "Hard": TASK_HARD
}

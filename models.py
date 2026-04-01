from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field

class ActionType(str, Enum):
    REFUND = "REFUND"
    REPLACE = "REPLACE"
    ESCALATE = "ESCALATE"
    RESPOND = "RESPOND"

class Action(BaseModel):
    action_type: ActionType
    explanation: str = Field(..., description="Reasoning for the action")
    response_text: str = Field(..., description="Message sent to the customer")

class CustomerType(str, Enum):
    NEW = "NEW"
    FREQUENT = "FREQUENT"
    RISKY = "RISKY"

class ProductIssue(str, Enum):
    NONE = "NONE"
    DAMAGED = "DAMAGED"
    WRONG_ITEM = "WRONG_ITEM"
    DELAYED = "DELAYED"

class Observation(BaseModel):
    customer_query: str
    order_value: float
    days_since_delivery: int
    customer_type: CustomerType
    product_issue: ProductIssue
    task_id: str

class Reward(BaseModel):
    value: float
    reason: str
    is_terminal: bool = False

class State(BaseModel):
    observation: Observation
    cumulative_reward: float
    step_count: int
    done: bool
    info: dict = {}

class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict = {}

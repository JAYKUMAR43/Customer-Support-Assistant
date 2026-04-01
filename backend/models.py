from enum import Enum
from typing import List, Optional, Union, Dict
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

class IssueType(str, Enum):
    DELAYED = "DELAYED"
    DAMAGED = "DAMAGED"
    WRONG_ITEM = "WRONG_ITEM"
    REFUND_REQUEST = "REFUND_REQUEST"

class ChatTurn(BaseModel):
    role: str # 'customer' or 'agent'
    content: str

class Observation(BaseModel):
    customer_query: str
    order_value: float
    customer_type: CustomerType
    issue_type: IssueType
    sentiment_score: float = Field(..., description="0.0 (negative) to 1.0 (positive)")
    conversation_history: List[ChatTurn] = []
    task_id: str

class Reward(BaseModel):
    value: float
    reason: str
    business_impact: float = 0.0
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

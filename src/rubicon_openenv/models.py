from pydantic import BaseModel
from typing import List, Dict, Optional

class Observation(BaseModel):
    step: int
    alerts: List[str]
    belief: Dict[str, float]
    uncertainty: float
    action_history: List[str]
    time_remaining: int

class Action(BaseModel):
    action_type: str

class Reward(BaseModel):
    value: float
    reason: str

class State(BaseModel):
    step: int
    ground_truth: str
    belief: Dict[str, float]
    committed: bool

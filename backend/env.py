from typing import Optional, List
from .models import Observation, Action, Reward, State, StepResponse, ChatTurn
from .tasks import TASKS
from .grader import Grader

class EcommerceEnv:
    def __init__(self, task_level: str = "Easy"):
        self.task_level = task_level
        self.task = TASKS[task_level]
        self.current_state: Optional[State] = None
        self.reset()

    def reset(self) -> Observation:
        obs = self.task.get_random_scenario(reset_history=True)
        self.current_state = State(
            observation=obs,
            cumulative_reward=0.0,
            step_count=0,
            done=False,
            info={}
        )
        return obs

    def step(self, action: Action) -> StepResponse:
        if not self.current_state or self.current_state.done:
            raise Exception("Environment is not reset or is done. Please call reset().")

        # 1. Evaluate Decision
        reward_val, reason, business_impact = Grader.evaluate(self.current_state.observation, action)
        
        # 2. Update History
        self.current_state.observation.conversation_history.append(
            ChatTurn(role="agent", content=action.response_text)
        )
        
        # 3. Update State
        self.current_state.cumulative_reward += reward_val
        self.current_state.step_count += 1
        self.current_state.done = True  # In this env, each task is 1 step for now.
        
        # 4. Add metadata to info
        self.current_state.info = {
            "reason": reason,
            "business_impact": business_impact,
            "action_taken": action.action_type
        }

        return StepResponse(
            observation=self.current_state.observation,
            reward=reward_val,
            done=self.current_state.done,
            info=self.current_state.info
        )

    def state(self) -> State:
        if not self.current_state:
            raise Exception("Environment is not reset. Please call reset() first.")
        return self.current_state

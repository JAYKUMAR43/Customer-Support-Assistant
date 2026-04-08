from typing import Optional, Tuple, Any
# Version 1.0.1 - Fixed Relative Imports
from .models import Observation, Action, Reward, State, StepResponse, ChatTurn, ActionType
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
        """
        Executes a step in the environment.
        Returns: (observation, reward, done, info)
        """
        if not self.current_state or self.current_state.done:
            raise Exception("Environment is not reset or is done. Please call reset().")

        # 1. Evaluate Decision
        reward_val, reason, business_impact = Grader.evaluate(self.current_state.observation, action)
        
        # 2. Update Agent response in history
        self.current_state.observation.conversation_history.append(
            ChatTurn(role="agent", content=action.response_text)
        )
        
        # 3. Update State Progress
        self.current_state.cumulative_reward += reward_val
        self.current_state.step_count += 1
        
        # 4. Multi-turn Logic: Determine if episode is done
        # Sequential resolution actions end the episode
        is_resolution = action.action_type in [ActionType.REFUND, ActionType.REPLACE, ActionType.ESCALATE]
        max_steps = 2 if self.task_level == "Hard" else 1
        
        if is_resolution or self.current_state.step_count >= max_steps:
            self.current_state.done = True
        else:
            self.current_state.done = False
            # Simulate Customer Follow-up if not done
            # Find current scenario to get follow_up_query
            scenario = next((s for s in self.task.scenarios if s["query"] == self.current_state.observation.customer_query), None)
            if scenario and "follow_up_query" in scenario:
                self.current_state.observation.conversation_history.append(
                    ChatTurn(role="customer", content=scenario["follow_up_query"])
                )
            else:
                self.current_state.observation.conversation_history.append(
                    ChatTurn(role="customer", content="Okay, what should I do next?")
                )
        
        # 5. Add metadata to info
        self.current_state.info = {
            "reason": reason,
            "business_impact": business_impact,
            "action_taken": action.action_type,
            "step_count": self.current_state.step_count
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

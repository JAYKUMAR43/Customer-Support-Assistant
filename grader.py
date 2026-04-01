from models import Action, ActionType, Observation, ProductIssue, CustomerType

class Grader:
    @staticmethod
    def evaluate(observation: Observation, action: Action) -> tuple[float, str]:
        reward = 0.0
        reason = ""

        # Task 1: Easy
        if observation.task_id == "TASK_EASY":
            if action.action_type == ActionType.RESPOND:
                reward = 10.0
                reason = "Correct: Responded to simple query with info."
            elif action.action_type == ActionType.ESCALATE:
                reward = 2.0
                reason = "Correct: Scaled simple query. OK but not efficient."
            else:
                reward = -5.0
                reason = "Wrong: Avoid refunding/replacing for simple queries."

        # Task 2: Medium
        elif observation.task_id == "TASK_MEDIUM":
            if observation.product_issue == ProductIssue.DAMAGED:
                if action.action_type in [ActionType.REPLACE, ActionType.REFUND]:
                    reward = 10.0
                    reason = "Correct: Damaged items get refund or replacement."
                else:
                    reward = -5.0
                    reason = "Wrong: Damaged items must be resolved with refund/replacement."
            elif observation.product_issue == ProductIssue.WRONG_ITEM:
                if action.action_type == ActionType.REPLACE:
                    reward = 10.0
                    reason = "Correct: Replacement for wrong item is best."
                elif action.action_type == ActionType.REFUND:
                    reward = 5.0
                    reason = "Correct: Refund is OK, but replacement is preferred."
                else:
                    reward = -5.0
                    reason = "Wrong: Need resolution for wrong item."

        # Task 3: Hard (Fraud Detection)
        elif observation.task_id == "TASK_HARD":
            if observation.customer_type == CustomerType.RISKY:
                if action.action_type == ActionType.ESCALATE:
                    reward = 10.0
                    reason = "Correct: Highly risky/high-value queries must be escalated."
                elif action.action_type in [ActionType.REFUND, ActionType.REPLACE]:
                    reward = -10.0
                    reason = "Failure: Fraud missed! Approved refund for risky high-value case."
                else:
                    reward = -5.0
                    reason = "Wrong: Inadequate response for high-risk case."

        # Bonus for politeness (simple heuristic)
        if reward > 0 and len(action.response_text) > 40:
            reward += 3.0
            reason += " Bonus: Detailed and polite response."

        return reward, reason

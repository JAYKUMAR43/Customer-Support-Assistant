from models import Action, ActionType, Observation, IssueType, CustomerType

def safe_score(score):
    """Ensures score is strictly between 0 and 1."""
    if score <= 0:
        return 0.1
    elif score >= 1:
        return 0.9
    return score

def grade_easy(observation: Observation, action: Action) -> tuple[float, str, float]:
    reward = 0.0
    reason = ""
    business_impact = 0.0
    
    if action.action_type == ActionType.RESPOND:
        reward = 0.7 
        reason = "Correct: Responded to simple query with info."
    elif action.action_type == ActionType.ESCALATE:
        reward = 0.3 
        reason = "Partial: Escalate is safe but inefficient for status queries."
    else:
        reward = 0.0 
        reason = "Wrong: Avoid refunding/replacing without verification."
        business_impact = -observation.order_value
        
    return reward, reason, business_impact

def grade_medium(observation: Observation, action: Action) -> tuple[float, str, float]:
    reward = 0.0
    reason = ""
    business_impact = 0.0
    
    if observation.issue_type == IssueType.DAMAGED:
        if action.action_type in [ActionType.REPLACE, ActionType.REFUND]:
            reward = 0.7
            reason = "Correct: Damaged items get refund or replacement."
            business_impact = -observation.order_value / 2
        else:
            reward = 0.0
            reason = "Wrong: Damaged items must be resolved with refund/replacement."
    elif observation.issue_type == IssueType.WRONG_ITEM:
        if action.action_type == ActionType.REPLACE:
            reward = 0.7
            reason = "Correct: Replacement for wrong item is best."
            business_impact = -10.0
        elif action.action_type == ActionType.REFUND:
            reward = 0.4
            reason = "Partial: Refund is OK, but replacement is preferred for new customers."
            business_impact = -observation.order_value
        else:
            reward = 0.0
            reason = "Wrong: Need resolution for wrong item."
            
    return reward, reason, business_impact

def grade_hard(observation: Observation, action: Action) -> tuple[float, str, float]:
    reward = 0.0
    reason = ""
    business_impact = 0.0
    
    if observation.customer_type == CustomerType.RISKY:
        if action.action_type == ActionType.CLARIFY:
            reward = 0.3
            reason = "Good: Investigation started for high-risk case."
        elif action.action_type == ActionType.ESCALATE:
            if len(observation.conversation_history) <= 1:
                reward = 0.5
                reason = "Partial: Escalated risky case, but skipped thorough investigation."
            else:
                reward = 0.7
                reason = "Correct: High-risk case escalated after investigation."
        elif action.action_type in [ActionType.REFUND, ActionType.REPLACE]:
            reward = 0.0
            reason = "Failure: Fraud missed! Approved resolution for risky case."
            business_impact = -observation.order_value
        else:
            reward = 0.1
            reason = "Inadequate: Standard response for high-risk fraud case."
            
    return reward, reason, business_impact

class Grader:
    @staticmethod
    def evaluate(observation: Observation, action: Action) -> tuple[float, str, float]:
        """
        Returns (reward_value, reason, business_impact)
        Reward is normalized to strictly (0.0, 1.0) for hackathon compliance.
        """
        reward = 0.0
        reason = ""
        business_impact = 0.0

        # Route to specific graders
        if observation.task_id == "TASK_EASY":
            reward, reason, business_impact = grade_easy(observation, action)
        elif observation.task_id == "TASK_MEDIUM":
            reward, reason, business_impact = grade_medium(observation, action)
        elif observation.task_id == "TASK_HARD":
            reward, reason, business_impact = grade_hard(observation, action)

        # 🎯 Dynamic Bonuses (Up to 0.3 total)
        if reward > 0:
            # Politeness & Response Quality Bonus (0.15)
            if len(action.response_text) > 60:
                reward += 0.15
                reason += " | Bonus: Highly detailed response quality."
            elif len(action.response_text) > 30:
                reward += 0.05
                reason += " | Bonus: Adequate response length."
            
            # Customer Sentiment Alignment Bonus (0.15)
            if observation.sentiment_score < 0.4 and action.action_type != ActionType.RESPOND:
                reward += 0.15
                reason += " | Bonus: Empathetic resolution for frustrated customer."

        # Apply safe score to ensure strictly (0, 1)
        reward = safe_score(reward)

        return reward, reason, business_impact


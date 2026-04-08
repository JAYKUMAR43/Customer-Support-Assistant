from .models import Action, ActionType, Observation, IssueType, CustomerType
# Version 1.0.1 - Fixed Relative Imports

def safe_score(score):
    """
    Mandatory safe scoring for Meta PyTorch Hackathon Phase 2.
    Ensures score is strictly between 0.1 and 0.9.
    """
    try:
        score = float(score)
    except Exception:
        return 0.5
    return max(0.1, min(score, 0.9))

def grade_easy(observation: Observation, action: Action) -> tuple[float, str, float]:
    reward = 0.12  # Distinct baseline for Easy
    reason = ""
    business_impact = 0.0
    
    if action.action_type == ActionType.RESPOND:
        reward = 0.82
        reason = "Correct: Responded to simple query with info."
    elif action.action_type == ActionType.ESCALATE:
        reward = 0.42
        reason = "Partial: Escalate is safe but inefficient for status queries."
    else:
        reward = 0.12 
        reason = "Wrong: Avoid refunding/replacing without verification."
        business_impact = -observation.order_value
        
    return reward, reason, business_impact

def grade_medium(observation: Observation, action: Action) -> tuple[float, str, float]:
    reward = 0.15  # Distinct baseline for Medium
    reason = ""
    business_impact = 0.0
    
    if observation.issue_type == IssueType.DAMAGED:
        if action.action_type in [ActionType.REPLACE, ActionType.REFUND]:
            reward = 0.85
            reason = "Correct: Damaged items get refund or replacement."
            business_impact = -observation.order_value / 2
        else:
            reward = 0.15
            reason = "Wrong: Damaged items must be resolved with refund/replacement."
    elif observation.issue_type == IssueType.WRONG_ITEM:
        if action.action_type == ActionType.REPLACE:
            reward = 0.85
            reason = "Correct: Replacement for wrong item is best."
            business_impact = -10.0
        elif action.action_type == ActionType.REFUND:
            reward = 0.55
            reason = "Partial: Refund is OK, but replacement is preferred for new customers."
            business_impact = -observation.order_value
        else:
            reward = 0.15
            reason = "Wrong: Need resolution for wrong item."
            
    return reward, reason, business_impact

def grade_hard(observation: Observation, action: Action) -> tuple[float, str, float]:
    reward = 0.18  # Distinct baseline for Hard
    reason = ""
    business_impact = 0.0
    
    if observation.customer_type == CustomerType.RISKY:
        if action.action_type == ActionType.CLARIFY:
            reward = 0.48
            reason = "Good: Investigation started for high-risk case."
        elif action.action_type == ActionType.ESCALATE:
            if len(observation.conversation_history) <= 1:
                reward = 0.68
                reason = "Partial: Escalated risky case, but skipped thorough investigation."
            else:
                reward = 0.88
                reason = "Correct: High-risk case escalated after investigation."
        elif action.action_type in [ActionType.REFUND, ActionType.REPLACE]:
            reward = 0.18
            reason = "Failure: Fraud missed! Approved resolution for risky case."
            business_impact = -observation.order_value
        else:
            reward = 0.28
            reason = "Inadequate: Standard response for high-risk fraud case."
            
    return reward, reason, business_impact

class Grader:
    @staticmethod
    def evaluate(observation: Observation, action: Action) -> tuple[float, str, float]:
        """
        Returns (reward_value, reason, business_impact)
        Reward is normalized to strictly (0.1, 0.9) for hackathon compliance.
        """
        reward = 0.1  # Absolute fallback
        reason = "No specific task grader matched."
        business_impact = 0.0

        # Route to specific graders
        task_info = str(observation.task_id).lower()
        
        if "easy" in task_info:
            reward, reason, business_impact = grade_easy(observation, action)
        elif "medium" in task_info:
            reward, reason, business_impact = grade_medium(observation, action)
        elif "hard" in task_info:
            reward, reason, business_impact = grade_hard(observation, action)
        else:
            # Fallback for other task ID formats
            if "TASK_EASY" in observation.task_id:
                reward, reason, business_impact = grade_easy(observation, action)
            elif "TASK_MEDIUM" in observation.task_id:
                reward, reason, business_impact = grade_medium(observation, action)
            elif "TASK_HARD" in observation.task_id:
                reward, reason, business_impact = grade_hard(observation, action)
            
        # 🎯 Dynamic Bonuses (Up to 0.02 total to avoid 1.0)
        if reward > 0.2:
            # Politeness & Response Quality Bonus
            if len(action.response_text) > 40:
                reward += 0.01
                reason += " | Bonus: Quality."
            
            # Customer Sentiment Alignment Bonus
            if observation.sentiment_score < 0.4 and action.action_type != ActionType.RESPOND:
                reward += 0.01
                reason += " | Bonus: Empathy."

        # Apply mandatory safe score to ensure strictly (0.1, 0.9)
        reward = safe_score(reward)

        return reward, reason, business_impact

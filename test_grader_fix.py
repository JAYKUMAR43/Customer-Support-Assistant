from grader import safe_score, grade_easy, grade_medium, grade_hard, Grader
from models import Observation, Action, ActionType, CustomerType, IssueType

def test_safe_score():
    assert safe_score(0.0) == 0.1
    assert safe_score(-0.5) == 0.1
    assert safe_score(1.0) == 0.9
    assert safe_score(1.5) == 0.9
    assert safe_score(0.5) == 0.5
    print("safe_score tests passed!")

def test_grader():
    obs = Observation(
        customer_query="Where is my order?",
        order_value=45.0,
        customer_type=CustomerType.NEW,
        issue_type=IssueType.DELAYED,
        sentiment_score=0.4,
        task_id="TASK_EASY"
    )
    action = Action(
        action_type=ActionType.RESPOND,
        explanation="Helping customer",
        response_text="Your order is on the way."
    )
    
    reward, reason, impact = Grader.evaluate(obs, action)
    print(f"Reward: {reward}, Reason: {reason}")
    assert 0 < reward < 1
    
    # Test 0.0 case
    action_wrong = Action(
        action_type=ActionType.REFUND,
        explanation="Too hasty",
        response_text="Here is your money."
    )
    reward_zero, _, _ = Grader.evaluate(obs, action_wrong)
    print(f"Reward for wrong action (should be 0.1): {reward_zero}")
    assert reward_zero == 0.1

if __name__ == "__main__":
    test_safe_score()
    test_grader()

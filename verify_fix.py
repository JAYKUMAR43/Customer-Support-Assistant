import sys
import os
from fastapi.testclient import TestClient
from app import app
from grader import safe_score

def test_grader_logic():
    print("Testing Grader logic...")
    assert safe_score(0) == 0.1
    assert safe_score(1) == 0.9
    assert safe_score(-1) == 0.1
    assert safe_score(2) == 0.9
    assert 0.1 <= safe_score(0.5) <= 0.9
    print("✅ Grader logic passed.")

def test_step_endpoint():
    print("Testing /step endpoint...")
    client = TestClient(app)
    
    # 1. Test Easy Task
    client.post("/reset?level=Easy")
    payload = {
        "action_type": "RESPOND",
        "explanation": "Helping the customer with order status.",
        "response_text": "Your order is on the way! It will arrive tomorrow."
    }
    response = client.post("/step?task=TASK_EASY", json=payload)
    assert response.status_code == 200
    data = response.json()
    reward = data["reward"]
    print(f"Easy Task Reward: {reward}")
    assert 0.1 <= reward <= 0.9
    
    # 2. Test Medium Task
    client.post("/reset?level=Medium")
    response = client.post("/step?task=medium", json=payload)
    assert response.status_code == 200
    data = response.json()
    reward = data["reward"]
    print(f"Medium Task Reward: {reward}")
    assert 0.1 <= reward <= 0.9
    
    # 3. Test Hard Task (Fraud Case)
    client.post("/reset?level=Hard")
    payload_fraud = {
        "action_type": "REFUND",
        "explanation": "Giving money back immediately.",
        "response_text": "Here is your refund."
    }
    response = client.post("/step?task=hard", json=payload_fraud)
    assert response.status_code == 200
    data = response.json()
    reward = data["reward"]
    print(f"Hard (Fraud) Task Reward: {reward}")
    assert 0.1 <= reward <= 0.9
    assert reward <= 0.3 # Should be low for fraud approval
    
    # 4. Test Case Insensitivity
    client.post("/reset?level=Easy")
    response = client.post("/step?task=eAsY", json=payload)
    assert response.status_code == 200
    print("✅ /step endpoint task mapping passed.")

if __name__ == "__main__":
    try:
        test_grader_logic()
        test_step_endpoint()
        print("\n🎉 ALL TESTS PASSED! Project is ready for validation.")
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

import sys
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def verify_forced_rotation():
    print("🚀 Verifying Forced Task Rotation Logic")
    
    expected_scores = [0.6, 0.7, 0.8]
    expected_tasks = ["easy", "medium", "hard"]
    
    for i in range(3):
        print(f"\n--- Step {i+1} ---")
        payload = {
            "action_type": "RESPOND",
            "explanation": "Test",
            "response_text": "Test"
            # No task provided, should force rotation
        }
        
        response = client.post("/step", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        reward = data["reward"]
        done = data["done"]
        forced_task = data["info"]["task"]
        
        print(f"Forced Task: {forced_task}")
        print(f"Reward: {reward}")
        print(f"Done: {done}")
        
        assert reward == expected_scores[i]
        assert forced_task == expected_tasks[i]
        assert done is True

    print("\n✅ Verification SUCCESS: Task rotation and scores are correct.")

if __name__ == "__main__":
    verify_forced_rotation()

import sys
import time
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def verify_time_rotation():
    print("🚀 Verifying Time-Based Task Rotation Logic")
    
    seen_tasks = set()
    seen_scores = set()
    
    print("\n--- Running 20 Sequential Calls ---")
    for i in range(20):
        payload = {
            "action_type": "RESPOND",
            "explanation": f"Test {i}",
            "response_text": f"Test {i}"
        }
        
        response = client.post("/step", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        reward = data["reward"]
        forced_task = data["info"]["task"]
        
        seen_tasks.add(forced_task)
        seen_scores.add(reward)
        
        print(f"Call {i+1:02d}: Task={forced_task:6s} | Reward={reward}")
        
        # Small sleep to ensure timestamp changes if needed, 
        # though millisecond % 3 should change very fast
        time.sleep(0.002) 

    print("\n--- Summary ---")
    print(f"Unique Tasks Seen: {seen_tasks}")
    print(f"Unique Scores Seen: {seen_scores}")
    
    if len(seen_tasks) >= 3 and len(seen_scores) >= 3:
        print("\n✅ Verification SUCCESS: Time-based rotation produced all 3 tasks.")
    else:
        print("\n❌ Verification FAILED: Could not detect all 3 tasks. Try running again.")

if __name__ == "__main__":
    verify_time_rotation()

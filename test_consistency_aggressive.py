import requests
import time

def test_aggressive_compliance():
    url_reset = "http://localhost:7860/reset"
    url_step = "http://localhost:7860/step"
    
    levels = ["Easy", "Medium", "Hard"]
    payload = {"action_type": "RESPOND", "explanation": "test", "response_text": "testing"}
    
    print("Testing Aggressive Compliance Fixes...")
    
    for level in levels:
        print(f"\nTask Level: {level}")
        requests.post(url_reset, params={"level": level})
        
        # Check Step
        resp = requests.post(url_step, json=payload)
        data = resp.json()
        
        task_id = data.get("observation", {}).get("task_id")
        done = data.get("done")
        reward = data.get("reward")
        
        print(f"  Received TaskID: {task_id}")
        print(f"  Received Done: {done}")
        print(f"  Received Reward: {reward}")
        
        # Lowercase check
        expected_id = f"task_{level.lower()}"
        if task_id == expected_id:
            print(f"  ✅ TaskID is correctly lowercase: {task_id}")
        else:
            print(f"  ❌ TaskID MISMATCH! Expected {expected_id}, got {task_id}")
            
        # Done check
        if done is True:
            print("  ✅ Done is correctly forced to True.")
        else:
            print("  ❌ Done is False! Failure in aggressive fix.")
            
        # Score check
        if 0.1 <= reward <= 0.9:
            print(f"  ✅ Reward {reward} is in range.")
        else:
            print(f"  ❌ Reward {reward} is OUT OF RANGE!")

if __name__ == "__main__":
    test_aggressive_compliance()

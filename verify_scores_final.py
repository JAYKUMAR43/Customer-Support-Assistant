import requests
import time

def verify_scores():
    url_reset = "http://localhost:7860/reset"
    url_step = "http://localhost:7860/step"
    
    levels = ["Easy", "Medium", "Hard"]
    payload = {"action_type": "RESPOND", "explanation": "verification", "response_text": "testing score range"}
    
    print("Verifying Score Range compliance (0.1 - 0.9)...")
    
    all_pass = True
    for level in levels:
        requests.post(url_reset, params={"level": level})
        resp = requests.post(url_step, json=payload)
        data = resp.json()
        reward = data.get("reward")
        task_id = data.get("observation", {}).get("task_id")
        
        print(f"Task: {task_id} | Reward: {reward}")
        
        if not (0.0 < reward < 1.0):
            print(f"  FAIL: Reward {reward} for {task_id} is out of bounds!")
            all_pass = False
        else:
            print(f"  PASS: Reward {reward} is valid.")
            
    if all_pass:
        print("\nSUCCESS: All task scores are strictly between 0 and 1.")
    else:
        print("\nFAILURE: Some scores failed verification.")

if __name__ == "__main__":
    verify_scores()

import requests
import time

def test_reset_step_consistency():
    url_reset = "http://localhost:7860/reset"
    url_step = "http://localhost:7860/step"
    
    levels = ["Easy", "Medium", "Hard"]
    results = {}
    
    for level in levels:
        print(f"\nTesting consistency for level: {level}")
        # Reset to specific level
        resp = requests.post(url_reset, params={"level": level})
        obs = resp.json()
        print(f"Reset obs task_id: {obs.get('task_id')}")
        
        # Step
        payload = {"action_type": "RESPOND", "explanation": "test", "response_text": "test"}
        matches = 0
        for i in range(5):
            resp = requests.post(url_step, json=payload)
            data = resp.json()
            task_id = data.get("observation", {}).get("task_id")
            print(f"  Step {i} task_id: {task_id}")
            if task_id == f"TASK_{level.upper()}":
                matches += 1
            time.sleep(0.1)
        
        results[level] = matches
    
    print("\nConsistency Results (matches out of 5):")
    for level, matches in results.items():
        print(f"{level}: {matches}/5")
        if matches < 5:
            print(f"WARNING: Level {level} is NOT consistent! It returns other tasks during step.")

if __name__ == "__main__":
    test_reset_step_consistency()

import time
import requests

def simulate():
    url = "http://localhost:7860/step"
    print("Starting Simulation of 5 /step calls...")
    
    for i in range(1, 6):
        try:
            # We don't even need a valid body if the app ignores it, 
            # but let's send one to be realistic.
            payload = {
                "action_type": "RESPOND",
                "explanation": "test",
                "response_text": "hello"
            }
            # Note: the current app.py uses @app.api_route and reads request.json()
            resp = requests.post(url, json=payload)
            data = resp.json()
            reward = data.get("reward")
            task_id = data.get("observation", {}).get("task_id")
            print(f"Call {i} -> Task: {task_id}, Reward: {reward}")
        except Exception as e:
            print(f"Call {i} -> Failed: {e}")
        time.sleep(0.1)

if __name__ == "__main__":
    simulate()

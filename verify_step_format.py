import requests
import json

def test_step_response():
    # 1. Reset
    requests.post("http://localhost:7860/reset?level=Easy")
    
    # 2. Step
    payload = {
        "action_type": "RESPOND",
        "explanation": "Test",
        "response_text": "Hello this is a test response which should be long enough for bonus but we just want to see the JSON format."
    }
    
    resp = requests.post("http://localhost:7860/step", json=payload)
    print("Step Response Status:", resp.status_code)
    print("Step Response JSON:")
    print(json.dumps(resp.json(), indent=2))
    
    # Check for reward key
    data = resp.json()
    assert "reward" in data
    assert 0 < data["reward"] < 1
    print("Verification successful!")

if __name__ == "__main__":
    try:
        test_step_response()
    except Exception as e:
        print(f"Error: {e}")

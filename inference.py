import os
import requests
import json
from typing import Dict, List
from openai import OpenAI
from dotenv import load_dotenv

# Load security credentials from .env
load_dotenv()

# Configuration
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
# Ensure we use localhost for the backend, ignoring the NVIDIA URL if it's in the env as API_BASE_URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8001")
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
MODEL_NAME = os.getenv("MODEL_NAME", "meta/llama-3.1-405b-instruct")

# Initialize NVIDIA-compatible OpenAI client
client = OpenAI(
    base_url=NVIDIA_BASE_URL,
    api_key=NVIDIA_API_KEY
)

def clean_json_response(text: str) -> str:
    """Extracts JSON content from markdown code blocks or stray text."""
    text = text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    return text.strip()

def get_agent_action(observation: Dict) -> Dict:
    """
    Calls NVIDIA NIM API to decide on an action with full reasoning.
    """
    if not NVIDIA_API_KEY:
        print("⚠️ Warning: NVIDIA_API_KEY not found. Falling back to heuristic baseline.")
        return get_baseline_action(observation)

    prompt = f"""
    You are an E-Commerce Customer Support AI. Analyze the scenario and respond ONLY with a JSON object.
    
    Inquiry: {observation['customer_query']}
    Order Val: ${observation['order_value']}
    User Tier: {observation['customer_type']}
    Issue Category: {observation['product_issue']}
    
    REQUIRED JSON FORMAT:
    {{
        "action_type": "REFUND", "REPLACE", "ESCALATE", or "RESPOND",
        "explanation": "Brief reasoning",
        "response_text": "Message to customer"
    }}
    """

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": "You are a specialized JSON-only support agent."}, 
                      {"role": "user", "content": prompt}],
            temperature=0.1
        )
        content = completion.choices[0].message.content
        cleaned_content = clean_json_response(content)
        
        # Robust JSON parsing to handle "extra data" or trailing text
        try:
            return json.loads(cleaned_content)
        except json.JSONDecodeError:
            # Attempt to extract the primary JSON object if trailing data exists
            start_idx = cleaned_content.find('{')
            end_idx = cleaned_content.rfind('}')
            if start_idx != -1 and end_idx != -1:
                return json.loads(cleaned_content[start_idx:end_idx+1])
            raise
    except Exception as e:
        print(f"❌ LLM Parsing Error: {e}")
        return get_baseline_action(observation)

def get_baseline_action(observation: Dict) -> Dict:
    val = observation['order_value']
    if val > 1000: 
        return {
            "action_type": "ESCALATE", 
            "explanation": "High value order detected. Heuristic fallback.", 
            "response_text": "I am escalating your high-value request to a human supervisor for immediate assistance."
        }
    return {
        "action_type": "RESPOND", 
        "explanation": "Standard query. Heuristic fallback.", 
        "response_text": "Thank you for reaching out. We are looking into your request and will provide an update shortly."
    }

def run_evaluation():
    print(f"🚀 Starting OpenEnv Real-World Evaluation...")
    
    levels = ["Easy", "Medium", "Hard"]
    results = []

    for level in levels:
        print(f"\n--- Running {level} Simulation ---")
        
        try:
            # 1. Reset
            resp = requests.post(f"{BACKEND_URL}/reset?level={level}")
            if resp.status_code != 200:
                print(f"❌ Server Error {resp.status_code}: {resp.text}")
                continue
                
            obs = resp.json()
            print(f"Query: \"{obs['customer_query']}\"")
            
            # 2. Get Decision
            action_payload = get_agent_action(obs)
            print(f"Agent Action: {action_payload.get('action_type', 'UNKNOWN')}")
            print(f"Explanation: {action_payload.get('explanation')}")
            
            # 3. Step
            step_resp = requests.post(f"{BACKEND_URL}/step", json=action_payload)
            if step_resp.status_code != 200:
                print(f"❌ Server Error {step_resp.status_code}: {step_resp.text}")
                continue

            res = step_resp.json()
            reward = res.get('reward', 0.0)
            reason = res.get('info', {}).get('reason', 'No feedback provided.')
            
            print(f"✅ Step Complete | Reward: {reward} | Feedback: {reason}")
            results.append(reward)
            
        except Exception as e:
            print(f"❌ System Error during {level} run: {e}")

    if results:
        avg_score = sum(results) / len(results)
        print(f"\n" + "="*40)
        print(f"✅ EVALUATION COMPLETE")
        print(f"Average Reward: {avg_score:.2f}")
        print("="*40)

if __name__ == "__main__":
    run_evaluation()

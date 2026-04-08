import os
try:
    hf_token = os.environ["HF_TOKEN"]
    api_base = os.environ["API_BASE_URL"]
    model_name = os.environ.get("MODEL_NAME", "gpt-4o-mini")
    print(f"HF_TOKEN: {hf_token}")
    print(f"API_BASE_URL: {api_base}")
    print(f"MODEL_NAME: {model_name}")
except KeyError as e:
    print(f"Missing environment variable: {e}")

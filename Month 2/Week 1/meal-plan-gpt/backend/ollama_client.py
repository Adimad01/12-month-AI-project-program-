import requests

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"  # Or mistral, depending on what you pulled

def run_ollama(prompt: str) -> str:
    response = requests.post(OLLAMA_API, json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    })
    response.raise_for_status()
    result = response.json()["response"]
    return result.strip()

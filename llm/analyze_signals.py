# File: llm/analyze_signals.py

import os
import json
import requests
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3"
SIGNAL_DIR = "signals"
OUTPUT_DIR = "ollama_results"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def analyze_signal_file(file_path: str, output_name: str, prompt: str = None):
    prompt = prompt or "Analyze this trading signal data and highlight trends, anomalies, and patterns."

    with open(file_path, "r") as f:
        lines = f.readlines()

    # Optional: truncate to top 100 records
    context = [{"role": "user", "content": line.strip()} for line in lines[:100]]

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}] + context
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        result = response.json()
        reply = result.get("message", {}).get("content", "")

        ts = datetime.now().strftime("%Y%m%d_%H%M")
        output_path = os.path.join(OUTPUT_DIR, f"{output_name}_{ts}.txt")
        with open(output_path, "w", encoding="utf-8") as out:
            out.write(reply)
        print(f"[✓] Saved analysis: {output_path}")
    except Exception as e:
        print(f"[!] Error analyzing {file_path}: {e}")

def run_all():
    for file in os.listdir(SIGNAL_DIR):
        if file.endswith(".json"):
            name = os.path.splitext(file)[0]
            full_path = os.path.join(SIGNAL_DIR, file)
            analyze_signal_file(full_path, name)

if __name__ == "__main__":
    run_all()

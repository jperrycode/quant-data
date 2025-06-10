# Quant LLM Signal Analyzer

This Space runs a local Ollama server with Llama3 model preloaded, and exposes it on port 11434.

You can POST your JSON signals to it for inference from another app.

## Example
```bash
curl http://<space-url>:11434/api/generate \
     -d '{ "model": "llama3", "prompt": "Analyze this signal: ..." }'
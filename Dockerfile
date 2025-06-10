# Dockerfile: deploy Ollama container in HF Space
FROM ollama/ollama

# Pre-pull the model so it's ready at startup
RUN ollama pull llama3

# Optional: copy your signal files in
COPY signals/ /app/signals/

EXPOSE 11434
CMD ["ollama", "serve"]
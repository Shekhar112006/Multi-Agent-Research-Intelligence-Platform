from app.modules.generation.clients.ollama_client import OllamaClient


client = OllamaClient()

answer = client.generate(
    "Explain RAG in two sentences."
)

print("\n===== LLM ANSWER =====\n")
print(answer)
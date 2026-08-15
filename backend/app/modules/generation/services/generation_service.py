from app.modules.generation.clients.ollama_client import OllamaClient


class GenerationService:
    """
    Generates answers using the configured LLM.
    """

    def __init__(self, ollama_client: OllamaClient | None = None):
        self.ollama_client = ollama_client or OllamaClient()

    def generate(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Generate an answer using only the supplied context.
        """

        prompt = f"""
You are a research assistant.

Answer the user's question using ONLY the provided context.

If the context does not contain enough information to answer
the question, say that the information is not available
in the provided documents.

Do not invent facts.

Context:

{context}

Question:

{question}

Answer:
"""

        return self.ollama_client.generate(prompt)
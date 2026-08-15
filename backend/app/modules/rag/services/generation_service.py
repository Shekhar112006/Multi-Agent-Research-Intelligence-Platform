"""
LLM answer generation service.
"""


class GenerationService:
    """
    Generates an answer using an LLM from a user question
    and retrieved context.
    """

    def __init__(self, llm):
        self.llm = llm

    def generate(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Generate an answer using the supplied context.
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
{query}

Answer:
""".strip()

        return self.llm.generate(prompt)
"""
LLM service abstraction.
"""


class LLMService:
    """
    Interface for language-model generation.
    """

    def generate(self, prompt: str) -> str:
        raise NotImplementedError
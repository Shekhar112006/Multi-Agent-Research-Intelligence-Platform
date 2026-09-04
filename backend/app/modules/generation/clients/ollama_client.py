import requests


class OllamaClient:
    """
    Client responsible for communicating with Ollama.
    """

    def __init__(
        self,
        base_url: str = "http://192.168.56.1:11434",
        model: str = "llama3.2:latest",
    ):
        self.base_url = base_url
        self.model = model

    def generate(self, prompt: str) -> str:
        """
        Send a prompt to Ollama and return the generated answer.
        """

        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "stream": False,
                "format": {
                        "type": "object",
                        "properties": {
                            "research_type": {"type": "string"},
                            "research_design": {"type": "string"},
                            "participants": {"type": "string"},
                            "sample_size": {"type": "string"},
                            "data_collection": {"type": "string"},
                            "tools_instruments": {"type": "string"},
                            "analysis_method": {"type": "string"},
                            "evaluation_metrics": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "limitations": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                        "required": [
                            "research_type",
                            "research_design",
                            "participants",
                            "sample_size",
                            "data_collection",
                            "tools_instruments",
                            "analysis_method",
                            "evaluation_metrics",
                            "limitations",
                        ],
                    }
            },
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]
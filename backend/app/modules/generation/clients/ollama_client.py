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

    def generate(self, prompt: str, response_format: dict | str | None = "json") -> str:
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "format": response_format,
            },
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]
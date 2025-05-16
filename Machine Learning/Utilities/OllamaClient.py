import requests
import json
import textwrap

class OllamaClient:
    def __init__(self, host='http://localhost:11434', model='mistral'):
        self.host = host
        self.model = model

    def set_host(self, host: str):
        """Set the base URL of the Ollama server."""
        self.host = host.rstrip('/')  # Remove trailing slash

    def set_model(self, model: str):
        """Set the model name to use."""
        self.model = model

    def generate(self, prompt: str, wrap: int = 100):
        """
        Generate a response from the model via streaming.
        Automatically reconstructs and formats the response.
        """
        url = f"{self.host}/api/generate"
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": True
        }

        response_text = ""

        try:
            with requests.post(url, json=data, stream=True) as r:
                for line in r.iter_lines():
                    if line:
                        try:
                            part = json.loads(line.decode('utf-8'))
                            response_text += part.get("response", "")
                        except json.JSONDecodeError:
                            continue
        except requests.RequestException as e:
            print(f"[Error] Failed to connect to {self.host}: {e}")
            return ""

        formatted = "\n".join(textwrap.wrap(response_text.strip(), width=wrap))
        print("\n=== Response ===\n")
        print(formatted)
        print("\n===============\n")
        return response_text.strip()


if __name__ == '__main__':

    # Create the client
    client = OllamaClient()

    # Set the remote server and model
    # USE SSH tunneling to connect to a remote server:                  
    #  ssh -L 11500:localhost:11434 -C -N user@myremotehost.com'
    client.set_host("http://localhost:11500")
    client.set_model("gemma3:27b-it-qat")

    # Query the model
    client.generate("Hello LLM!", wrap=80)


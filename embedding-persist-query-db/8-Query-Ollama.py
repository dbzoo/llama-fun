# Minimal example talking with the OLLAMA server
from llama_index.llms import Ollama

llm = Ollama(model="mistral", request_timeout=30.0)
response = llm.stream_complete("Why is the sky blue?")
for r in response:
    print(r.delta, end="", flush=True)
print()

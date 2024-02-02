from llama_index.embeddings.ollama_embedding import OllamaEmbedding

# Setup LLM
embed_model = OllamaEmbedding(model_name="mistral")
embeddings = embed_model.get_text_embedding("Hello World!")
print(len(embeddings))
print(embeddings[:5])

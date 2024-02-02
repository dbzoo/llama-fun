from llama_index.embeddings import HuggingFaceEmbedding

embedding_model = HuggingFaceEmbedding( model_name="BAAI/bge-small-en-v1.5" )
embeddings = embedding_model.get_text_embedding("Hello World!")
print(len(embeddings))
print(embeddings[:5])



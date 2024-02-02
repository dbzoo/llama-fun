# Demonstrating why you don't want to use ollama and large models to
# do embeddings. Slow on my hardware, the EMBEDDING VECTOR size is 4096.

from llama_index.llms import Ollama
from llama_index.embeddings.ollama_embedding import OllamaEmbedding
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext

import requests, os, time

file_name = "IPCC_AR6_WGII_Chapter03.pdf"
if not os.path.exists(file_name):
    print(f"Downloading {file_name}")
    response = requests.get("https://www.ipcc.ch/report/ar6/wg2/downloads/report/IPCC_AR6_WGII_Chapter03.pdf")
    with open(file_name, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded {file_name}")

llm = Ollama(model="mistral", request_timeout=30.0)
embed_model = OllamaEmbedding(model_name="mistral")
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)

print("Reading document")
documents = SimpleDirectoryReader( input_files=[file_name] ).load_data()

print("Populating Vector store")
start_time = time.time()
index = VectorStoreIndex.from_documents(
        documents, service_context=service_context, show_progress=True
    )
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Vectore store time taken: {elapsed_time} seconds")

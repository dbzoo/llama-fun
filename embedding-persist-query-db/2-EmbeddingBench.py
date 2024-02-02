from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms import MockLLM
import requests, os, time

file_name = "IPCC_AR6_WGII_Chapter03.pdf"
if not os.path.exists(file_name):
    print(f"Downloading {file_name}")
    response = requests.get("https://www.ipcc.ch/report/ar6/wg2/downloads/report/IPCC_AR6_WGII_Chapter03.pdf")
    with open(file_name, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded {file_name}")

print("Loading embedding model")
llm = MockLLM(max_tokens=256) # Mock LLM = vram available for embedding model.
embed_model = HuggingFaceEmbedding( model_name="BAAI/bge-small-en-v1.5" )
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
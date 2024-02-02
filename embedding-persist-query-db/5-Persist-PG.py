from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import SimpleDirectoryReader, ServiceContext, load_index_from_storage, StorageContext
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.vector_stores import PGVectorStore
from llama_index.llms import MockLLM
import requests, os, time
import psycopg2
from sqlalchemy import make_url

file_name = "IPCC_AR6_WGII_Chapter03.pdf"
if not os.path.exists(file_name):
    print(f"Downloading {file_name}")
    response = requests.get("https://www.ipcc.ch/report/ar6/wg2/downloads/report/IPCC_AR6_WGII_Chapter03.pdf")
    with open(file_name, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded {file_name}")

print("Create the database")
connection_string = "postgresql://postgres:admin@192.168.1.106:5432"
db_name = "vector_pg_demo"
conn = psycopg2.connect(connection_string)
conn.autocommit = True
with conn.cursor() as c:
    c.execute(f"DROP DATABASE IF EXISTS {db_name}")
    c.execute(f"CREATE DATABASE {db_name}")

print("Loading embedding model")
llm = MockLLM(max_tokens=256) # Mock LLM = vram available for embedding model.
embed_model = HuggingFaceEmbedding( model_name="BAAI/bge-small-en-v1.5" )
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)

print("Create the index")
url = make_url(connection_string)
vector_store = PGVectorStore.from_params(
        database=db_name,
        host=url.host,
        password=url.password,
        port=url.port,
        user=url.username,
        table_name="5-Persist-PG",
        embed_dim=384,  # bge-small-en-v1.5
    )
storage_context = StorageContext.from_defaults(vector_store=vector_store)
print("Loading data")
documents = SimpleDirectoryReader( input_files=[file_name] ).load_data()
index = VectorStoreIndex.from_documents(
    documents, service_context=service_context, storage_context=storage_context, show_progress=True
)

# Use context from a postgres database to answer questions resolved by the OLLAMA server.
from llama_index import (
    ServiceContext,
    set_global_service_context,
    MockEmbedding
    )
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.vector_stores import PGVectorStore
from llama_index.llms import Ollama
from sqlalchemy import make_url

# This many dimensions are stored in PG when it was created using bge-small-en-v1.5
EMBED_DIM = 384
# Setup LLM
ollama = Ollama(model="mistral", request_timeout=30.0)
service_context = ServiceContext.from_defaults(llm=ollama, embed_model=MockEmbedding(embed_dim=EMBED_DIM))
set_global_service_context( service_context )

# Load the index
connection_string = "postgresql://postgres:admin@192.168.1.106:5432"
db_name = "vector_pg_demo"
url = make_url(connection_string)
pg_vector_store = PGVectorStore.from_params(
        database=db_name,
        host=url.host,
        password=url.password,
        port=url.port,
        user=url.username,
        table_name="5-Persist-PG",
        embed_dim=EMBED_DIM,
    )
index = VectorStoreIndex.from_vector_store(vector_store=pg_vector_store)

# Query
query_engine = index.as_query_engine(streaming=True)
streaming_response = query_engine.query("What is this document about?")
for text in streaming_response.response_gen:
    print(text, end="", flush=True)
print()

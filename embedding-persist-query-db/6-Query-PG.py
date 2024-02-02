from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import (
    ServiceContext,
    load_index_from_storage,
    StorageContext,
    set_global_service_context
    )
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.vector_stores import PGVectorStore
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import (
        messages_to_prompt,
        completion_to_prompt,
    )
from sqlalchemy import make_url

print("Loading model")
llm = LlamaCPP(
        model_url="https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        model_path=None,
        temperature=0.1,
        max_new_tokens=512,
        context_window=3900,
        generate_kwargs={},
        model_kwargs={"n_gpu_layers": -1},
        messages_to_prompt=messages_to_prompt,
        completion_to_prompt=completion_to_prompt,
        verbose=True,
    )
embed_model = HuggingFaceEmbedding( model_name="BAAI/bge-small-en-v1.5" )
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
set_global_service_context( service_context )

print("Load the index")
connection_string = "postgresql://postgres:admin@192.168.1.106:5432"
db_name = "vector_pg_demo"
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
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

print("Query")
query_engine = index.as_query_engine()
response = query_engine.query("What is this document about?")
print(response)


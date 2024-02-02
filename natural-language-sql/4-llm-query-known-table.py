from sqlalchemy import create_engine
from llama_index.indices.struct_store.sql_query import PGVectorSQLQueryEngine
from llama_index import (
    ServiceContext,
    SQLDatabase,
    set_global_service_context
    )
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import (
        messages_to_prompt,
        completion_to_prompt,
    )
from llama_index.embeddings import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding( model_name="BAAI/bge-small-en-v1.5" )
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
        verbose=False,
    )
# Instead of providing a service context when loading the index from storage use a global.
set_global_service_context( ServiceContext.from_defaults(llm=llm, embed_model=embed_model) )

database_name = 'sql_demo'
connection_string = f"postgresql://postgres:admin@192.168.1.106:5432/{database_name}"

engine = create_engine(connection_string)
sql_database = SQLDatabase(engine, include_tables=["city_stats"])

query_engine = PGVectorSQLQueryEngine(
        sql_database=sql_database,
        tables=["city_stats"],
)
query_str = "Which city has the highest population?"
response = query_engine.query(query_str)
sql = response.metadata["sql_query"]
print(f"Executed SQL: {sql}")
print(f"Response: {response}")

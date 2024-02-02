# If we don’t know ahead of time which table we would like to use.
#
# The way we can do this is using the SQLTableNodeMapping object,
# which takes in a SQLDatabase and produces a Node object for each
# SQLTableSchema object passed into the ObjectIndex constructor
from sqlalchemy import create_engine
from llama_index.indices.struct_store.sql_query import (
        SQLTableRetrieverQueryEngine,
    )
from llama_index import (
    set_global_tokenizer,
    SQLDatabase,
    VectorStoreIndex,
    ServiceContext,
    set_global_service_context,
    MockEmbedding
    )
from llama_index.llms import Ollama
from llama_index.objects import (
        SQLTableNodeMapping,
        ObjectIndex,
        SQLTableSchema,
    )
from llama_index.embeddings import HuggingFaceEmbedding
from transformers import AutoTokenizer

EMBED_DIM=384
ollama = Ollama(model="mistral", request_timeout=30.0)
set_global_tokenizer( AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2").encode )

service_context = ServiceContext.from_defaults(llm=ollama, embed_model=MockEmbedding(embed_dim=EMBED_DIM))
# Instead of providing a service context when loading the index from storage use a global.
set_global_service_context( service_context )

database_name = 'sql_demo'
connection_string = f"postgresql://postgres:admin@192.168.1.106:5432/{database_name}"

engine = create_engine(connection_string)
sql_database = SQLDatabase(engine, include_tables=["city_stats"])

city_stats_text = (
        "This table gives information regarding the population and country of a"
        " given city.\nThe user will query with codewords, where 'foo' corresponds"
        " to population and 'bar' corresponds to city."
    )
table_node_mapping = SQLTableNodeMapping(sql_database)
table_schema_objs = [
        (SQLTableSchema(table_name="city_stats", context_str=city_stats_text))
    ]
obj_index = ObjectIndex.from_objects(
    table_schema_objs,
    table_node_mapping,
    VectorStoreIndex,
)
query_engine = SQLTableRetrieverQueryEngine(
        sql_database, obj_index.as_retriever(similarity_top_k=1)
    )

query_str = "Return the top 4 cities (along with their populations) with the highest population."
response = query_engine.query(query_str)
sql = response.metadata["sql_query"]
print(f"Executed SQL: {sql}")
print(f"Response: {response}")

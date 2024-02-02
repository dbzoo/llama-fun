from llama_index import (
    ServiceContext,
    load_index_from_storage,
    StorageContext,
    set_global_service_context
    )
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import (
        messages_to_prompt,
        completion_to_prompt,
    )
from llama_index.embeddings import HuggingFaceEmbedding

import os, sys

print("Loading model")
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
        verbose=True,
    )
# Instead of providing a service context when loading the index from storage use a global.
set_global_service_context( ServiceContext.from_defaults(llm=llm, embed_model=embed_model) )

PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    print("Storage must be setup first; 3-Persist.py")
    sys.exit(1)

query_engine = load_index_from_storage( StorageContext.from_defaults(persist_dir=PERSIST_DIR) ).as_query_engine()
response = query_engine.query("What is this document about?")
print(response)

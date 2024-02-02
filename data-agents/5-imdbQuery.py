# This example https://llamahub.ai/l/tools-wikipedia using a Local LLM
from llama_index import set_global_tokenizer
from llama_index.llms import Ollama
from llama_index.agent import ReActAgent
from transformers import AutoTokenizer
from imdbToolSpec import IMDBToolSpec

ollama = Ollama(model="starling-lm", request_timeout=30.0)
set_global_tokenizer(AutoTokenizer.from_pretrained("openchat/openchat_3.5").encode)
tool_list = IMDBToolSpec().to_tool_list()
agent = ReActAgent.from_tools(tools=tool_list, llm=ollama, verbose=True)
for question in ("What year did the first 'Conan the Barbarian' movie come out?",
                 "List movies with the title 'Conan the Barbarian' with their release year"):
    print(f"Q: {question}")
    print("A: "+str(agent.chat(question)))

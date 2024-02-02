# This example https://llamahub.ai/l/tools-wikipedia using a Local LLM
from llama_index import set_global_tokenizer
from llama_hub.tools.wikipedia import WikipediaToolSpec
from llama_index.llms import Ollama
from llama_index.agent import ReActAgent
from transformers import AutoTokenizer

ollama = Ollama(model="starling-lm", request_timeout=30.0)
set_global_tokenizer(AutoTokenizer.from_pretrained("openchat/openchat_3.5").encode)
tool_list = WikipediaToolSpec().to_tool_list()
agent = ReActAgent.from_tools(tools=tool_list, llm=ollama, verbose=True)
question = "Search Wikipedia and summarize what is a cheesecake"
print(f"Q: {question}")
print("A: "+str(agent.chat(question)))

# Obversations:
#   With llama2:7b-chat-q5_K_S, llama2:7b-chat-q5_K_M models, the code works, but hits CPU.
#   llama2:7b-chat-q4_K_M - starling-lm fits in the GPU
#   Using mistral, mistral:7b-instruct-v0.2-q5_K_M and llama2 confused the ReActAgent
#
# Smells like this issue: https://github.com/run-llama/llama_index/issues/9057

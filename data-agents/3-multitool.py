# Demonstation using multiple agent tools
from llama_index import set_global_tokenizer
from llama_index.llms import Ollama
from llama_index.agent import ReActAgent
from llama_hub.tools.wikipedia import WikipediaToolSpec
from llama_hub.tools.weather import OpenWeatherMapToolSpec
from llama_index.tools.function_tool import FunctionTool
from transformers import AutoTokenizer

def add_numbers(x: int, y: int) -> int:
    """Adds two numbers together and returns the result"""
    return x + y

ollama = Ollama(model="starling-lm", request_timeout=30.0)
# https://huggingface.co/TheBloke/Starling-LM-7B-alpha-GGUF
set_global_tokenizer(AutoTokenizer.from_pretrained("openchat/openchat_3.5").encode)

# Each spec defines multiple tools.
# .to_tool_list() returns an array of FunctionTools implemented by the Spec
tool_list = []
tool_list += WikipediaToolSpec().to_tool_list()
tool_list += [FunctionTool.from_defaults(fn=add_numbers)]

agent = ReActAgent.from_tools(tool_list, llm=ollama, verbose=True)
for question in ( "Ask wikipedia what country has the largest population",
                  "What is 102 + 34" ):
    print(f"Q: {question}")
    print("A: "+str(agent.chat(question)))

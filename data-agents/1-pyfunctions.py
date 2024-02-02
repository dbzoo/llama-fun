# Calling python functions as agent tools
import datetime
from llama_index import set_global_tokenizer
from llama_index.llms import Ollama
from llama_index.agent.react.base import ReActAgent
from llama_index.tools import FunctionTool
from transformers import AutoTokenizer

def add_numbers(a : int, b: int) -> int:
    """Adds two numbers and returns the result"""
    return a+b

def get_current_date_time() -> dict:
    """Returns a dictionary object of today's date and time"""
    current_datetime = datetime.datetime.now()
    return {
        "year": current_datetime.year,
        "month": current_datetime.month,
        "day": current_datetime.day,
        "hour": current_datetime.hour,
        "minute": current_datetime.minute,
        "second": current_datetime.second }

# Observation: llama2 and mistral misbehave
ollama = Ollama(model="starling-lm", request_timeout=30.0)
# https://huggingface.co/TheBloke/Starling-LM-7B-alpha-GGUF
set_global_tokenizer(AutoTokenizer.from_pretrained("openchat/openchat_3.5").encode)
all_tools = [
    FunctionTool.from_defaults(fn=add_numbers),
    FunctionTool.from_defaults(fn=get_current_date_time)
]
agent = ReActAgent.from_tools(tools=all_tools, llm=ollama, verbose=True)

for question in ("What is todays date?", "What is 10 + 6 ?"):
    print(f"Q: {question}")
    print("A: "+str(agent.chat(question)))

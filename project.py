import os
from typing import TypedDict

from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()



# State

class pipelinestate(TypedDict):
    raw_input : str
    edited_text : str
    script_text : str
    final_output : str


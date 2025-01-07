#https://langchain-ai.github.io/langgraph/how-tos/create-react-agent/
#pip install -U langgraph langchain-openai

import os
from dotenv import load_dotenv

load_dotenv()
# First we initialize the model we want to use.
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o", temperature=0)


# For this tutorial we will use custom tool that returns pre-defined values for weather in two cities (NYC & SF)

from typing import Literal

from langchain_core.tools import tool


@tool
def get_icd10_code(procdure: Literal["Insertion of central venous catheter", "Replacement of abdominal aorta with synthetic graft","Excision of skin lesion"]):
    """Use this to get ICD-10 Code for the specified medical procedure."""
    if procdure == "Insertion of central venous catheter":
        return "ICD-10-PCS 0016070"
    elif procdure == "Replacement of abdominal aorta with synthetic graft":
        return "ICD-10-PCS 04R00JZ"
    elif procdure == "Excision of skin lesion":
        return "ICD-10-PCS 10A00Z0"    
    else:
        raise AssertionError("Unknown medical procedure")

# see https://python.langchain.com/v0.1/docs/modules/tools/custom_tools/
@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


tools = [get_weather, get_icd10_code]


# Define the graph

from langgraph.prebuilt import create_react_agent

graph = create_react_agent(model, tools=tools)

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

#inputs = {"messages": [("user", "what is the weather in sf")]}
#inputs = {"messages": [("user", "what is the weather like in sf")]}
#inputs = {"messages": [("user", "Is it cloudy in sf")]}
#inputs = {"messages": [("user", "Is it sunny in sfo")]}

#inputs = {"messages": [("user", "What is the ICD-10 code for Insertion of central venous catheter")]}
inputs = {"messages": [("user", "What is the ICD-10 code for Measurement of cardiac pressures")]}

print_stream(graph.stream(inputs, stream_mode="values"))

#Now let's try a question that doesn't need tools
#inputs = {"messages": [("user", "who built you?")]}
#print_stream(graph.stream(inputs, stream_mode="values"))
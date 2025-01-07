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
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


tools = [get_weather]


# Define the graph

from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt import AgentState


#graph = create_react_agent(model, tools=tools)

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

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a helpful bot named Fred."),
     ("placeholder", "{messages}"),
     ("user", "Remember, always be polite!"),
    ])

def format_for_model(state: AgentState):
     # You can do more complex modifications here
     return prompt.invoke({"messages": state["messages"]})

graph = create_react_agent(model, tools, state_modifier=format_for_model)
inputs = {"messages": [("user", "What's your name? And what's the weather in SF?")]}
print_stream(graph.stream(inputs, stream_mode="values"))
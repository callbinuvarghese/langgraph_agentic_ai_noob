
#https://www.pinecone.io/learn/series/langchain/langchain-tools/

#!pip install -qU langchain openai transformers

import os
from dotenv import load_dotenv
from tools1 import CustomSearchTool, CustomCalculatorTool, CircumferenceTool


load_dotenv()
# First we initialize the model we want to use.
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o", temperature=0)

from langchain.chains.conversation.memory import ConversationBufferWindowMemory
# initialize conversational memory
conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True
)

from langchain.agents import initialize_agent

tools = [CustomSearchTool(), CustomCalculatorTool(), CircumferenceTool()]

# initialize agent with tools
#agent = initialize_agent(
#    agent='chat-conversational-react-description',
#    tools=tools,
#    llm=llm,
#    verbose=True,
#    max_iterations=3,
#    early_stopping_method='generate',
#    memory=conversational_memory
#)

from langgraph.prebuilt import create_react_agent

graph = create_react_agent(model, tools=tools) 
#max_iterations=3, early_stopping_method='generate')

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

inputs = {"messages": [("user", "provide weather forecast")]}
print_stream(graph.stream(inputs, stream_mode="values"))
#agent("can you calculate the circumference of a circle that has a radius of 7.81mm")   

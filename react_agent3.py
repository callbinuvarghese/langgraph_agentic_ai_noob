
#https://www.pinecone.io/learn/series/langchain/langchain-tools/

#!pip install -qU langchain openai transformers

import os
from dotenv import load_dotenv

load_dotenv()

from langchain.tools import BaseTool
from math import pi
from typing import Union
  

class CircumferenceTool(BaseTool):
    name = "Circumference calculator"
    description = "use this tool when you need to calculate a circumference using the radius of a circle"

    def _run(self, radius: Union[int, float]):
        return float(radius)*2.0*pi

    def _arun(self, radius: int):
        raise NotImplementedError("This tool does not support async")


from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory


# initialize LLM (we use ChatOpenAI because we'll later define a `chat` agent)
llm = ChatOpenAI(
        openai_api_key="OPENAI_API_KEY",
        temperature=0,
        model_name='gpt-4o'
)

# initialize conversational memory
conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True
)

from langchain.agents import initialize_agent

tools = [CircumferenceTool()]

# initialize agent with tools
agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=conversational_memory
)

agent("can you calculate the circumference of a circle that has a radius of 7.81mm")

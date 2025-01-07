#https://medium.com/@mehulpratapsingh/langchain-agents-for-noobs-a-complete-practical-guide-e231b6c71a4a
# Install required packages
#!pip install langchain openai python-dotenv google-search-results wikipedia
#pip install langchain-openai
#pip install --upgrade --quiet langchain-openai langchain

import os
from dotenv import load_dotenv

#from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

from langchain.schema import HumanMessage

load_dotenv()

class ResearchAgent:
    def __init__(self, llm):
        self.llm = llm
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        
        # Define tools
        self.tools = [
            Tool(
                name="Wikipedia",
                func=self.search_wikipedia,
                description="Useful for searching Wikipedia articles"
            ),
            Tool(
                name="Calculator",
                func=self.calculate,
                description="Useful for performing mathematical calculations"
            )
        ]
        
        # Initialize agent
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )
    
    def search_wikipedia(self, query):
        #from langchain.tools import WikipediaQueryRun
        from langchain_community.tools import WikipediaQueryRun
        from langchain_community.utilities import WikipediaAPIWrapper

        api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
        tool = WikipediaQueryRun(api_wrapper=api_wrapper)
        return tool.invoke({"query": query})
    
    def calculate(self, expression):
        return eval(expression)
    
    def run(self, query):
        return self.agent.run(query)

# Usage example
research_agent = ResearchAgent(ChatOpenAI(temperature=0))
result = research_agent.run("Tell me about artificial intelligence and calculate how many years since it was first coined as a term in 1956.")
print(result)
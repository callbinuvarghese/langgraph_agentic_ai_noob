import unittest

from typing import List, Optional, Type, Union

from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from pydantic import BaseModel, field_validator, ValidationError, Field
import math

class SearchResult(BaseModel):
    title: str
    url: str

class SearchInput(BaseModel):
    query: str


class SearchInput(BaseModel):
    query: str

    @field_validator("query")
    def query_must_not_be_empty(cls, v):
        if not v.strip():  # Check for empty or whitespace-only strings
            raise ValueError("Query cannot be empty or contain only whitespace.")
        return v

    @field_validator("query")
    def query_must_be_alphanumeric(cls, v):
        if not all(c.isalnum() or c.isspace() for c in v):
          raise ValueError("Query must be alphanumeric or contain spaces.")
        return v


class SearchOutput(BaseModel):
    results: List[SearchResult]

class CustomSearchTool(BaseTool):
    """A custom search tool that simulates a basic search engine."""

    name: str = "custom_search"  # Added type annotation here
    description: str = "Useful for when you need to search for information. Input should be a search query."
    _search_data = {
        "weather": [
            SearchResult(title="Current weather forecast", url="https://weather.com/today"),
            SearchResult(title="Weather apps for mobile", url="https://www.appadvice.com/appguides/weather/"),
        ],
        "news": [
            SearchResult(title="Top news headlines", url="https://news.google.com/"),
            SearchResult(title="News aggregators online", url="https://www.feedly.com/"),
        ],
    }

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun]) -> SearchOutput:
        """Use the tool."""
        results = []
        query = query.lower()
        for key, value in self._search_data.items():
            if key in query:
                results.extend(value)
        return SearchOutput(results=results)

    async def _arun(self, query: str, run_manager: Optional[CallbackManagerForToolRun]) -> SearchOutput:
        """Use the tool asynchronously."""
        # Since this is a simple in-memory search, we can just call the synchronous version
        return self._run(query, run_manager)

class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


class CustomCalculatorTool(BaseTool):
    """A custom calculator tool that multiplies two numbers."""

    name: str = "Calculator"
    description: str = "useful for when you need to answer questions about math"
    args_schema: Type[BaseModel] = CalculatorInput
    return_direct: bool = True

    def _run(
        self, a: int, b: int, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return a * b

    async def _arun(
        self,
        a: int,
        b: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")

class CircumferenceInput(BaseModel):
    radius:  Union[int, float] = Field(description="radius")

class CircumferenceTool(BaseTool):
    """A custom calculator tool that multiplies two numbers."""

    name: str = "Circumference calculator"
    description: str = "use this tool when you need to calculate a circumference using the radius of a circle"
    args_schema: Type[BaseModel] = CircumferenceInput
    return_direct: float = True

    def _run(self, radius: Union[int, float]):
        return float(radius)*2.0*math.pi

    def _arun(self, radius: int):
        raise NotImplementedError("This tool does not support async")

def run_calc_tool():
        
    # Example usage of the custom search tool
    calc_tool = CustomCalculatorTool()

def run_search_tool():
        
    # Example usage of the custom search tool
    search_tool = CustomSearchTool()

    # Search for weather information
    search_input = SearchInput(query="weather forecast")
    search_output = search_tool.run(search_input.query)

    print(f"Search results for '{search_input.query}':")
    for result in search_output.results:
        print(f"- {result.title} ({result.url})")

    # Search for news
    search_input = SearchInput(query="latest news")
    search_output = search_tool.run(search_input.query)

    print(f"\nSearch results for '{search_input.query}':")
    for result in search_output.results:
        print(f"- {result.title} ({result.url})")

    # Invalid search (empty)
    try:
        search_input = SearchInput(query="   ")
        search_output = search_tool.run(search_input.query)
        print(f"Search results for '{search_input.query}':")
        for result in search_output.results:
            print(f"- {result.title} ({result.url})")
    except ValidationError as e:
        print(f"Validation Error: {e}")

    # Invalid search (non-alphanumeric)
    try:
        search_input = SearchInput(query="Weather!!!")
        search_output = search_tool.run(search_input.query)
        print(f"Search results for '{search_input.query}':")
        for result in search_output.results:
            print(f"- {result.title} ({result.url})")
    except ValidationError as e:
        print(f"Validation Error: {e}")

def run_calculator_tool():
    calculator_tool = CustomCalculatorTool()

    # 1. Using tool.run (Recommended - handles input validation):

    #calcInput=CalculatorInput(a=5, b=3)
    #result = calculator_tool.run(a=calcInput.a, b=calcInput.b) # Pydantic input
    #print(f"Result (using run with Pydantic): {result}")


    try:
        result = calculator_tool.run({"a": 5, "b": 3}) # Dictionary input
        print(f"Result (using run with dict): {result}")

        result = calculator_tool.run("a=5, b=3") # String input
        print(f"Result (using run with string): {result}")
    except ValidationError as e:
        print(f"Validation Error: {e}")
    try:
        calculator_tool.run({"a": "invalid", "b": 3})  # Invalid input type for 'a'
    except ValidationError as e:
        print(f"Expected Validation Error (invalid type): {e}")
    
    try:
        calculator_tool.run({"a": 5})  # Missing input for 'b'
    except ValidationError as e:
        print(f"Expected Validation Error (missing input): {e}")

    # 2. Direct call to _run (Bypasses input validation - for unit testing core logic):
    try:
        result = calculator_tool._run(5, 3)
        print(f"Result (using _run directly): {result}")
    except Exception as e:
        print(f"Error: {e}")

def run_circumference_tool():
    circumference_tool = CircumferenceTool()
    try:
        result = circumference_tool.run({"radius": 5}) 
        print(f"Result (using _run directly): {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    #run_search_tool()
    #run_calculator_tool()
    run_circumference_tool()
    #unittest.main(argv=[''], exit=False)

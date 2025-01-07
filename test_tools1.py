import unittest
from pydantic import ValidationError
from tools1 import SearchInput, CustomSearchTool  # Import from main.py

class TestSearchInputValidation(unittest.TestCase):
    def test_valid_query(self):
        try:
          SearchInput(query="Valid Search Query")
        except ValidationError:
          self.fail("ValidationError raised for a valid query")

    def test_empty_query(self):
        with self.assertRaises(ValidationError) as context:
            SearchInput(query="   ")
        self.assertIn("Query cannot be empty or contain only whitespace.", str(context.exception))

    def test_non_alphanumeric_query(self):
        with self.assertRaises(ValidationError) as context:
            SearchInput(query="Invalid!!!")
        self.assertIn("Query must be alphanumeric or contain spaces.", str(context.exception))

    def test_mixed_valid_invalid_query(self):
        try:
          SearchInput(query="Valid 123")
        except ValidationError:
          self.fail("ValidationError raised for a valid query")

class TestCustomSearchTool(unittest.TestCase):
  def setUp(self):
    self.search_tool = CustomSearchTool()

  def test_weather_search(self):
    search_output = self.search_tool.run("weather")
    self.assertEqual(len(search_output.results), 2)
    self.assertIn("weather", search_output.results[0].title.lower())
    self.assertIn("weather", search_output.results[1].title.lower())

  def test_news_search(self):
    search_output = self.search_tool.run("news")
    self.assertEqual(len(search_output.results), 2)
    self.assertIn("news", search_output.results[0].title.lower())
    self.assertIn("news", search_output.results[1].title.lower())

  def test_no_results(self):
    search_output = self.search_tool.run("xyz123")  # A query that won't match
    self.assertEqual(len(search_output.results), 0)

  def test_case_insensitivity(self):
      search_output = self.search_tool.run("WeAtHeR")
      self.assertEqual(len(search_output.results), 2)


# Run the tests
#python -m xmlrunner discover -s . -p "test_*.py" -t . -o test-reports
#python -m unittest test_tools1.py

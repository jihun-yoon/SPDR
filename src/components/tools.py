"""
Tools for the Deep Research system
"""

from typing import List, Dict, Any, Optional, Union
import json

# Langchain imports
from langchain_core.tools import BaseTool
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_community.utilities import GoogleSearchAPIWrapper
from src.utils.config import get_config


class FinanceNewsSearchTool:
    """Tool for searching finance news using Yahoo Finance"""

    def __init__(self):
        """Initialize the Finance News Search Tool"""
        self.yahoo_tool = YahooFinanceNewsTool()

    def search(self, query: str) -> List[Dict[str, str]]:
        """
        Search for finance news articles

        Args:
            query: Search query, could be a ticker symbol or a company name

        Returns:
            List[Dict[str, str]]: List of news articles with title, content, and source
        """
        # Call the Yahoo Finance News tool
        result = self.yahoo_tool.invoke(query)

        # Process the response
        if not result or result.strip() == "":
            return []

        # Yahoo Finance returns a string with news items
        # We need to parse it into structured data
        articles = []

        # Split the result by empty lines
        news_items = result.split("\n\n")
        for item in news_items:
            if not item.strip():
                continue

            # Parse the news item
            lines = item.strip().split("\n")
            if len(lines) >= 1:
                title = lines[0]
                content = "\n".join(lines[1:]) if len(lines) > 1 else ""
                articles.append(
                    {"title": title, "content": content, "source": "Yahoo Finance News"}
                )

        return articles

    def search_ticker(self, ticker: str) -> List[Dict[str, str]]:
        """
        Search for news about a specific ticker

        Args:
            ticker: Stock ticker symbol

        Returns:
            List[Dict[str, str]]: List of news articles
        """
        return self.search(ticker)

    def search_company(self, company_name: str) -> List[Dict[str, str]]:
        """
        Search for news about a company by name

        Args:
            company_name: Company name

        Returns:
            List[Dict[str, str]]: List of news articles
        """
        return self.search(company_name)


class QueryExpansionTool:
    """Tool for expanding search queries using an LLM"""

    def __init__(self, model_interface):
        """
        Initialize the Query Expansion Tool

        Args:
            model_interface: The ModelInterface instance
        """
        self.model = model_interface

    def expand_query(self, query: str, context: Optional[str] = None) -> List[str]:
        """
        Expand a query into multiple related queries

        Args:
            query: Original query
            context: Optional context for the expansion

        Returns:
            List[str]: List of expanded queries
        """
        # Prepare prompt for the model
        system_prompt = """You are a query expansion expert. Your task is to expand a given query into multiple related queries that would help gather comprehensive information about the topic. Follow these guidelines:
1. Generate search queries that cover different aspects of the topic.
2. Ensure each query is specific and focused.
3. Include variations using different terminology.
4. Consider related topics that would provide useful context.
5. Output ONLY the expanded queries in a JSON list format, nothing else."""

        # Add context if provided
        user_prompt = f"Original query: {query}"
        if context:
            user_prompt += f"\nContext: {context}"
        user_prompt += "\nGenerate 3-5 expanded search queries that will help find comprehensive information about this topic."

        # Define the expected schema
        schema = {
            "queries": {
                "type": "array",
                "description": "List of expanded search queries",
                "items": {"type": "string"},
            }
        }

        # Generate expanded queries
        response = self.model.generate_structured(
            prompt=user_prompt,
            system_prompt=system_prompt,
            json_schema=schema,
            temperature=0.5,  # Higher temperature for more creative expansion
        )

        # Extract the queries
        if "queries" in response and isinstance(response["queries"], list):
            return response["queries"]

        # Fallback if structured output fails
        if "text" in response:
            # Try to parse the text as JSON
            try:
                text = response["text"]
                # Find json-like content
                start_idx = text.find("[")
                end_idx = text.rfind("]")
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = text[start_idx : end_idx + 1]
                    expanded_queries = json.loads(json_str)
                    if isinstance(expanded_queries, list):
                        return expanded_queries
            except:
                pass

            # If that fails, try to extract queries line by line
            lines = response["text"].split("\n")
            queries = [line.strip() for line in lines if line.strip()]
            if queries:
                return queries

        # If all else fails, return the original query
        return [query]


def get_tools(model_interface) -> Dict[str, Any]:
    """
    Get all available tools for the Deep Research system

    Args:
        model_interface: The ModelInterface instance

    Returns:
        Dict[str, Any]: Dictionary of tools
    """
    return {
        "finance_news": FinanceNewsSearchTool(),
        "query_expansion": QueryExpansionTool(model_interface),
    }

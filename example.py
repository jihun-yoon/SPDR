#!/usr/bin/env python3
"""
Example script demonstrating the Stock Price Deep Reasoner with Deep Research
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Example queries
EXAMPLE_QUERIES = [
    "What are the recent developments and future outlook for NVIDIA stock?",
    "What factors might affect Apple's stock price in the next quarter?",
    "How might interest rate changes impact bank stocks?",
    "What are the growth prospects for AI-related stocks?",
    "How are EV stocks performing and what is their outlook?",
]


def main():
    """Main entry point for the example"""
    from src.components.deep_search import DeepResearcher

    print("Stock Price Reasoner with Deep Research")
    print("=" * 50)
    print("\nAvailable example queries:")

    for i, query in enumerate(EXAMPLE_QUERIES, 1):
        print(f"{i}. {query}")

    try:
        choice = int(input("\nSelect a query (1-5) or enter 0 to input your own: "))

        if choice == 0:
            query = input("\nEnter your research query: ")
        elif 1 <= choice <= len(EXAMPLE_QUERIES):
            query = EXAMPLE_QUERIES[choice - 1]
        else:
            print("Invalid choice. Using the first example query.")
            query = EXAMPLE_QUERIES[0]

        # Initialize the deep researcher
        researcher = DeepResearcher(verbose=True)

        print(f"\nResearching: {query}")
        print("-" * 50)

        # Run research
        result = researcher.research(query)

        print("\nResearch Results:")
        print("=" * 50)
        print(result)

    except KeyboardInterrupt:
        print("\nResearch interrupted by user.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

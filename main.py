#!/usr/bin/env python3
"""
Stock Price Reasoner with Deep Research
Main entry point for the application
"""

import argparse
import os
import sys
from dotenv import load_dotenv

# Ensure src directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()


def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        description="Deep Research for stock price analysis"
    )
    parser.add_argument("query", type=str, help="Research query about stock prices")
    parser.add_argument(
        "--ticker", type=str, help="Stock ticker symbol to focus research on"
    )
    parser.add_argument(
        "--max-steps", type=int, default=10, help="Maximum number of research steps"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    try:
        from src.components.deep_search import DeepResearcher

        # Initialize researcher
        researcher = DeepResearcher(max_steps=args.max_steps, verbose=args.verbose)

        # Prepare query
        query = args.query
        if args.ticker:
            query = f"Regarding {args.ticker} stock: {query}"

        # Run research
        print(f"Researching: {query}")
        print("-" * 50)

        result = researcher.research(query)

        print("\nResearch Results:")
        print("=" * 50)
        print(result)

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

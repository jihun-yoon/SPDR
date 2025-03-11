# Quick Start Guide

This guide provides a quick introduction to using the Stock Price Deep Reasoner with Deep Research system.

## Setup

Before you begin, make sure you have:
1. Installed the system following the [Installation Guide](installation.md)
2. Configured your environment variables with the necessary API keys

## Running Your First Query

Here's how to run a basic stock research query:

```python
from stock_price_reasoner import DeepResearcher

# Initialize the researcher
researcher = DeepResearcher()

# Run a stock research query
result = researcher.research("What are the growth prospects for NVIDIA (NVDA) over the next 2 years?")

# View the research results
print(result.summary)

# Access detailed findings
for finding in result.findings:
    print(f"Source: {finding.source}")
    print(f"Content: {finding.content}")
    print(f"Confidence: {finding.confidence}")
    print("---")
```

## Common Parameters

You can customize your research with these parameters:

```python
result = researcher.research(
    query="What factors affect Tesla's (TSLA) stock price?",
    depth=3,                # Number of search-read-reason iterations
    max_tokens=10000,       # Maximum token budget for the entire research
    detailed_answer=True    # Generate a more comprehensive answer
)
```

## Next Steps

Once you're comfortable with basic usage:

1. Explore the [Usage Guide](usage_guide.md) for more advanced features
2. Check out the [Examples](examples.md) for specific use cases
3. Learn about the [Architecture](architecture.md) to understand how the system works

For a complete API reference, see the [API Reference](api_reference.md) documentation. 
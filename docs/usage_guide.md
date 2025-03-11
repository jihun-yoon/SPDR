# Usage Guide

This document provides instructions on how to use the Stock Price Reasoner with Deep Research system.

## Basic Usage

To use the system for researching stock-related questions, you can use the main script with your query:

```bash
python main.py "What factors might impact NVDA stock price in the next quarter?"
```

### Command Line Arguments

The system supports the following command line arguments:

- `query`: The research query (required)
- `--ticker`: Specific stock ticker to focus on (optional)
- `--max-steps`: Maximum number of research steps (default: 10)
- `--verbose`: Enable verbose output (optional)

Examples:

```bash
# Basic query
python main.py "What are the recent developments in AI stocks?"

# Query with specific ticker
python main.py "What are the growth prospects?" --ticker AAPL

# Increase max steps for more thorough research
python main.py "How might interest rates affect tech stocks?" --max-steps 15

# Enable verbose output for detailed logging
python main.py "Analyze recent earnings reports for cloud companies" --verbose
```

## Programmatic Usage

You can also use the system programmatically in your own Python code:

```python
from src.components.deep_search import DeepResearcher

# Initialize the researcher
researcher = DeepResearcher(max_steps=10, verbose=True)

# Perform research
query = "What factors might impact NVDA stock price in the next quarter?"
result = researcher.research(query)

# Use the research results
print(result)
```

## Example Script

For convenience, an example script is provided that demonstrates basic usage:

```bash
python example.py
```

The example script provides a selection of pre-defined queries and allows you to enter your own custom query.

## Customization

### Adjusting the Token Budget

You can adjust the token budget by setting the `TOKEN_BUDGET` environment variable:

```bash
export TOKEN_BUDGET=8192
python main.py "Your research query"
```

### Changing the LLM Model

To use a different vLLM model, set the `VLLM_MODEL_NAME` environment variable:

```bash
export VLLM_MODEL_NAME="mistralai/Mistral-7B-Instruct-v0.2"
python main.py "Your research query"
```

### Running with a Remote vLLM Endpoint

If you're running vLLM as a server, you can connect to it by setting the `VLLM_ENDPOINT`:

```bash
export VLLM_ENDPOINT="http://localhost:8000/v1"
python main.py "Your research query"
``` 
# Example Usage Scenarios

This document provides examples of how to use the Stock Price Reasoner with Deep Research system for different research scenarios.

## Example 1: Analyzing a Specific Stock

### Query
```bash
python main.py "What are the recent developments and future outlook for NVIDIA stock?"
```

### What This Does
This will research:
- Recent news about NVIDIA
- Earnings reports and financial performance
- Analyst opinions and price targets
- Market trends affecting the semiconductor industry
- AI and data center developments relevant to NVIDIA

### Alternative Method
You can also specify the ticker separately:
```bash
python main.py "What are the recent developments and future outlook?" --ticker NVDA
```

## Example 2: Exploring Industry Trends

### Query
```bash
python main.py "How are EV stocks performing and what is their outlook?"
```

### What This Does
This will research:
- Performance of major EV companies (Tesla, Rivian, Lucid, etc.)
- Industry trends in electric vehicle adoption
- Regulatory changes affecting EV manufacturers
- Supply chain considerations
- Market competition and growth forecasts

## Example 3: Analyzing Economic Factors

### Query
```bash
python main.py "How might interest rate changes impact bank stocks?"
```

### What This Does
This will research:
- Recent and projected interest rate changes
- Historical correlations between rates and bank performance
- Analyst opinions on banking sector outlook
- Specific banks that might be more affected
- Related economic factors

## Example 4: Technical Integration

Here's an example of integrating the researcher into a trading analysis application:

```python
from src.components.deep_search import DeepResearcher
import pandas as pd
import matplotlib.pyplot as plt

# Initialize researcher
researcher = DeepResearcher(max_steps=15)

# Define stocks to analyze
stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
results = {}

# Research each stock
for ticker in stocks:
    query = f"What is the current sentiment and growth outlook for {ticker}?"
    research_result = researcher.research(query)
    results[ticker] = research_result
    
    # Save to file
    with open(f"{ticker}_analysis.txt", "w") as f:
        f.write(research_result)
    
    print(f"Completed research for {ticker}")

# Display summary
for ticker, result in results.items():
    # Extract a summary (first paragraph)
    summary = result.split('\n\n')[0]
    print(f"{ticker}: {summary}")
```

## Example 5: Batch Processing with Custom Configuration

```python
import os
from src.components.deep_search import DeepResearcher
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure for more thorough research
os.environ["MAX_STEPS"] = "20"
os.environ["TOKEN_BUDGET"] = "8192"

# Initialize researcher with custom settings
researcher = DeepResearcher(verbose=True)

# List of research questions from a file
with open("research_questions.txt", "r") as f:
    questions = [line.strip() for line in f if line.strip()]

# Process each question
for i, question in enumerate(questions):
    print(f"Processing question {i+1}/{len(questions)}: {question}")
    
    result = researcher.research(question)
    
    # Save results
    with open(f"results/question_{i+1}.txt", "w") as f:
        f.write(f"Question: {question}\n\n")
        f.write(f"Answer:\n{result}")
    
    print(f"Completed question {i+1}")
```

These examples demonstrate the flexibility of the Stock Price Reasoner with Deep Research system for various financial research scenarios. 
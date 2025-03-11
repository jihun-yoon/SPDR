# SPDR: Stock Price Deep Reasoner

This project implements a Deep Research system for stock price analysis using open-source models via Langchain and vLLM. The system is based on the iterative deep search approach described in [Jina AI's blog post on implementing DeepSearch/DeepResearch](https://jina.ai/news/a-practical-guide-to-implementing-deepsearch-deepresearch/).

## Features

- **Iterative Deep Research Loop**: Implements a continuous loop of searching, reading, and reasoning until an optimal answer is found
- **Open Source LLM Integration**: Uses vLLM to run open source models efficiently
- **Yahoo Finance News Integration**: Leverages Langchain's Yahoo Finance News tools for up-to-date financial information
- **Memory Management**: Tracks knowledge acquisition through the research process
- **Embedding-based Deduplication**: Uses sentence embeddings for information deduplication

## Project Structure

```
SPDR/
├── src/
│   ├── components/
│   │   ├── deep_search.py      # Main deep search loop implementation
│   │   ├── memory.py           # Memory management for the search process
│   │   ├── llm_interface.py    # Interface for language models through vLLM
│   │   └── tools.py            # Tool implementations (Yahoo Finance, etc.)
│   └── utils/
│       ├── config.py           # Configuration management
│       ├── embeddings.py       # Embedding utilities for deduplication
│       └── logging.py          # Logging utilities
├── .env                        # Environment variables (create from .env.example)
├── requirements.txt            # Project dependencies
└── main.py                     # Main entry point
```

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env`:
   ```
   # Model configuration
   VLLM_MODEL_NAME=your_model_name
   VLLM_ENDPOINT=http://localhost:8000/v1  # If running vLLM as a server

   # Optional API keys if needed
   OPENAI_API_KEY=your_openai_api_key  # If using OpenAI for embeddings
   ```

4. Run the application:
   ```
   python main.py
   ```

## Usage

The system can be used to perform deep research on stock prices and related financial information. It will iteratively search for information, read relevant data, and reason about the findings until it can provide a comprehensive answer.

Example usage:
```python
from src.components.deep_search import DeepResearcher

# Initialize the deep researcher
researcher = DeepResearcher()

# Ask a research question
answer = researcher.research("What factors might impact NVDA stock price in the next quarter?")
print(answer)
```

## Implementation Details

This implementation follows the core principles from Jina AI's DeepSearch approach:
1. **Search**: Uses Yahoo Finance News to find relevant financial information
2. **Read**: Processes and understands the retrieved information
3. **Reason**: Evaluates current knowledge and determines next steps
4. Continue the loop until an answer is found or the token budget is exceeded

## License

MIT

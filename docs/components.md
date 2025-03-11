# System Components

This document provides detailed information about each component of the Stock Price Reasoner system.

## Deep Researcher (`deep_search.py`)

The DeepResearcher class is the core component that orchestrates the entire research process. It manages the iterative search-read-reason loop and coordinates all other components.

### Key Features:
- **Research Loop Management**: Controls the flow of the research process
- **Action Planning**: Determines the next optimal action based on current state
- **State Tracking**: Monitors research progress and token usage
- **Answer Generation**: Creates the final comprehensive answer

### Methods:
- `research(query)`: Main method that initiates and manages the research process
- `_plan_next_action()`: Decides what action to take next
- `_execute_search()`, `_execute_read()`, `_execute_reason()`, `_execute_answer()`: Implement different action types
- `_generate_final_answer()`: Synthesizes knowledge into a final answer

## Memory Management (`memory.py`)

The ResearchMemory class manages the accumulation and retrieval of knowledge throughout the research process.

### Key Features:
- **Fact Storage**: Stores information gathered during research
- **Question Tracking**: Manages original and follow-up questions
- **Source Tracking**: Records visited information sources
- **Deduplication**: Prevents storing redundant information
- **Relevance Matching**: Finds information relevant to specific questions

### Methods:
- `add_fact()`: Adds a new fact to memory if not duplicate
- `add_question()`, `mark_question_answered()`: Manage research questions
- `get_relevant_facts()`: Retrieves facts most relevant to a given query
- `get_formatted_facts()`: Formats facts for inclusion in prompts

## LLM Interface (`llm_interface.py`)

The ModelInterface class provides an abstraction layer for interacting with language models via vLLM.

### Key Features:
- **Model Configuration**: Manages model parameters and setup
- **Text Generation**: Handles prompt formatting and response generation
- **Structured Output**: Supports JSON schema-based structured outputs
- **Temperature Control**: Allows adjusting the randomness of outputs

### Methods:
- `generate()`: Generates text based on prompt and system instructions
- `generate_structured()`: Generates structured output based on a JSON schema

## Tools (`tools.py`)

The tools package provides specialized utilities for gathering and processing information.

### Components:
- **FinanceNewsSearchTool**: Interfaces with Yahoo Finance News to retrieve financial information
- **QueryExpansionTool**: Uses the LLM to expand research queries into multiple variations

### Methods:
- `FinanceNewsSearchTool.search()`: Searches for finance news articles
- `QueryExpansionTool.expand_query()`: Expands a query into multiple related queries

## Utilities

### Embeddings (`embeddings.py`):
- Provides functionality for computing text embeddings
- Implements similarity calculation and deduplication
- Offers methods for finding semantically similar content

### Logging (`logging.py`):
- Configures logging with appropriate formatting
- Provides specialized logging for different action types
- Implements color-coded output for better readability

### Configuration (`config.py`):
- Manages system configuration with sensible defaults
- Allows overriding settings via environment variables
- Centralizes configuration management 
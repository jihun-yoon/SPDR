# System Architecture

The Stock Price Deep Reasoner with Deep Research system is built with a modular architecture designed for flexibility and extensibility. This document provides an overview of the system's architecture and how the components interact.

## High-Level Architecture

The system follows a layered architecture: 

```text
+-------------------------------------------------------------------+
| Main Application                                                  |
+-------------------------------------------------------------------+
            |                     |                    |
            v                     v                    v
+------------------+  +-------------------+  +------------------+
| Deep Researcher  |  | Memory Management |  | LLM Interface    |
+------------------+  +-------------------+  +------------------+
            |                     |                    |
            v                     v                    v
+------------------+  +-------------------+  +------------------+
| Tools            |  | Utilities         |  | Configuration    |
+------------------+  +-------------------+  +------------------+
```

## Core Components

1. **Deep Researcher**: The central component that orchestrates the research process through iterative search-read-reason loops.

2. **Memory Management**: Manages the accumulation and retrieval of knowledge throughout the research process.

3. **LLM Interface**: Provides an abstraction layer for interacting with language models via vLLM.

4. **Tools**: Specialized components for tasks like finance news search and query expansion.

5. **Utilities**: Helper functions and classes for embeddings, logging, and configuration.

## Information Flow

1. User submits a research query
2. Deep Researcher initializes the research process
3. The system iteratively:
   - Plans the next action (search, read, or reason)
   - Executes the action using appropriate tools
   - Updates memory with new knowledge
   - Evaluates whether to continue or generate an answer
4. When complete, returns a comprehensive answer based on accumulated knowledge

## Component Interactions

- **Deep Researcher ↔ Memory Management**: Deep Researcher stores and retrieves facts, questions, and search history in Memory.
- **Deep Researcher ↔ LLM Interface**: Deep Researcher uses the LLM for reasoning, query expansion, and answer generation.
- **Deep Researcher ↔ Tools**: Deep Researcher uses tools to gather information from external sources.
- **Memory Management ↔ Utilities**: Memory uses embedding utilities for similarity search and deduplication.
- **LLM Interface ↔ Configuration**: LLM Interface uses configuration settings to initialize and configure the language model.

This modular design allows for easy extension and modification of individual components while maintaining the overall system functionality.
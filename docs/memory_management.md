# Memory Management

This document explains how the memory system works in the Stock Price Deep Reasoner with Deep Research system.

## Memory Components

The memory system manages several types of information:

1. **Facts**: Information gathered during research
2. **Questions**: Original and follow-up questions
3. **Search Queries**: Queries used for information retrieval
4. **Visited Sources**: Sources that have been accessed

## Memory Operations

### Adding Information

When new information is discovered during research, it is added to memory using methods like:

- `add_fact(content, source, metadata)`: Adds a new fact with its source and metadata
- `add_question(question)`: Adds a new question to be investigated
- `add_search_query(query)`: Records a search query that was executed
- `add_visited_source(source)`: Tracks information sources that have been accessed

### Deduplication

To prevent redundant information, the memory system uses embedding-based similarity detection:

1. When a new fact or question is added, its embedding is computed
2. The embedding is compared with existing items using cosine similarity
3. If similarity exceeds a threshold, the item is considered a duplicate and not added

This approach ensures that semantically similar information is not stored multiple times, even if it has different wording.

### Relevance Matching

When the system needs information relevant to a specific question:

1. The question and all facts are converted to embeddings
2. Similarity scores are computed between the question and each fact
3. Facts are ranked by similarity
4. The most relevant facts are retrieved

This enables the system to focus on the most pertinent information when reasoning about a specific question.

## Memory Implementation

The memory system is implemented in the `ResearchMemory` class with the following components:

- **Data Structures**:
  - `facts`: List of MemoryItem objects (content, source, metadata)
  - `questions`: List of unanswered questions
  - `answered_questions`: List of questions that have been addressed
  - `search_queries`: List of executed search queries
  - `visited_sources`: List of accessed information sources

- **Supporting Methods**:
  - `get_formatted_facts()`: Returns facts formatted for inclusion in prompts
  - `get_relevant_facts()`: Finds facts most relevant to a given query
  - `get_unanswered_questions()`: Returns questions that still need investigation
  - `get_summary()`: Provides a summary of the memory state

## Memory Optimization

To prevent memory growth issues during extended research:

1. Each memory component has a maximum size limit
2. When a component exceeds its limit, older items are removed
3. The maximum size is configurable via the `MAX_MEMORY_ITEMS` setting

## Using the Memory System

The memory system is primarily used by the DeepResearcher component:

1. During search, new facts are added to memory
2. During reasoning, insights are added as facts and follow-up questions are identified
3. When generating an answer, relevant facts are retrieved from memory
4. Throughout the process, the memory tracks what has been done to avoid repetition 
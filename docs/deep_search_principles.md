# Deep Search Principles

This document explains the core principles of the Deep Research approach implemented in our system.

## The Deep Search Loop

The fundamental concept of Deep Research is the continuous loop of searching, reading, and reasoning until a comprehensive answer is found. This approach differs from traditional RAG systems that typically perform a single search-and-generate pass.

The loop consists of three main actions:

1. **Search**: Retrieving relevant information from external sources (Yahoo Finance News)
2. **Read**: Processing and understanding the retrieved information
3. **Reason**: Analyzing current knowledge, identifying gaps, and determining next steps

## Action Planning

The system dynamically plans its next action based on the current state of knowledge and the research question. This planning uses several factors:

- Amount of accumulated knowledge
- Remaining unanswered questions
- Previous search attempts
- Current step in the research process
- Available token budget

This dynamic planning allows the system to adapt its research strategy based on what it discovers during the process.

## Progressive Knowledge Building

The Deep Research approach progressively builds knowledge through multiple iterations, enabling it to:

1. Start with broad searches
2. Identify knowledge gaps
3. Formulate specific follow-up questions
4. Search for targeted information
5. Synthesize findings into a comprehensive answer

## Budget-Aware Processing

The system is designed to be aware of its computational budget (in terms of tokens):

- It tracks token usage throughout the research process
- It adjusts research depth based on remaining budget
- When approaching budget limits, it can enter "beast mode" to ensure an answer is generated

## Memory Management

Effective memory management is crucial for Deep Research, enabling the system to:

- Track accumulated knowledge
- Avoid duplication
- Remember previous search attempts
- Identify the most relevant information for the current question

## Reasoning and Evaluation

The system incorporates reasoning steps to:

- Extract insights from gathered information
- Identify connections between different pieces of information
- Assess information reliability
- Determine if more research is needed
- Evaluate answer completeness and accuracy

These principles combine to create a powerful research system that can explore topics in depth, handle complex questions, and provide comprehensive, well-supported answers. 
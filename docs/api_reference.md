# API Reference

This document provides a detailed reference for the key classes and methods in the Stock Price Reasoner with Deep Research system.

## DeepResearcher

```python
class DeepResearcher:
    """Main component for deep research through iterative search-read-reason loop"""
    
    def __init__(self, max_steps: Optional[int] = None, verbose: bool = False):
        """Initialize the Deep Researcher"""
        
    def research(self, query: str) -> str:
        """
        Perform deep research on a query
        
        Args:
            query: The research query
            
        Returns:
            str: Research results
        """
```

## ResearchMemory

```python
class ResearchMemory:
    """Memory system for the Deep Research process"""
    
    def __init__(self):
        """Initialize the memory system"""
        
    def add_fact(self, content: str, source: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Add a fact to memory if not a duplicate
        
        Args:
            content: Content of the fact
            source: Source of the fact
            metadata: Additional metadata about the fact
            
        Returns:
            bool: True if fact was added, False if it was a duplicate
        """
        
    def add_question(self, question: str) -> bool:
        """
        Add a question to memory if not a duplicate
        
        Args:
            question: Question to add
            
        Returns:
            bool: True if question was added, False if it was a duplicate
        """
        
    def mark_question_answered(self, question: str) -> None:
        """
        Mark a question as answered and move it to answered questions
        
        Args:
            question: Question to mark as answered
        """
        
    def get_relevant_facts(self, query: str, max_facts: int = 5) -> List[MemoryItem]:
        """
        Get facts relevant to a query
        
        Args:
            query: Query to find relevant facts for
            max_facts: Maximum number of facts to return
            
        Returns:
            List[MemoryItem]: Relevant facts
        """
```

## ModelInterface

```python
class ModelInterface:
    """Interface for language models using vLLM"""
    
    def __init__(self):
        """Initialize the model interface"""
        
    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: Optional[float] = None) -> str:
        """
        Generate text using the language model
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Optional temperature override
            
        Returns:
            str: Generated text
        """
        
    def generate_structured(self, prompt: str, system_prompt: Optional[str] = None, 
                           json_schema: Optional[Dict[str, Any]] = None, 
                           temperature: Optional[float] = None) -> Dict[str, Any]:
        """
        Generate structured output based on a JSON schema
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            json_schema: JSON schema for structured output
            temperature: Optional temperature override
            
        Returns:
            Dict[str, Any]: Structured output
        """
```

## FinanceNewsSearchTool

```python
class FinanceNewsSearchTool:
    """Tool for searching finance news using Yahoo Finance"""
    
    def __init__(self):
        """Initialize the Finance News Search Tool"""
        
    def search(self, query: str) -> List[Dict[str, str]]:
        """
        Search for finance news articles
        
        Args:
            query: Search query, could be a ticker symbol or a company name
            
        Returns:
            List[Dict[str, str]]: List of news articles with title, content, and source
        """
        
    def search_ticker(self, ticker: str) -> List[Dict[str, str]]:
        """
        Search for news about a specific ticker
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            List[Dict[str, str]]: List of news articles
        """
```

## QueryExpansionTool

```python
class QueryExpansionTool:
    """Tool for expanding search queries using an LLM"""
    
    def __init__(self, model_interface):
        """
        Initialize the Query Expansion Tool
        
        Args:
            model_interface: The ModelInterface instance
        """
        
    def expand_query(self, query: str, context: Optional[str] = None) -> List[str]:
        """
        Expand a query into multiple related queries
        
        Args:
            query: Original query
            context: Optional context for the expansion
            
        Returns:
            List[str]: List of expanded queries
        """
```

## Utility Functions

```python
# Embedding utilities
def compute_embeddings(texts: List[str]) -> np.ndarray:
    """
    Compute embeddings for a list of texts
    
    Args:
        texts: List of texts to embed
        
    Returns:
        np.ndarray: Array of embeddings, shape (len(texts), embedding_dim)
    """
    
def compute_similarity(text1: str, text2: str) -> float:
    """
    Compute cosine similarity between two texts
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        float: Cosine similarity (-1 to 1)
    """
    
def is_duplicate(query: str, candidates: List[str], threshold: Optional[float] = None) -> bool:
    """
    Check if a query is a duplicate of any candidates
    
    Args:
        query: Query text
        candidates: List of candidate texts
        threshold: Similarity threshold (if None, use config value)
        
    Returns:
        bool: True if query is a duplicate
    """

# Configuration
def get_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables with defaults
    
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
``` 
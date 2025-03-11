"""
Memory management for the Deep Research system
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from src.utils.config import get_config
from src.utils.embeddings import is_duplicate


@dataclass
class MemoryItem:
    """A single item in the research memory"""

    content: str
    source: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        """String representation of memory item"""
        return f"{self.content} (Source: {self.source})"


class ResearchMemory:
    """Memory system for the Deep Research process"""

    def __init__(self):
        """Initialize the memory system"""
        config = get_config()
        self.max_items = config["MAX_MEMORY_ITEMS"]

        # Different types of memory
        self.facts: List[MemoryItem] = []
        self.questions: List[str] = []
        self.answered_questions: List[str] = []
        self.search_queries: List[str] = []
        self.visited_sources: List[str] = []

    def add_fact(
        self, content: str, source: str, metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Add a fact to memory if not a duplicate

        Args:
            content: Content of the fact
            source: Source of the fact
            metadata: Additional metadata about the fact

        Returns:
            bool: True if fact was added, False if it was a duplicate
        """
        # Check if content is a duplicate
        if is_duplicate(content, [item.content for item in self.facts]):
            return False

        # Add fact to memory
        self.facts.append(
            MemoryItem(content=content, source=source, metadata=metadata or {})
        )

        # Trim if necessary
        if len(self.facts) > self.max_items:
            self.facts.pop(0)

        return True

    def add_question(self, question: str) -> bool:
        """
        Add a question to memory if not a duplicate

        Args:
            question: Question to add

        Returns:
            bool: True if question was added, False if it was a duplicate
        """
        # Check if question is already in questions or answered questions
        if is_duplicate(question, self.questions + self.answered_questions):
            return False

        # Add question to memory
        self.questions.append(question)

        # Trim if necessary
        if len(self.questions) > self.max_items:
            self.questions.pop(0)

        return True

    def mark_question_answered(self, question: str) -> None:
        """
        Mark a question as answered and move it to answered questions

        Args:
            question: Question to mark as answered
        """
        if question in self.questions:
            self.questions.remove(question)
            self.answered_questions.append(question)

            # Trim if necessary
            if len(self.answered_questions) > self.max_items:
                self.answered_questions.pop(0)

    def add_search_query(self, query: str) -> bool:
        """
        Add a search query to memory if not a duplicate

        Args:
            query: Search query to add

        Returns:
            bool: True if query was added, False if it was a duplicate
        """
        # Check if query is a duplicate
        if is_duplicate(query, self.search_queries):
            return False

        # Add query to memory
        self.search_queries.append(query)

        # Trim if necessary
        if len(self.search_queries) > self.max_items:
            self.search_queries.pop(0)

        return True

    def add_visited_source(self, source: str) -> bool:
        """
        Add a visited source to memory

        Args:
            source: Source URL or identifier

        Returns:
            bool: True if source was added, False if it was already visited
        """
        if source in self.visited_sources:
            return False

        self.visited_sources.append(source)

        # Trim if necessary
        if len(self.visited_sources) > self.max_items:
            self.visited_sources.pop(0)

        return True

    def get_formatted_facts(self, max_facts: Optional[int] = None) -> str:
        """
        Get formatted facts from memory

        Args:
            max_facts: Maximum number of facts to include (most recent)

        Returns:
            str: Formatted facts
        """
        facts_to_format = self.facts
        if max_facts is not None:
            facts_to_format = facts_to_format[-max_facts:]

        return "\n".join([f"- {fact}" for fact in facts_to_format])

    def get_relevant_facts(self, query: str, max_facts: int = 5) -> List[MemoryItem]:
        """
        Get facts relevant to a query

        Args:
            query: Query to find relevant facts for
            max_facts: Maximum number of facts to return

        Returns:
            List[MemoryItem]: Relevant facts
        """
        from src.utils.embeddings import compute_embeddings, cosine_similarity

        if not self.facts:
            return []

        # Compute embeddings
        fact_texts = [item.content for item in self.facts]
        all_embeddings = compute_embeddings([query] + fact_texts)

        query_embedding = all_embeddings[0]
        fact_embeddings = all_embeddings[1:]

        # Compute similarities
        similarities = [
            cosine_similarity(query_embedding, fact_embedding)
            for fact_embedding in fact_embeddings
        ]

        # Sort facts by similarity
        fact_similarities = list(zip(self.facts, similarities))
        fact_similarities.sort(key=lambda x: x[1], reverse=True)

        # Return top facts
        return [fact for fact, _ in fact_similarities[:max_facts]]

    def get_unanswered_questions(self) -> List[str]:
        """
        Get all unanswered questions

        Returns:
            List[str]: Unanswered questions
        """
        return self.questions

    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the memory state

        Returns:
            Dict[str, Any]: Memory summary
        """
        return {
            "facts": len(self.facts),
            "questions": len(self.questions),
            "answered_questions": len(self.answered_questions),
            "search_queries": len(self.search_queries),
            "visited_sources": len(self.visited_sources),
        }

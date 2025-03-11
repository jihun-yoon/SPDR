"""
Main Deep Research component for iterative search-read-reason loop
"""

import time
import random
from typing import List, Dict, Any, Optional, Union, Tuple
from enum import Enum

from src.components.memory import ResearchMemory
from src.components.llm_interface import ModelInterface
from src.components.tools import get_tools
from src.utils.config import get_config
from src.utils.logging import setup_logging, log_step, log_memory, logger


class ActionType(Enum):
    """Types of actions the researcher can take"""

    SEARCH = "search"
    READ = "read"
    REASON = "reason"
    ANSWER = "answer"


class DeepResearcher:
    """
    Main component for deep research through iterative search-read-reason loop
    """

    def __init__(self, max_steps: Optional[int] = None, verbose: bool = False):
        """
        Initialize the Deep Researcher

        Args:
            max_steps: Maximum number of research steps (or None for config default)
            verbose: Whether to enable verbose logging
        """
        # Set up logging
        setup_logging(verbose=verbose)

        # Load configuration
        self.config = get_config()
        self.max_steps = max_steps or self.config["MAX_STEPS"]
        self.token_budget = self.config["TOKEN_BUDGET"]

        # Initialize components
        self.model = ModelInterface()
        self.memory = ResearchMemory()
        self.tools = get_tools(self.model)

        # Tracking variables
        self.current_step = 0
        self.total_tokens_used = 0
        self.research_query = ""
        self.research_complete = False
        self.answer = ""

    def research(self, query: str) -> str:
        """
        Perform deep research on a query

        Args:
            query: The research query

        Returns:
            str: Research results
        """
        # Reset state
        self.current_step = 0
        self.total_tokens_used = 0
        self.research_query = query
        self.research_complete = False
        self.answer = ""

        # Initialize memory with the original query
        self.memory = ResearchMemory()
        self.memory.add_question(query)

        logger.info(f"Starting deep research for query: {query}")

        # Main research loop
        while not self.research_complete and self.current_step < self.max_steps:
            self.current_step += 1

            # Check if we're over budget
            if self.total_tokens_used >= self.token_budget:
                logger.warning(f"Token budget exceeded after {self.current_step} steps")
                break

            # Plan next action
            action, action_params = self._plan_next_action()

            # Execute action
            if action == ActionType.SEARCH:
                self._execute_search(action_params)
            elif action == ActionType.READ:
                self._execute_read(action_params)
            elif action == ActionType.REASON:
                self._execute_reason(action_params)
            elif action == ActionType.ANSWER:
                self._execute_answer(action_params)
                self.research_complete = True

            # Add some delay to avoid overwhelming the system
            time.sleep(0.1)

        # If research is still not complete, generate final answer with what we have
        if not self.research_complete:
            logger.info(
                f"Research incomplete after {self.current_step} steps. Generating final answer with current knowledge."
            )
            self._generate_final_answer()

        logger.info(f"Deep research completed in {self.current_step} steps")
        return self.answer

    def _plan_next_action(self) -> Tuple[ActionType, Dict[str, Any]]:
        """
        Plan the next action based on current state

        Returns:
            Tuple[ActionType, Dict[str, Any]]: Action type and parameters
        """
        log_step(self.current_step, "plan", "Planning next action")

        # Get memory summary
        memory_summary = self.memory.get_summary()
        facts_count = memory_summary["facts"]
        questions_count = memory_summary["questions"]

        # If no facts yet, start with search
        if facts_count == 0:
            query = self.research_query
            log_step(
                self.current_step,
                "plan",
                f"No facts yet, starting with search for '{query}'",
            )
            return ActionType.SEARCH, {"query": query}

        # If we have questions to answer, prioritize getting more information
        if questions_count > 0:
            question = self.memory.get_unanswered_questions()[0]

            # Randomize between search and reason to avoid getting stuck
            if self.current_step % 3 == 0 or facts_count < 3:
                log_step(
                    self.current_step,
                    "plan",
                    f"Searching for more information about '{question}'",
                )
                return ActionType.SEARCH, {"query": question}
            else:
                log_step(self.current_step, "plan", "Reasoning about current knowledge")
                return ActionType.REASON, {"focus_question": question}

        # Otherwise, we should have enough information to answer
        if facts_count >= 3 or self.current_step >= self.max_steps // 2:
            log_step(
                self.current_step,
                "plan",
                "Have sufficient information, generating answer",
            )
            return ActionType.ANSWER, {}

        # Default: more search
        log_step(self.current_step, "plan", "Continuing research with more search")
        return ActionType.SEARCH, {"query": self.research_query}

    def _execute_search(self, params: Dict[str, Any]) -> None:
        """
        Execute a search action

        Args:
            params: Search parameters, including the query
        """
        query = params.get("query", self.research_query)
        log_step(self.current_step, "search", f"Searching for: {query}")

        # Use query expansion tool to generate variations
        expanded_queries = self.tools["query_expansion"].expand_query(query)
        log_step(
            self.current_step, "search", f"Expanded to {len(expanded_queries)} queries"
        )

        # Track which query we're using
        self.memory.add_search_query(query)

        # For each expanded query, search for finance news
        all_articles = []
        for expanded_query in expanded_queries:
            log_step(self.current_step, "search", f"Searching for: {expanded_query}")
            articles = self.tools["finance_news"].search(expanded_query)
            log_step(self.current_step, "search", f"Found {len(articles)} articles")
            all_articles.extend(articles)

        # Add search results to memory
        for article in all_articles:
            source = f"{article['source']} - {article['title']}"
            content = f"{article['title']}: {article['content']}"
            self.memory.add_fact(content, source)

        log_step(
            self.current_step, "search", f"Added {len(all_articles)} articles to memory"
        )

    def _execute_read(self, params: Dict[str, Any]) -> None:
        """
        Execute a read action on a specific source

        Args:
            params: Read parameters
        """
        # In the current implementation with Yahoo Finance News,
        # the read action is combined with search
        # This method is kept for future extension
        log_step(self.current_step, "read", "Reading information (handled with search)")

    def _execute_reason(self, params: Dict[str, Any]) -> None:
        """
        Execute a reasoning action to analyze current knowledge

        Args:
            params: Reasoning parameters
        """
        focus_question = params.get("focus_question", self.research_query)
        log_step(self.current_step, "reason", f"Reasoning about: {focus_question}")

        # Get relevant facts from memory
        relevant_facts = self.memory.get_relevant_facts(focus_question)
        facts_str = "\n".join([f"- {fact}" for fact in relevant_facts])

        # Prepare the reasoning prompt
        system_prompt = """You are a financial researcher analyzing information about stocks and markets. 
Your task is to analyze the provided facts, extract insights, and identify gaps in information.
Follow these guidelines:
1. Analyze the facts to extract key insights relevant to the focus question.
2. Identify important connections or patterns in the data.
3. List follow-up questions that would help fill gaps in knowledge.
4. Keep your analysis focused on the specific focus question."""

        user_prompt = f"""Focus Question: {focus_question}

Facts:
{facts_str}

Analyze these facts to provide insights about the focus question. Then identify 2-3 specific follow-up questions that would help fill gaps in knowledge."""

        # Define the expected schema
        schema = {
            "insights": {
                "type": "array",
                "description": "Key insights extracted from the facts",
                "items": {"type": "string"},
            },
            "follow_up_questions": {
                "type": "array",
                "description": "Follow-up questions to fill knowledge gaps",
                "items": {"type": "string"},
            },
        }

        # Generate reasoning
        response = self.model.generate_structured(
            prompt=user_prompt, system_prompt=system_prompt, json_schema=schema
        )

        # Process insights
        if "insights" in response and isinstance(response["insights"], list):
            for insight in response["insights"]:
                self.memory.add_fact(insight, "Reasoning")
                log_step(self.current_step, "reason", f"Insight: {insight}")

        # Process follow-up questions
        if "follow_up_questions" in response and isinstance(
            response["follow_up_questions"], list
        ):
            for question in response["follow_up_questions"]:
                added = self.memory.add_question(question)
                if added:
                    log_step(self.current_step, "reason", f"New question: {question}")

        # If the current focus question was answered, mark it
        self.memory.mark_question_answered(focus_question)

    def _execute_answer(self, params: Dict[str, Any]) -> None:
        """
        Execute an answer action to generate the final response

        Args:
            params: Answer parameters
        """
        log_step(self.current_step, "answer", "Generating final answer")
        self._generate_final_answer()

    def _generate_final_answer(self) -> None:
        """Generate the final answer based on accumulated knowledge"""
        # Get all facts
        facts = self.memory.facts
        facts_str = "\n".join([f"- {fact}" for fact in facts])

        # Prepare the answer generation prompt
        system_prompt = """You are a financial research analyst providing insights based on information gathered. 
Your task is to synthesize the provided facts into a comprehensive, well-structured answer.
Follow these guidelines:
1. Focus on directly answering the original research question.
2. Organize your response logically with clear sections if needed.
3. Be specific and cite information sources where relevant.
4. Acknowledge limitations or uncertainties in the available information.
5. Provide actionable conclusions or recommendations if appropriate."""

        user_prompt = f"""Research Question: {self.research_query}

Facts collected during research:
{facts_str}

Based on these facts, provide a comprehensive answer to the research question."""

        # Generate answer
        answer = self.model.generate(prompt=user_prompt, system_prompt=system_prompt)

        # Store the answer
        self.answer = answer
        log_step(self.current_step, "answer", "Final answer generated")

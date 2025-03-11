"""
Logging utilities for the deep research system
"""

import logging
import sys
from typing import Optional
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Logger instance
logger = logging.getLogger("deep_research")


def setup_logging(verbose: bool = False) -> None:
    """
    Set up logging configuration

    Args:
        verbose: Whether to enable verbose logging
    """
    # Set up handler
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    # Configure logger
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Prevent propagation to root logger
    logger.propagate = False


def log_step(step: int, action: str, details: str, color: Optional[str] = None) -> None:
    """
    Log a research step with formatting

    Args:
        step: Current step number
        action: Action being taken (search, read, reason)
        details: Details about the action
        color: Color to use for the action (default: None)
    """
    color_map = {
        "search": Fore.BLUE,
        "read": Fore.GREEN,
        "reason": Fore.YELLOW,
        "answer": Fore.MAGENTA,
        "error": Fore.RED,
    }

    # Use provided color or look up in map
    action_color = color or color_map.get(action.lower(), "")

    # Format step information
    step_info = f"[Step {step}] {action_color}{action.upper()}{Style.RESET_ALL}"

    # Log the message
    logger.info(f"{step_info}: {details}")


def log_memory(content: str) -> None:
    """
    Log memory content (at debug level)

    Args:
        content: Memory content to log
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(f"MEMORY: {content}")

"""
Configuration utilities for the deep research system
"""

import os
from typing import Dict, Any

# Default values
DEFAULT_CONFIG = {
    # Model configuration
    "VLLM_MODEL_NAME": "mistralai/Mistral-7B-Instruct-v0.2",
    "VLLM_ENDPOINT": "http://localhost:8000/v1",
    # Token limits
    "MAX_TOKENS": 8192,
    "TOKEN_BUDGET": 4096,
    # Search parameters
    "MAX_SEARCH_RESULTS": 5,
    "MAX_STEPS": 10,
    # Memory settings
    "MAX_MEMORY_ITEMS": 100,
    # Embeddings model (for deduplication)
    "EMBEDDING_MODEL": "all-MiniLM-L6-v2",
    # Similarity threshold for deduplication
    "SIMILARITY_THRESHOLD": 0.85,
}


def get_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables with defaults

    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()

    # Override with environment variables
    for key in config:
        if key in os.environ:
            # Convert to appropriate type
            env_value = os.environ[key]
            if isinstance(config[key], int):
                config[key] = int(env_value)
            elif isinstance(config[key], float):
                config[key] = float(env_value)
            elif isinstance(config[key], bool):
                config[key] = env_value.lower() in ("true", "1", "yes")
            else:
                config[key] = env_value

    return config

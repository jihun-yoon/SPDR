"""
LLM interface for the Deep Research system using vLLM
"""

import os
from typing import Dict, Any, List, Optional, Union
from src.utils.config import get_config

# Import LangChain components
from langchain_core.language_models.llms import LLM
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Import VLLM for open source models
from langchain_openai import ChatOpenAI


class ModelInterface:
    """Interface for language models using vLLM"""

    def __init__(self):
        """Initialize the model interface"""
        config = get_config()

        # Get model configuration
        self.model_name = config.get("VLLM_MODEL_NAME")
        self.endpoint = config.get("VLLM_ENDPOINT")
        self.max_tokens = config.get("MAX_TOKENS")

        # Initialize vLLM model through OpenAI-compatible API
        self.llm = ChatOpenAI(
            model=self.model_name,
            openai_api_key="EMPTY",  # Not needed for vLLM
            openai_api_base=self.endpoint,
            max_tokens=self.max_tokens,
            temperature=0.1,  # Low temperature for more deterministic outputs
        )

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """
        Generate text using the language model

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Optional temperature override

        Returns:
            str: Generated text
        """
        # Create messages
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))

        # Override temperature if provided
        kwargs = {}
        if temperature is not None:
            kwargs["temperature"] = temperature

        # Generate response
        response = self.llm.invoke(messages, **kwargs)

        # Return content
        return response.content

    def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        json_schema: Optional[Dict[str, Any]] = None,
        temperature: Optional[float] = None,
    ) -> Dict[str, Any]:
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
        # Use standard generation if no schema provided
        if json_schema is None:
            return {"text": self.generate(prompt, system_prompt, temperature)}

        # Configure the model to output JSON
        from langchain_core.output_parsers import JsonOutputParser
        from langchain_core.pydantic_v1 import BaseModel, Field, create_model

        # Create dynamic Pydantic model from schema
        fields = {}
        for key, value in json_schema.items():
            if isinstance(value, dict) and "type" in value:
                if value["type"] == "string":
                    fields[key] = (str, Field(description=value.get("description", "")))
                elif value["type"] == "integer":
                    fields[key] = (int, Field(description=value.get("description", "")))
                elif value["type"] == "number":
                    fields[key] = (
                        float,
                        Field(description=value.get("description", "")),
                    )
                elif value["type"] == "boolean":
                    fields[key] = (
                        bool,
                        Field(description=value.get("description", "")),
                    )
                elif value["type"] == "array":
                    fields[key] = (
                        List[str],
                        Field(description=value.get("description", "")),
                    )
                else:
                    fields[key] = (str, Field(description=value.get("description", "")))
            else:
                fields[key] = (str, Field(description=""))

        DynamicModel = create_model("DynamicModel", **fields)

        # Create output parser
        parser = JsonOutputParser(pydantic_object=DynamicModel)

        # Prepare the prompt
        messages = []
        if system_prompt:
            # Add JSON formatting instructions to system prompt
            json_instructions = "\nYou MUST format your response as a JSON object that follows this schema:\n"
            json_instructions += parser.get_format_instructions()
            enhanced_system_prompt = system_prompt + json_instructions
            messages.append(SystemMessage(content=enhanced_system_prompt))
        else:
            # Create a system prompt with just the JSON instructions
            json_instructions = "You MUST format your response as a JSON object that follows this schema:\n"
            json_instructions += parser.get_format_instructions()
            messages.append(SystemMessage(content=json_instructions))

        messages.append(HumanMessage(content=prompt))

        # Override temperature if provided
        kwargs = {}
        if temperature is not None:
            kwargs["temperature"] = temperature

        # Generate response
        chain = self.llm | parser
        try:
            response = chain.invoke(messages, **kwargs)
            return response
        except Exception as e:
            # Fallback to non-structured output if parsing fails
            print(f"Error parsing JSON response: {e}")
            raw_response = self.llm.invoke(messages, **kwargs)
            return {"text": raw_response.content, "error": str(e)}

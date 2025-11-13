"""
Cerebras API Client with streaming support.

This module provides a client for interacting with Cerebras Cloud API
for chat completions with tool calling and streaming capabilities.
"""

import os
from typing import Any, Dict, List, Optional, Generator
from cerebras.cloud.sdk import Cerebras


class CerebrasClient:
    """
    Client for Cerebras Cloud API with streaming support.
    
    Handles chat completions with tool calling using the Cerebras SDK.
    The SDK provides built-in retry logic and error handling.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Cerebras client.
        
        Args:
            api_key: Cerebras API key (defaults to CEREBRAS_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("CEREBRAS_API_KEY")
        if not self.api_key:
            raise ValueError("Cerebras API key is required")
        
        # Initialize Cerebras client
        self.client = Cerebras(api_key=self.api_key)
        
        # Using llama-3.3-70b as specified
        self.model = "llama-3.3-70b"
    
    def create_chat_completion(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False
    ) -> Any:
        """
        Create a chat completion with optional tool calling.
        
        Args:
            messages: List of message objects
            tools: Optional list of tool definitions
            stream: Whether to stream the response
            
        Returns:
            Response object or generator for streaming
        """
        # Prepare request parameters
        params = {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }
        
        # Add tools if provided
        if tools:
            params["tools"] = tools
            params["tool_choice"] = "auto"
        
        # Make the API call
        if stream:
            return self._stream_completion(params)
        else:
            return self._complete(params)
    
    def _complete(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a non-streaming chat completion request.
        
        Args:
            params: Request parameters
            
        Returns:
            API response as dictionary
        """
        try:
            response = self.client.chat.completions.create(**params)
            
            # Convert response to dictionary format compatible with OpenAI
            return self._format_response(response)
        
        except Exception as e:
            error_str = str(e)
            # Check for tool_use_failed error from Cerebras
            if "tool_use_failed" in error_str or "No valid function calls generated" in error_str:
                # Return a special response that indicates tool call failure
                # This will be caught by the agent to provide user-friendly guidance
                return {
                    "choices": [
                        {
                            "message": {
                                "content": "",
                                "tool_calls": []
                            }
                        }
                    ],
                    "_tool_call_failed": True,
                    "_tool_call_error": error_str
                }
            raise Exception(f"Cerebras API request failed: {str(e)}")
    
    def _stream_completion(
        self,
        params: Dict[str, Any]
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Stream chat completion responses.
        
        Handles streaming responses from Cerebras API.
        
        Args:
            params: Request parameters
            
        Yields:
            Response chunks containing deltas for text or tool calls
        """
        try:
            stream = self.client.chat.completions.create(**params)
            
            for chunk in stream:
                # Convert chunk to dictionary format
                yield self._format_chunk(chunk)
        
        except Exception as e:
            raise Exception(f"Cerebras streaming failed: {str(e)}")
    
    def _format_response(self, response: Any) -> Dict[str, Any]:
        """
        Format Cerebras response to OpenAI-compatible dictionary.
        
        Args:
            response: Cerebras response object
            
        Returns:
            Formatted response dictionary
        """
        # Convert to dict if it's a Pydantic model
        if hasattr(response, 'model_dump'):
            return response.model_dump()
        elif hasattr(response, 'dict'):
            return response.dict()
        else:
            # Already a dict or can be converted
            return dict(response)
    
    def _format_chunk(self, chunk: Any) -> Dict[str, Any]:
        """
        Format streaming chunk to OpenAI-compatible dictionary.
        
        Args:
            chunk: Cerebras chunk object
            
        Returns:
            Formatted chunk dictionary
        """
        # Convert to dict if it's a Pydantic model
        if hasattr(chunk, 'model_dump'):
            return chunk.model_dump()
        elif hasattr(chunk, 'dict'):
            return chunk.dict()
        else:
            # Already a dict or can be converted
            return dict(chunk)

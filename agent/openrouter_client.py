"""
OpenRouter API client for the GoodFoods Reservation Agent.

This module provides a client for interacting with the OpenRouter API
to access LLM capabilities with tool calling support.
"""

import os
import time
import requests
from typing import Any, Dict, List, Optional, Generator


class OpenRouterClient:
    """
    Client for OpenRouter API with streaming support.
    
    Handles chat completions with tool calling and implements retry logic
    for API failures.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenRouter client.
        
        Args:
            api_key: OpenRouter API key (defaults to OPENROUTER_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
        
        self.base_url = "https://openrouter.ai/api/v1"
        # Using the 70b free model as specified in requirements
        self.model = "meta-llama/llama-3.3-8b-instruct:free"
        self.max_retries = 3
    
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
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/goodfoods-reservation-agent",
            "X-Title": "GoodFoods Reservation Agent"
        }
        
        payload = {
            "model": self.model,
            "messages": messages
        }
        
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        if stream:
            payload["stream"] = True
            return self._stream_completion(headers, payload)
        else:
            return self._complete_with_retry(headers, payload)
    
    def _complete_with_retry(
        self,
        headers: Dict[str, str],
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Make API request with exponential backoff retry logic.
        
        Args:
            headers: Request headers
            payload: Request payload
            
        Returns:
            API response
            
        Raises:
            Exception: If all retries fail
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:  # Rate limit
                    wait_time = (2 ** attempt) * 1  # Exponential backoff
                    time.sleep(wait_time)
                    continue
                else:
                    response.raise_for_status()
            
            except requests.exceptions.RequestException as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    wait_time = (2 ** attempt) * 1
                    time.sleep(wait_time)
                    continue
                else:
                    break
        
        raise Exception(f"API request failed after {self.max_retries} attempts: {last_error}")
    
    def _stream_completion(
        self,
        headers: Dict[str, str],
        payload: Dict[str, Any]
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Stream chat completion responses.
        
        Handles both text streaming and tool calls in streaming responses.
        
        Args:
            headers: Request headers
            payload: Request payload
            
        Yields:
            Response chunks containing deltas for text or tool calls
        """
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=60
        )
        
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]  # Remove 'data: ' prefix
                    
                    if data_str == '[DONE]':
                        break
                    
                    try:
                        import json
                        chunk = json.loads(data_str)
                        
                        # Yield chunk if it contains content or tool calls
                        if 'choices' in chunk and len(chunk['choices']) > 0:
                            delta = chunk['choices'][0].get('delta', {})
                            if delta.get('content') or delta.get('tool_calls'):
                                yield chunk
                    
                    except json.JSONDecodeError:
                        continue

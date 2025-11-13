"""
Reservation Agent implementation for the GoodFoods Reservation Agent.

This module implements the core agent loop with tool calling capabilities
for managing restaurant reservations through natural language interactions.
"""

from typing import Any, Dict, List, Generator, Optional, Tuple
import re
from agent.cerebras_client import CerebrasClient
from mcp_server.server import MCPServer


class ReservationAgent:
    """
    Conversational AI agent for restaurant reservations.
    
    Implements a custom agent loop with tool calling support, maintaining
    conversation context and orchestrating interactions between the LLM
    and the MCP Server.
    """
    
    # Tool schemas formatted according to OpenAI function calling specification
    TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "search_restaurants",
                "description": "Search for restaurants based on criteria such as cuisine type, location, party size, date, and time",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cuisine": {
                            "type": "string",
                            "description": "Type of cuisine (e.g., Italian, Chinese, Japanese, Mexican)"
                        },
                        "location": {
                            "type": "string",
                            "description": "Geographic location or area (e.g., Downtown, Midtown, Uptown)"
                        },
                        "party_size": {
                            "type": "integer",
                            "description": "Number of guests in the party"
                        },
                        "date": {
                            "type": "string",
                            "description": "Reservation date in YYYY-MM-DD format"
                        },
                        "time": {
                            "type": "string",
                            "description": "Reservation time in HH:MM format (24-hour)"
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_availability",
                "description": "Check availability for a specific restaurant at a given date and time",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "restaurant_id": {
                            "type": "string",
                            "description": "Unique identifier of the restaurant"
                        },
                        "date": {
                            "type": "string",
                            "description": "Reservation date in YYYY-MM-DD format"
                        },
                        "time": {
                            "type": "string",
                            "description": "Reservation time in HH:MM format (24-hour)"
                        },
                        "party_size": {
                            "type": "integer",
                            "description": "Number of guests in the party"
                        }
                    },
                    "required": ["restaurant_id", "date", "time", "party_size"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "make_reservation",
                "description": "Create a new reservation at a restaurant for a specific date, time, and party size",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "restaurant_id": {
                            "type": "string",
                            "description": "Unique identifier of the restaurant"
                        },
                        "date": {
                            "type": "string",
                            "description": "Reservation date in YYYY-MM-DD format"
                        },
                        "time": {
                            "type": "string",
                            "description": "Reservation time in HH:MM format (24-hour)"
                        },
                        "party_size": {
                            "type": "integer",
                            "description": "Number of guests in the party"
                        },
                        "customer_name": {
                            "type": "string",
                            "description": "Full name of the customer making the reservation"
                        }
                    },
                    "required": ["restaurant_id", "date", "time", "party_size", "customer_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "cancel_reservation",
                "description": "Cancel an existing reservation using the reservation ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "Unique identifier of the reservation to cancel"
                        }
                    },
                    "required": ["reservation_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_recommendations",
                "description": "Get personalized restaurant recommendations based on user preferences",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "preferences": {
                            "type": "object",
                            "description": "User preferences for restaurant recommendations",
                            "properties": {
                                "cuisine": {
                                    "type": "string",
                                    "description": "Preferred cuisine type"
                                },
                                "location": {
                                    "type": "string",
                                    "description": "Preferred location or area"
                                },
                                "price_range": {
                                    "type": "string",
                                    "description": "Preferred price range ($, $$, $$$, $$$$)"
                                },
                                "min_rating": {
                                    "type": "number",
                                    "description": "Minimum rating (1.0 to 5.0)"
                                }
                            }
                        }
                    },
                    "required": []
                }
            }
        }
    ]
    
    # System message to guide LLM behavior
    SYSTEM_MESSAGE = {
        "role": "system",
        "content": """You are a helpful restaurant reservation assistant. Your role is to help users find restaurants, check availability, make reservations, and get recommendations.

SCOPE ENFORCEMENT - CRITICAL:
1. ONLY answer questions related to restaurants, reservations, dining, and food
2. If asked about topics outside your scope (weather, sports, general knowledge, personal information, etc.), politely refuse and redirect:
   - Example: "I'm a restaurant reservation assistant and can only help with finding restaurants and making reservations. Is there a restaurant you'd like to search for?"
3. DO NOT call tools for out-of-scope queries
4. If unsure whether a query is in scope, err on the side of asking clarifying questions about restaurant preferences

FORMATTING REQUIREMENTS - CRITICAL AND MANDATORY:
1. ALWAYS use proper spacing and line breaks between information
2. ALWAYS add a blank line between each restaurant (press Enter twice)
3. NEVER remove spaces from restaurant names or addresses
4. ALWAYS write out addresses with proper spacing: NOT "3572RiverRd,Downtown" BUT "3572 River Rd, Downtown"
5. ALWAYS use **bold** (two asterisks) for restaurant names
6. Use bullet points for information fields
7. DO NOT concatenate words - always include spaces between words

MANDATORY OUTPUT TEMPLATE FOR RESTAURANTS:
Found these restaurants:

**Restaurant Name**
- Cuisine: Type
- Location: City
- Address: Full Address With Spaces
- Rating: X.X / 5
- Price Range: $ / $$ / $$$ / $$$$
- Description: Full description with spaces

**Next Restaurant Name**
- Cuisine: Type
- Location: City
- Address: Full Address With Spaces
- Rating: X.X / 5
- Price Range: $ / $$ / $$$ / $$$$
- Description: Full description with spaces

CRITICAL AGENT RULES:
1. Use tools to get restaurant information
2. After tool returns results, format them exactly as shown above
3. NEVER stop after a tool call - always provide your formatted response
4. DO NOT call the same tool twice unless user asks differently
5. Be conversational and helpful

REMEMBER: Every space matters. Write naturally with proper English spacing."""
    }
    
    def __init__(self, mcp_server: MCPServer, cerebras_client: CerebrasClient):
        """
        Initialize the Reservation Agent.
        
        Args:
            mcp_server: MCP Server instance for tool execution
            cerebras_client: Cerebras client for LLM interactions
        """
        self.mcp_server = mcp_server
        self.client = cerebras_client
        # Initialize conversation history with system message
        self.conversation_history: List[Dict[str, Any]] = [self.SYSTEM_MESSAGE]

    def process_message(self, user_message: str) -> Generator[Any, None, None]:
        """
        Process a user message and yield response chunks.
        
        Implements the agent loop with tool calling:
        1. Add user message to conversation history
        2. Call LLM with tools and conversation history
        3. Handle tool calls if suggested by LLM
        4. Stream final response to user
        
        Args:
            user_message: The user's input message
            
        Yields:
            Response chunks (text or status updates)
        """
        # Quick pre-check for out-of-context or ambiguous follow-ups.
        # If detected, return a short clarifying response locally without
        # calling the LLM or tools. This avoids unnecessary tool calls for
        # messages like "Any other recommendation" or "Can we have your name for the reservation".
        out_of_context, clarifying_resp = self._is_out_of_context(user_message)
        if out_of_context:
            # Yield the clarifying response and add it to history as assistant
            if clarifying_resp:
                yield clarifying_resp
                self.conversation_history.append({
                    "role": "assistant",
                    "content": clarifying_resp
                })
            return

        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Agent loop - continue until we get a final text response
        max_iterations = 5  # Prevent infinite loops
        iteration = 0
        tools_executed = False  # Track if we've executed tools
        
        try:
            while iteration < max_iterations:
                iteration += 1
                
                # After tools are executed, don't allow more tool calls
                # This prevents the LLM from trying to call tools again
                tools_for_this_call = None if tools_executed else self.TOOLS
                
                # For tool calling rounds, use non-streaming
                # For final response, use streaming
                response = self.client.create_chat_completion(
                    messages=self.conversation_history,
                    tools=tools_for_this_call,
                    stream=False
                )
                
                # Check if LLM wants to call tools
                if "choices" in response and len(response["choices"]) > 0:
                    choice = response["choices"][0]
                    message = choice.get("message", {})
                    
                    # Check for tool calls
                    tool_calls = message.get("tool_calls")
                    
                    if tool_calls:
                        # Add assistant message with tool calls to history
                        self.conversation_history.append({
                            "role": "assistant",
                            "content": message.get("content") or "",
                            "tool_calls": tool_calls
                        })
                        
                        # Yield status update
                        tool_names = [tc.get("function", {}).get("name") for tc in tool_calls]
                        yield f"Using tools: {', '.join(tool_names)}..."
                        
                        # Execute tools and get results, yielding tool call data
                        tool_messages = []
                        for tool_call in tool_calls:
                            tool_id = tool_call.get("id")
                            function_data = tool_call.get("function", {})
                            tool_name = function_data.get("name")
                            
                            # Parse arguments
                            import json
                            try:
                                arguments_str = function_data.get("arguments", "{}")
                                arguments = json.loads(arguments_str)
                            except json.JSONDecodeError:
                                arguments = {}
                            
                            # Execute the tool
                            result = self._execute_tool(tool_name, arguments)
                            
                            # Yield tool call data for UI display
                            yield {
                                "tool_name": tool_name,
                                "arguments": arguments,
                                "result": result
                            }
                            
                            # Create tool message for conversation history
                            tool_message = {
                                "role": "tool",
                                "tool_call_id": tool_id,
                                "content": result
                            }
                            tool_messages.append(tool_message)
                        
                        # Add tool results to conversation history
                        self.conversation_history.extend(tool_messages)
                        
                        # Mark that we've executed tools
                        tools_executed = True
                        
                        # Continue loop to get final response
                        continue
                    else:
                        # No tool calls, get streaming response for final answer
                        # Make a streaming call for the final response
                        # Don't pass tools if we've already executed them
                        stream_response = self.client.create_chat_completion(
                            messages=self.conversation_history,
                            tools=None if tools_executed else self.TOOLS,
                            stream=True
                        )
                        
                        # Accumulate the complete response
                        complete_response = ""
                        
                        # Stream the response chunks
                        for chunk in stream_response:
                            if "choices" in chunk and len(chunk["choices"]) > 0:
                                delta = chunk["choices"][0].get("delta", {})
                                content_chunk = delta.get("content", "")
                                
                                if content_chunk:
                                    complete_response += content_chunk
                                    yield content_chunk
                        
                        # Add complete response to conversation history
                        if complete_response:
                            self.conversation_history.append({
                                "role": "assistant",
                                "content": complete_response
                            })
                        
                        break
                else:
                    # Unexpected response format
                    yield "I apologize, but I encountered an issue processing your request."
                    break
            
            if iteration >= max_iterations:
                yield "I apologize, but I'm having trouble completing your request. Please try rephrasing."
        
        except Exception as e:
            error_message = f"Error processing message: {str(e)}"
            yield error_message

    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Execute a tool via the MCP Server.
        
        Routes tool calls to the appropriate MCP Server method and returns
        the formatted result.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Dictionary of tool arguments
            
        Returns:
            Tool execution result as a string
        """
        try:
            # Create MCP request
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            
            # Execute tool via MCP Server
            mcp_response = self.mcp_server.handle_request(mcp_request)
            
            # Check for errors
            if "error" in mcp_response:
                error_msg = mcp_response["error"].get("message", "Unknown error")
                return f"Error executing {tool_name}: {error_msg}"
            
            # Extract result
            result = mcp_response.get("result", {})
            
            # Format the result based on MCP response structure
            if "content" in result:
                # Extract text from content array
                content_items = result["content"]
                if isinstance(content_items, list) and len(content_items) > 0:
                    return content_items[0].get("text", "No result")
            
            return str(result)
        
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"

    def _is_out_of_context(self, user_message: str) -> Tuple[bool, Optional[str]]:
        """
        Heuristic to detect out-of-context or ambiguous short follow-ups that
        shouldn't trigger tool calls. Returns (is_out_of_context, clarifying_response).

        The heuristic covers common patterns like:
        - "Any other recommendation", "Anything else?", "Any more recommendations?"
        - Requests for the agent's personal name: "Can we have your name for the reservation?"
        - Very short inputs that look like follow-ups without enough context

        This is intentionally conservative: if unsure, it returns False so the
        LLM flow remains in charge.
        """
        if not user_message or not user_message.strip():
            return True, "Could you please clarify your request? I didn't catch that."

        msg = user_message.strip().lower()

        # Pattern: generic follow-up asking for more recommendations/suggestions
        # This should ONLY match vague follow-ups like "Any other recommendation?" 
        # NOT initial requests like "Recommend me some Indian restaurants"
        more_reco_pattern = re.compile(r"^(any|anything|anymore|any other|anything else|more)\b.*\b(recommendation|recommendations|suggestions)")
        if more_reco_pattern.search(msg):
            # If the conversation already contains recommendation results, ask
            # whether they want more of the same or different preferences.
            prev_has_reco = any("recommend" in (m.get("content") or "").lower() for m in self.conversation_history)
            if prev_has_reco:
                return True, ("Do you want more recommendations similar to the ones I showed earlier, "
                              "or would you like to change your preferences (cuisine, location, price)?")
            else:
                # Even without previous recommendations, if it starts with vague words, ask for specifics
                return True, "What kind of recommendations are you looking for? Cuisine, location, or price range?"

        # Pattern: asking for the agent's name or personal info
        name_pattern = re.compile(r"\b(your name|your full name|who are you)\b")
        if name_pattern.search(msg):
            return True, ("I don't have a personal name. If you'd like to make a reservation, "
                          "please provide the customer's full name to use for the booking.")

        # Very short follow-ups without nouns (e.g., "Also?", "And?", "More?")
        tokens = re.findall(r"\w+", msg)
        if len(tokens) <= 2 and (msg.endswith("?") or len(msg) < 15):
            # If it's clearly a continuation and there is insufficient context,
            # ask for clarification.
            return True, "Could you please provide a bit more detail so I can help? For example, which cuisine or area are you interested in?"

        return False, None
    
    def _parse_and_execute_tools(self, tool_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Parse tool calls from LLM response and execute them.
        
        Handles multiple tool calls in parallel and formats results as
        tool messages for the conversation history.
        
        Args:
            tool_calls: List of tool call objects from LLM response
            
        Returns:
            List of tool message objects to add to conversation history
        """
        tool_messages = []
        
        for tool_call in tool_calls:
            tool_id = tool_call.get("id")
            function_data = tool_call.get("function", {})
            tool_name = function_data.get("name")
            
            # Parse arguments (they come as JSON string)
            import json
            try:
                arguments_str = function_data.get("arguments", "{}")
                arguments = json.loads(arguments_str)
            except json.JSONDecodeError:
                arguments = {}
            
            # Execute the tool
            result = self._execute_tool(tool_name, arguments)
            
            # Create tool message
            tool_message = {
                "role": "tool",
                "tool_call_id": tool_id,
                "content": result
            }
            
            tool_messages.append(tool_message)
        
        return tool_messages

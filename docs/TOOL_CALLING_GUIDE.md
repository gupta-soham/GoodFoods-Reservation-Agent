# Tool Calling Guide

Complete guide to understanding and implementing tool calling in the GoodFoods Reservation Agent.

## Table of Contents

- [Overview](#overview)
- [The 3-Step Tool Calling Process](#the-3-step-tool-calling-process)
- [Defining New Tools](#defining-new-tools)
- [How the Agent Loop Works](#how-the-agent-loop-works)
- [Debugging Tips](#debugging-tips)

---

## Overview

Tool calling allows the LLM to interact with external systems by calling predefined functions. Instead of just generating text, the LLM can:

1. Analyze user requests
2. Decide which tools to use
3. Generate appropriate parameters
4. Process tool results
5. Provide natural language responses

---

## The 3-Step Tool Calling Process

### Step 1: LLM Suggests Tool Calls

The LLM analyzes the user's message and conversation history, then decides which tools to call.

**Example Request to LLM:**

```python
{
    "model": "meta-llama/llama-3.3-70b-instruct:free",
    "messages": [
        {"role": "user", "content": "Find Italian restaurants in Downtown"}
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "search_restaurants",
                "description": "Search for restaurants...",
                "parameters": {...}
            }
        }
    ]
}
```

**LLM Response:**

```python
{
    "choices": [{
        "message": {
            "role": "assistant",
            "content": null,
            "tool_calls": [{
                "id": "call_abc123",
                "type": "function",
                "function": {
                    "name": "search_restaurants",
                    "arguments": '{"cuisine": "Italian", "location": "Downtown"}'
                }
            }]
        }
    }]
}
```

### Step 2: Agent Executes Tools

The agent parses tool calls and executes them via the MCP Server.

**Code:**

```python
def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
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

    # Execute via MCP Server
    mcp_response = self.mcp_server.handle_request(mcp_request)

    # Extract and return result
    return mcp_response["result"]["content"][0]["text"]
```

**Tool Result:**

```
Found 3 restaurant(s):

[
  {
    "id": "rest_001",
    "name": "Bella Italia",
    "cuisine": "Italian",
    "location": "Downtown",
    ...
  },
  ...
]
```

### Step 3: LLM Generates Final Response

The agent adds tool results to conversation history and calls the LLM again.

**Request to LLM:**

```python
{
    "messages": [
        {"role": "user", "content": "Find Italian restaurants in Downtown"},
        {
            "role": "assistant",
            "content": null,
            "tool_calls": [...]
        },
        {
            "role": "tool",
            "tool_call_id": "call_abc123",
            "content": "Found 3 restaurant(s): [...]"
        }
    ]
}
```

**LLM Response:**

```
I found 3 Italian restaurants in Downtown for you:

1. **Bella Italia** - A highly-rated authentic Italian restaurant...
2. **Pasta Paradise** - Known for their fresh homemade pasta...
3. **Roma Trattoria** - Traditional Italian cuisine in a cozy setting...

Would you like to check availability at any of these restaurants?
```

---

## Defining New Tools

### Tool Schema Format

Tools follow the OpenAI function calling specification:

```python
{
    "type": "function",
    "function": {
        "name": "tool_name",
        "description": "Clear description of what the tool does",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Description of param1"
                },
                "param2": {
                    "type": "integer",
                    "description": "Description of param2"
                }
            },
            "required": ["param1"]  # Optional parameters not listed
        }
    }
}
```

### Example: Adding a New Tool

Let's add a `get_restaurant_reviews` tool.

**Step 1: Define the Schema**

Add to `ReservationAgent.TOOLS`:

```python
{
    "type": "function",
    "function": {
        "name": "get_restaurant_reviews",
        "description": "Get customer reviews for a specific restaurant",
        "parameters": {
            "type": "object",
            "properties": {
                "restaurant_id": {
                    "type": "string",
                    "description": "Unique identifier of the restaurant"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of reviews to return (default: 5)"
                }
            },
            "required": ["restaurant_id"]
        }
    }
}
```

**Step 2: Implement in MCP Server**

Add to `MCPServer._define_tools()`:

```python
{
    "name": "get_restaurant_reviews",
    "description": "Get customer reviews for a specific restaurant",
    "inputSchema": {
        "type": "object",
        "properties": {
            "restaurant_id": {"type": "string"},
            "limit": {"type": "integer"}
        },
        "required": ["restaurant_id"]
    }
}
```

**Step 3: Implement Tool Handler**

Add to `MCPServer.call_tool()`:

```python
def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if tool_name == "get_restaurant_reviews":
        return self._get_restaurant_reviews(arguments)
    # ... other tools
```

**Step 4: Implement Tool Logic**

```python
def _get_restaurant_reviews(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
    restaurant_id = arguments.get("restaurant_id")
    limit = arguments.get("limit", 5)

    # Get reviews from database
    reviews = self.database.get_reviews(restaurant_id, limit)

    if not reviews:
        return {
            "content": [{
                "type": "text",
                "text": f"No reviews found for restaurant {restaurant_id}"
            }]
        }

    # Format reviews
    import json
    reviews_data = [
        {
            "rating": r.rating,
            "comment": r.comment,
            "date": r.date,
            "customer": r.customer_name
        }
        for r in reviews
    ]

    return {
        "content": [{
            "type": "text",
            "text": f"Reviews for restaurant {restaurant_id}:\n\n{json.dumps(reviews_data, indent=2)}"
        }]
    }
```

**Step 5: Test the Tool**

```python
# The LLM will now automatically use this tool when appropriate
User: "Show me reviews for Bella Italia"
Agent: [Calls get_restaurant_reviews tool and displays results]
```

---

## How the Agent Loop Works

### Agent Loop Pseudocode

```python
def process_message(user_message):
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # Loop until we get a final text response
    max_iterations = 5
    for iteration in range(max_iterations):
        # Call LLM with tools and history
        response = llm.create_chat_completion(
            messages=conversation_history,
            tools=TOOLS
        )

        # Check if LLM wants to call tools
        if response.has_tool_calls():
            # Add assistant message with tool calls
            conversation_history.append({
                "role": "assistant",
                "tool_calls": response.tool_calls
            })

            # Execute each tool
            for tool_call in response.tool_calls:
                result = execute_tool(
                    tool_call.name,
                    tool_call.arguments
                )

                # Add tool result to history
                conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            # Continue loop to get final response
            continue
        else:
            # No tool calls, stream final response
            for chunk in llm.stream_response():
                yield chunk
            break
```

### Multi-Turn Example

**Turn 1: Search**

```
User: "Find Italian restaurants"
LLM: [Calls search_restaurants]
Tool: [Returns 3 restaurants]
```

**Turn 2: Availability**

```
LLM: "I found 3 restaurants. Let me check availability..."
LLM: [Calls get_availability for each]
Tool: [Returns availability status]
```

**Turn 3: Final Response**

```
LLM: "Here are the available restaurants:
      1. Bella Italia - Available at 7pm
      2. Pasta Paradise - Available at 8pm
      Would you like to make a reservation?"
```

### Parallel Tool Calls

The LLM can suggest multiple tools at once:

```python
{
    "tool_calls": [
        {
            "id": "call_1",
            "function": {
                "name": "get_availability",
                "arguments": '{"restaurant_id": "rest_001", ...}'
            }
        },
        {
            "id": "call_2",
            "function": {
                "name": "get_availability",
                "arguments": '{"restaurant_id": "rest_002", ...}'
            }
        }
    ]
}
```

The agent executes all tools and adds all results before calling the LLM again.

---

## Debugging Tips

### 1. Enable Logging

Add logging to see tool calls:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def _execute_tool(self, tool_name, arguments):
    logger.debug(f"Executing tool: {tool_name}")
    logger.debug(f"Arguments: {arguments}")

    result = # ... execute tool

    logger.debug(f"Result: {result}")
    return result
```

### 2. Inspect Conversation History

Print the conversation history to see what the LLM sees:

```python
import json

def process_message(self, user_message):
    # ... add user message

    print("=== Conversation History ===")
    print(json.dumps(self.conversation_history, indent=2))

    # ... continue processing
```

### 3. Test Tools Independently

Test MCP Server tools directly:

```python
# Test search_restaurants
request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "search_restaurants",
        "arguments": {
            "cuisine": "Italian",
            "location": "Downtown"
        }
    }
}

response = mcp_server.handle_request(request)
print(json.dumps(response, indent=2))
```

### 4. Check Tool Schema Validation

Ensure tool schemas are valid:

```python
import jsonschema

# Validate against OpenAI function calling schema
schema = {
    "type": "object",
    "properties": {
        "type": {"const": "function"},
        "function": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "parameters": {"type": "object"}
            },
            "required": ["name", "description", "parameters"]
        }
    },
    "required": ["type", "function"]
}

for tool in TOOLS:
    jsonschema.validate(tool, schema)
    print(f"✓ {tool['function']['name']} is valid")
```

### 5. Common Issues

**Issue: LLM doesn't call tools**

- Check tool descriptions are clear and specific
- Ensure parameters are well-documented
- Verify tools are included in the request

**Issue: Tool execution fails**

- Check MCP Server error handling
- Verify tool arguments match schema
- Ensure database has required data

**Issue: Infinite loop**

- Check max_iterations limit
- Ensure LLM eventually returns text response
- Verify tool results are properly formatted

**Issue: Wrong tool called**

- Improve tool descriptions
- Add examples in descriptions
- Make parameter descriptions more specific

---

## Best Practices

### Tool Design

1. **Single Responsibility**: Each tool should do one thing well
2. **Clear Descriptions**: Help the LLM understand when to use the tool
3. **Flexible Parameters**: Make parameters optional when possible
4. **Structured Output**: Return consistent, well-formatted results
5. **Error Handling**: Return helpful error messages

### Schema Design

1. **Descriptive Names**: Use clear, action-oriented names
2. **Detailed Descriptions**: Explain what the tool does and when to use it
3. **Parameter Descriptions**: Describe format, constraints, and examples
4. **Required vs Optional**: Only mark truly required parameters

### Agent Loop

1. **Iteration Limit**: Prevent infinite loops (5-10 iterations)
2. **Context Management**: Keep conversation history focused
3. **Error Recovery**: Handle tool failures gracefully
4. **Status Updates**: Inform users when tools are executing

### Testing

1. **Unit Test Tools**: Test each tool independently
2. **Integration Tests**: Test agent + MCP Server interaction
3. **End-to-End Tests**: Test complete conversation flows
4. **Edge Cases**: Test with invalid inputs and error scenarios

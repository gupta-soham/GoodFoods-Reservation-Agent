# MCP Protocol Implementation

Documentation for the Model Context Protocol (MCP) implementation in GoodFoods Reservation Agent.

## Overview

The Model Context Protocol (MCP) is a standardized protocol for AI-tool interactions using JSON-RPC 2.0. It provides a consistent way for AI models to discover and execute tools, and access resources.

## JSON-RPC 2.0 Message Format

### Request Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "method_name",
  "params": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

### Response Format (Success)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "data": "result_data"
  }
}
```

### Response Format (Error)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Method not found"
  }
}
```

## MCP Methods

### tools/list

List all available tools.

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "search_restaurants",
        "description": "Search for restaurants based on criteria",
        "inputSchema": {
          "type": "object",
          "properties": {
            "cuisine": { "type": "string" },
            "location": { "type": "string" }
          }
        }
      }
    ]
  }
}
```

### tools/call

Execute a specific tool.

**Request:**

```json
{
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
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Found 3 restaurant(s):\n\n[...]"
      }
    ]
  }
}
```

### resources/list

List all available resources.

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/list",
  "params": {}
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resources": [
      {
        "uri": "restaurants://list",
        "name": "All Restaurants",
        "description": "List of all available restaurants",
        "mimeType": "application/json"
      }
    ]
  }
}
```

### resources/read

Read a specific resource.

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/read",
  "params": {
    "uri": "restaurants://rest_001"
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "contents": [
      {
        "uri": "restaurants://rest_001",
        "mimeType": "application/json",
        "text": "{\"id\": \"rest_001\", \"name\": \"Bella Italia\", ...}"
      }
    ]
  }
}
```

## Tool Definitions

### Tool Schema

```json
{
  "name": "tool_name",
  "description": "What the tool does",
  "inputSchema": {
    "type": "object",
    "properties": {
      "param1": {
        "type": "string",
        "description": "Parameter description"
      }
    },
    "required": ["param1"]
  }
}
```

### Implemented Tools

1. **search_restaurants** - Search for restaurants
2. **get_availability** - Check restaurant availability
3. **make_reservation** - Create a reservation
4. **cancel_reservation** - Cancel a reservation
5. **get_recommendations** - Get restaurant recommendations

## Resource Definitions

### Resource Schema

```json
{
  "uri": "scheme://identifier",
  "name": "Resource Name",
  "description": "Resource description",
  "mimeType": "application/json"
}
```

### Implemented Resources

1. **restaurants://list** - All restaurants
2. **restaurants://{id}** - Specific restaurant details

## Error Codes

Standard JSON-RPC 2.0 error codes:

- `-32700`: Parse error
- `-32600`: Invalid request
- `-32601`: Method not found
- `-32602`: Invalid params
- `-32603`: Internal error

## Implementation Example

```python
class MCPServer:
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            if method == "tools/list":
                result = self.list_tools()
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                result = self.call_tool(tool_name, arguments)
            elif method == "resources/list":
                result = self.list_resources()
            elif method == "resources/read":
                uri = params.get("uri")
                result = self.read_resource(uri)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
```

## References

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)

# API Reference

Complete API documentation for the GoodFoods Reservation Agent.

## Table of Contents

- [ReservationAgent API](#reservationagent-api)
- [MCPServer API](#mcpserver-api)
- [RestaurantDatabase API](#restaurantdatabase-api)
- [OpenRouterClient API](#openrouterclient-api)
- [Tool Schemas](#tool-schemas)

---

## ReservationAgent API

The main agent class that orchestrates conversation and tool calling.

### Class: `ReservationAgent`

```python
from agent.agent import ReservationAgent
from agent.openrouter_client import OpenRouterClient
from mcp_server.server import MCPServer

agent = ReservationAgent(mcp_server, openrouter_client)
```

#### Constructor

**Parameters:**

- `mcp_server` (MCPServer): MCP Server instance for tool execution
- `openrouter_client` (OpenRouterClient): OpenRouter client for LLM interactions

#### Methods

##### `process_message(user_message: str) -> Generator[str, None, None]`

Process a user message and yield response chunks.

**Parameters:**

- `user_message` (str): The user's input message

**Yields:**

- `str`: Response chunks (text or status updates)

**Example:**

```python
for chunk in agent.process_message("Find Italian restaurants in Downtown"):
    print(chunk, end="", flush=True)
```

**Response Flow:**

1. Status updates: `"Using tools: search_restaurants..."`
2. Content chunks: Streamed text response

---

## MCPServer API

JSON-RPC 2.0 server providing restaurant tools and resources.

### Class: `MCPServer`

```python
from mcp_server.server import MCPServer
from database.restaurant_db import RestaurantDatabase

server = MCPServer(database)
```

#### Constructor

**Parameters:**

- `database` (RestaurantDatabase): Database instance for data operations

#### Methods

##### `handle_request(request: Dict[str, Any]) -> Dict[str, Any]`

Handle incoming JSON-RPC 2.0 requests.

**Parameters:**

- `request` (dict): JSON-RPC request object

**Returns:**

- `dict`: JSON-RPC response object

**Example Request:**

```python
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

response = server.handle_request(request)
```

**Example Response:**

```python
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

### Endpoints

#### `tools/list`

List all available tools.

**Request:**

```python
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
}
```

**Response:**

```python
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "tools": [
            {
                "name": "search_restaurants",
                "description": "Search for restaurants based on criteria",
                "inputSchema": {...}
            },
            ...
        ]
    }
}
```

#### `tools/call`

Execute a specific tool.

**Request:**

```python
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "make_reservation",
        "arguments": {
            "restaurant_id": "rest_001",
            "date": "2025-11-15",
            "time": "19:00",
            "party_size": 4,
            "customer_name": "John Smith"
        }
    }
}
```

**Response:**

```python
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "content": [
            {
                "type": "text",
                "text": "Reservation confirmed!\n\n{...}"
            }
        ]
    }
}
```

#### `resources/list`

List all available resources.

**Request:**

```python
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "resources/list",
    "params": {}
}
```

**Response:**

```python
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
            },
            ...
        ]
    }
}
```

#### `resources/read`

Read a specific resource.

**Request:**

```python
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "resources/read",
    "params": {
        "uri": "restaurants://rest_001"
    }
}
```

---

## RestaurantDatabase API

In-memory database for managing restaurants and reservations.

### Class: `RestaurantDatabase`

```python
from database.restaurant_db import RestaurantDatabase

db = RestaurantDatabase()
```

#### Methods

##### `add_restaurant(restaurant: Restaurant) -> None`

Add a restaurant to the database.

**Parameters:**

- `restaurant` (Restaurant): Restaurant object to add

**Example:**

```python
from database.models import Restaurant

restaurant = Restaurant(
    id="rest_001",
    name="Bella Italia",
    cuisine="Italian",
    location="Downtown",
    address="123 Main St",
    seating_capacity=50,
    operating_hours={"mon-fri": "11:00-22:00"},
    price_range="$$",
    rating=4.5,
    description="Authentic Italian cuisine"
)

db.add_restaurant(restaurant)
```

##### `get_restaurant(restaurant_id: str) -> Optional[Restaurant]`

Retrieve a restaurant by ID.

**Parameters:**

- `restaurant_id` (str): Unique identifier of the restaurant

**Returns:**

- `Restaurant | None`: Restaurant object if found, None otherwise

**Example:**

```python
restaurant = db.get_restaurant("rest_001")
if restaurant:
    print(f"Found: {restaurant.name}")
```

##### `search_restaurants(...) -> List[Restaurant]`

Search for restaurants based on criteria.

**Parameters:**

- `cuisine` (str, optional): Filter by cuisine type
- `location` (str, optional): Filter by location
- `party_size` (int, optional): Filter by seating capacity
- `date` (str, optional): Filter by availability on date (YYYY-MM-DD)
- `time` (str, optional): Filter by availability at time (HH:MM)

**Returns:**

- `List[Restaurant]`: List of matching restaurants

**Example:**

```python
results = db.search_restaurants(
    cuisine="Italian",
    location="Downtown",
    party_size=4,
    date="2025-11-15",
    time="19:00"
)
```

##### `check_availability(...) -> bool`

Check if a restaurant can accommodate a party.

**Parameters:**

- `restaurant_id` (str): ID of the restaurant
- `date` (str): Reservation date (YYYY-MM-DD)
- `time` (str): Reservation time (HH:MM)
- `party_size` (int): Number of guests

**Returns:**

- `bool`: True if available, False otherwise

**Example:**

```python
is_available = db.check_availability(
    restaurant_id="rest_001",
    date="2025-11-15",
    time="19:00",
    party_size=4
)
```

##### `create_reservation(...) -> Optional[Reservation]`

Create a new reservation.

**Parameters:**

- `restaurant_id` (str): ID of the restaurant
- `date` (str): Reservation date (YYYY-MM-DD)
- `time` (str): Reservation time (HH:MM)
- `party_size` (int): Number of guests
- `customer_name` (str): Name of the customer

**Returns:**

- `Reservation | None`: Reservation object if successful, None if unavailable

**Example:**

```python
reservation = db.create_reservation(
    restaurant_id="rest_001",
    date="2025-11-15",
    time="19:00",
    party_size=4,
    customer_name="John Smith"
)

if reservation:
    print(f"Reservation ID: {reservation.id}")
```

##### `cancel_reservation(reservation_id: str) -> bool`

Cancel an existing reservation.

**Parameters:**

- `reservation_id` (str): ID of the reservation to cancel

**Returns:**

- `bool`: True if successful, False if not found

**Example:**

```python
success = db.cancel_reservation("abc-123-def")
```

---

## OpenRouterClient API

Client for interacting with OpenRouter's LLM API.

### Class: `OpenRouterClient`

```python
from agent.openrouter_client import OpenRouterClient

client = OpenRouterClient(api_key="sk-or-...")
```

#### Constructor

**Parameters:**

- `api_key` (str, optional): OpenRouter API key (defaults to OPENROUTER_API_KEY env var)

#### Methods

##### `create_chat_completion(...) -> Any`

Create a chat completion with optional tool calling.

**Parameters:**

- `messages` (List[Dict]): List of message objects
- `tools` (List[Dict], optional): List of tool definitions
- `stream` (bool): Whether to stream the response (default: False)

**Returns:**

- `dict | Generator`: Response object or generator for streaming

**Example (Non-streaming):**

```python
response = client.create_chat_completion(
    messages=[
        {"role": "user", "content": "Hello!"}
    ],
    stream=False
)

print(response["choices"][0]["message"]["content"])
```

**Example (Streaming):**

```python
stream = client.create_chat_completion(
    messages=[
        {"role": "user", "content": "Hello!"}
    ],
    stream=True
)

for chunk in stream:
    if "choices" in chunk:
        delta = chunk["choices"][0].get("delta", {})
        content = delta.get("content", "")
        print(content, end="", flush=True)
```

---

## Tool Schemas

All tools follow the OpenAI function calling specification.

### search_restaurants

Search for restaurants based on criteria.

**Schema:**

```python
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
}
```

### get_availability

Check availability for a specific restaurant.

**Schema:**

```python
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
}
```

### make_reservation

Create a new reservation.

**Schema:**

```python
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
}
```

### cancel_reservation

Cancel an existing reservation.

**Schema:**

```python
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
}
```

### get_recommendations

Get personalized restaurant recommendations.

**Schema:**

```python
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
```

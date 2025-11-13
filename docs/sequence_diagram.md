# GoodFoods Reservation Agent - Mermaid Sequence Diagram

## Complete User Interaction Flow

```mermaid
sequenceDiagram
    participant User
    participant StreamlitUI as Streamlit UI
    participant Agent as Reservation Agent
    participant Cerebras as Cerebras LLM
    participant MCPServer as MCP Server
    participant Database as In-Memory DB

    User->>StreamlitUI: "Find Italian restaurants for 4 people tonight"
    StreamlitUI->>StreamlitUI: Update session state
    StreamlitUI->>Agent: Process user message
    
    Agent->>Agent: Build conversation context
    Agent->>Cerebras: Send message with context
    Cerebras->>Agent: Response with tool calls
    
    Agent->>Agent: Parse tool calls
    Agent->>MCPServer: search_restaurants(cuisine="Italian", party_size=4)
    MCPServer->>Database: Query restaurants
    Database->>MCPServer: Return matching restaurants
    MCPServer->>Agent: Tool execution result
    
    Agent->>Cerebras: Generate response with results
    Cerebras->>Agent: Formatted response
    Agent->>StreamlitUI: Stream response
    StreamlitUI->>User: "Found 3 Italian restaurants: Bella Italia, Mario's, Giuseppe's"
    
    User->>StreamlitUI: "Check availability at Bella Italia for 7pm"
    StreamlitUI->>Agent: Process availability request
    Agent->>Cerebras: Analyze request
    Cerebras->>Agent: Tool call for availability
    
    Agent->>MCPServer: get_availability(restaurant_id="bella-italia", time="19:00")
    MCPServer->>Database: Check availability
    Database->>MCPServer: Return availability status
    MCPServer->>Agent: Availability result
    
    Agent->>Cerebras: Generate availability response
    Cerebras->>Agent: Formatted response
    Agent->>StreamlitUI: Stream response
    StreamlitUI->>User: "Bella Italia is available at 7:30pm. Shall I book it?"
    
    User->>StreamlitUI: "Yes, book it for John Smith"
    StreamlitUI->>Agent: Process reservation request
    Agent->>Cerebras: Analyze booking request
    Cerebras->>Agent: Tool call for reservation
    
    Agent->>MCPServer: make_reservation(restaurant_id="bella-italia", customer_name="John Smith")
    MCPServer->>Database: Create reservation
    Database->>MCPServer: Return reservation ID
    MCPServer->>Agent: Reservation confirmation
    
    Agent->>Cerebras: Generate confirmation response
    Cerebras->>Agent: Formatted confirmation
    Agent->>StreamlitUI: Stream confirmation
    StreamlitUI->>User: "Reservation confirmed! ID: RES-123. Bella Italia, 7:30pm for 4 people."
```

## Tool-Specific Sequence Flows

### Search Restaurants Flow
```mermaid
sequenceDiagram
    participant Agent
    participant Cerebras as Cerebras LLM
    participant MCP as MCP Server
    participant DB as Database

    Agent->>Cerebras: "Find Italian restaurants"
    Cerebras->>Agent: search_restaurants tool call
    Agent->>MCP: search_restaurants(cuisine="Italian", location="Downtown")
    MCP->>DB: SELECT * FROM restaurants WHERE cuisine='Italian'
    DB->>MCP: Restaurant list
    MCP->>Agent: Formatted restaurant results
    Agent->>Cerebras: Include results in response
    Cerebras->>Agent: "Found 3 Italian restaurants..."
```

### Make Reservation Flow
```mermaid
sequenceDiagram
    participant Agent
    participant Cerebras as Cerebras LLM
    participant MCP as MCP Server
    participant DB as Database

    Agent->>Cerebras: "Book table for John Smith"
    Cerebras->>Agent: make_reservation tool call
    Agent->>MCP: make_reservation(restaurant_id, customer_name, date, time)
    MCP->>DB: Check availability
    DB->>MCP: Available slots
    MCP->>DB: INSERT reservation
    DB->>MCP: Reservation ID
    MCP->>Agent: Confirmation with ID
    Agent->>Cerebras: Include confirmation in response
    Cerebras->>Agent: "Reservation confirmed! ID: RES-123"
```

### Cancel Reservation Flow
```mermaid
sequenceDiagram
    participant Agent
    participant Cerebras as Cerebras LLM
    participant MCP as MCP Server
    participant DB as Database

    Agent->>Cerebras: "Cancel reservation RES-123"
    Cerebras->>Agent: cancel_reservation tool call
    Agent->>MCP: cancel_reservation(reservation_id="RES-123")
    MCP->>DB: UPDATE reservation SET status='cancelled'
    DB->>MCP: Cancellation confirmed
    MCP->>Agent: Cancellation result
    Agent->>Cerebras: Include result in response
    Cerebras->>Agent: "Reservation RES-123 has been cancelled"
```

## Error Handling Flow
```mermaid
sequenceDiagram
    participant User
    participant StreamlitUI as Streamlit UI
    participant Agent as Reservation Agent
    participant Cerebras as Cerebras LLM
    participant MCPServer as MCP Server

    User->>StreamlitUI: "Book table at non-existent restaurant"
    StreamlitUI->>Agent: Process request
    Agent->>Cerebras: Analyze request
    Cerebras->>Agent: make_reservation tool call
    Agent->>MCPServer: make_reservation(restaurant_id="invalid")
    MCPServer->>Agent: Error: Restaurant not found
    Agent->>Cerebras: Include error in context
    Cerebras->>Agent: "I couldn't find that restaurant. Here are available options..."
    Agent->>StreamlitUI: Stream error response
    StreamlitUI->>User: Helpful error message with alternatives
```

## MCP Protocol Communication
```mermaid
sequenceDiagram
    participant Agent as Agent (Client)
    participant MCP as MCP Server

    Agent->>MCP: JSON-RPC Request<br/>{"method": "tools/call", "params": {...}}
    MCP->>MCP: Validate request
    MCP->>MCP: Route to appropriate tool
    MCP->>MCP: Execute tool logic
    MCP->>MCP: Format response
    MCP->>Agent: JSON-RPC Response<br/>{"result": {"content": [...]}}
    Agent->>Agent: Process tool result
```

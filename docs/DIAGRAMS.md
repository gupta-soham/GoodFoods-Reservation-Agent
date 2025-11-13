# 🏗️ GoodFoods Reservation Agent - Architecture & Flow Diagrams

This document provides comprehensive visual documentation of the GoodFoods Reservation Agent architecture, including system components, data flow, tool calling mechanisms, and deployment structure.

## 📋 Table of Contents

1. [System Architecture Overview](#system-architecture-overview)
2. [Tool Calling Flow](#tool-calling-flow)
3. [Component Interaction](#component-interaction)
4. [MCP Protocol Communication](#mcp-protocol-communication)
5. [Complete Conversation Flow](#complete-conversation-flow)
6. [Tool Schema & Database Operations](#tool-schema--database-operations)
7. [Deployment Architecture](#deployment-architecture)
8. [Key Components Explained](#key-components-explained)
9. [Tool Calling Mechanisms](#tool-calling-mechanisms)

## 🏛️ System Architecture Overview

![System Architecture](generated-diagrams/system_architecture.png)

### Architecture Layers

**Frontend Layer**
- **User**: End users interacting with the system
- **Streamlit UI (app.py)**: Web-based chat interface providing conversational interaction

**Agent Layer**
- **Reservation Agent (agent.py)**: Core conversational AI agent with tool calling capabilities
- **Cerebras Cloud LLM API**: External LLM service providing natural language processing

**MCP Protocol Layer**
- **MCP Server (server.py)**: Model Context Protocol server implementing JSON-RPC 2.0
- **Tool Registry**: Collection of available tools for restaurant operations

**Database Layer**
- **Restaurant DB (In-Memory)**: PostgreSQL-style in-memory database
- **Data Models**: Restaurant and Reservation data structures

## 🔄 Tool Calling Flow

![Tool Calling Flow](generated-diagrams/tool_calling_flow.png)

### Tool Execution Process

1. **User Query Processing**: Natural language input is processed by the agent
2. **LLM Analysis**: Cerebras LLM determines if tool calling is required
3. **Tool Selection**: Based on user intent, appropriate tools are selected:
   - `search_restaurants`: Find restaurants matching criteria
   - `get_availability`: Check restaurant availability
   - `make_reservation`: Create new reservations
   - `get_recommendations`: Get personalized suggestions
   - `cancel_reservation`: Cancel existing reservations

4. **Database Operations**: Tools interact with the restaurant database
5. **Response Generation**: Results are formatted and returned to the user

## 🔗 Component Interaction

![Component Interaction](generated-diagrams/component_interaction.png)

### Component Relationships

**Streamlit Frontend Components**:
- Chat Interface: Main user interaction point
- Session State: Maintains conversation context
- UI Config: Interface configuration and styling

**Agent Layer Components**:
- ReservationAgent: Core agent logic and orchestration
- Tool Schemas: Definitions of available tools and parameters
- Conversation Context: Maintains chat history and state
- CerebrasClient: API client for LLM communication
- API Config: Cerebras API configuration

**MCP Server Components**:
- MCPServer: Main server implementing MCP protocol
- Tool Registry: Available tool definitions
- Resource Registry: Available resource definitions

**Database Components**:
- RestaurantDatabase: Main database manager
- Restaurant Model: Restaurant data structure
- Reservation Model: Reservation data structure
- Sample Data: Seed data for testing

## 📡 MCP Protocol Communication

![MCP Protocol Flow](generated-diagrams/mcp_protocol_flow.png)

### MCP Protocol Implementation

The system implements the Model Context Protocol (MCP) using JSON-RPC 2.0:

**Request Format**:
```json
{
  "method": "tools/call",
  "params": {
    "name": "search_restaurants",
    "arguments": {
      "cuisine": "Italian",
      "location": "Downtown",
      "party_size": 4
    }
  }
}
```

**Response Format**:
```json
{
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Found 3 Italian restaurants..."
      }
    ]
  }
}
```

### Tool Routing

The MCP Server routes method calls to appropriate tools:
- Method parsing and validation
- Parameter extraction and validation
- Tool execution with database interaction
- Result formatting and response generation

## 💬 Complete Conversation Flow

![Conversation Flow](generated-diagrams/conversation_flow.png)

### Conversation Lifecycle

1. **User Input**: User sends message through Streamlit interface
2. **Session Management**: Streamlit updates session state and context
3. **Agent Processing**: 
   - Context building from conversation history
   - LLM request to Cerebras with conversation context
   - Tool calling decision based on LLM response
4. **Tool Execution** (if needed):
   - Parse tool calls from LLM response
   - Execute MCP tools with database interaction
   - Format results for response generation
5. **Response Generation**: Generate and stream response to user
6. **Continuation**: User can continue conversation or end session

## 🛠️ Tool Schema & Database Operations

![Tool Schema & Database](generated-diagrams/tool_schema_database.png)

### Available Tools

#### 1. search_restaurants
**Purpose**: Find restaurants based on search criteria
**Parameters**:
- `cuisine` (string): Type of cuisine (Italian, Chinese, etc.)
- `location` (string): Geographic area (Downtown, Midtown, etc.)
- `party_size` (int): Number of guests
- `date` (string): Reservation date (YYYY-MM-DD)
- `time` (string): Reservation time (HH:MM)

#### 2. get_availability
**Purpose**: Check restaurant availability for specific time
**Parameters**:
- `restaurant_id` (string): Unique restaurant identifier
- `date` (string): Date in YYYY-MM-DD format
- `time` (string): Time in HH:MM format
- `party_size` (int): Number of guests

#### 3. make_reservation
**Purpose**: Create new restaurant reservation
**Parameters**:
- `restaurant_id` (string): Restaurant identifier
- `date` (string): Reservation date
- `time` (string): Reservation time
- `party_size` (int): Number of guests
- `customer_name` (string): Customer name

#### 4. cancel_reservation
**Purpose**: Cancel existing reservation
**Parameters**:
- `reservation_id` (string): Unique reservation identifier

#### 5. get_recommendations
**Purpose**: Get personalized restaurant recommendations
**Parameters**:
- `preferences` (object): User preferences and criteria
- `location` (string): Preferred location
- `party_size` (int): Number of guests

### Database Models

#### Restaurant Model
- `id`: Unique identifier
- `name`: Restaurant name
- `cuisine`: Cuisine type
- `location`: Geographic location
- `address`: Full address
- `seating_capacity`: Maximum capacity
- `operating_hours`: Hours of operation
- `price_range`: Price indicator ($-$$$$)
- `rating`: Customer rating (1.0-5.0)

#### Reservation Model
- `id`: Unique identifier
- `restaurant_id`: Associated restaurant
- `date`: Reservation date
- `time`: Reservation time
- `party_size`: Number of guests
- `customer_name`: Customer name
- `created_at`: Creation timestamp
- `status`: Reservation status

## 🚀 Deployment Architecture

![Deployment Architecture](generated-diagrams/deployment_architecture.png)

### Deployment Components

**Application Server**:
- Local server running on localhost:8501
- Python virtual environment with all dependencies
- Application components running in isolated environment

**Application Components**:
- Streamlit App: Web interface server
- Agent Module: Core AI agent logic
- MCP Server: Protocol server for tool calling
- Database Module: In-memory database management

**Configuration**:
- `.env`: Environment variables (Cerebras API key)
- `.streamlit/config.toml`: Streamlit configuration

**External Services**:
- Cerebras Cloud API: LLM service endpoint

**Local Storage**:
- Application files and static assets
- Session data and conversation history

## 🔧 Key Components Explained

### 1. Streamlit Frontend (app.py)
- **Purpose**: Provides web-based chat interface
- **Features**: Real-time messaging, session management, responsive design
- **Technology**: Streamlit framework with custom CSS styling

### 2. Reservation Agent (agent/agent.py)
- **Purpose**: Core conversational AI agent
- **Features**: Tool calling, conversation context, response streaming
- **Technology**: Custom agent loop with Cerebras LLM integration

### 3. Cerebras Client (agent/cerebras_client.py)
- **Purpose**: API client for Cerebras Cloud LLM
- **Features**: Streaming responses, error handling, rate limiting
- **Technology**: HTTP client with async support

### 4. MCP Server (mcp_server/server.py)
- **Purpose**: Implements Model Context Protocol for tool calling
- **Features**: JSON-RPC 2.0, tool registry, resource management
- **Technology**: Custom MCP implementation

### 5. Restaurant Database (database/restaurant_db.py)
- **Purpose**: In-memory database for restaurant and reservation data
- **Features**: CRUD operations, search functionality, data persistence
- **Technology**: Python data structures with PostgreSQL-like interface

## ⚙️ Tool Calling Mechanisms

### 1. Tool Definition
Tools are defined with OpenAI-compatible schemas:
```python
{
    "type": "function",
    "function": {
        "name": "search_restaurants",
        "description": "Search for restaurants based on criteria",
        "parameters": {
            "type": "object",
            "properties": {
                "cuisine": {"type": "string"},
                "location": {"type": "string"}
            }
        }
    }
}
```

### 2. Tool Execution Flow
1. **LLM Decision**: Cerebras LLM decides to call tools based on user input
2. **Tool Parsing**: Agent parses tool calls from LLM response
3. **MCP Communication**: Agent sends tool call to MCP Server
4. **Tool Execution**: MCP Server executes tool with database interaction
5. **Result Processing**: Results are formatted and returned to agent
6. **Response Generation**: Agent incorporates results into final response

### 3. Error Handling
- **Validation**: Parameter validation before tool execution
- **Fallbacks**: Graceful degradation when tools fail
- **Retry Logic**: Automatic retry for transient failures
- **User Feedback**: Clear error messages for users

## 📊 Performance Characteristics

### Response Times
- **LLM Calls**: ~1-3 seconds (Cerebras fast inference)
- **Tool Execution**: ~100-500ms (in-memory database)
- **Total Response**: ~2-4 seconds end-to-end

### Scalability
- **Concurrent Users**: Limited by Streamlit single-process model
- **Database**: In-memory storage suitable for demo/development
- **API Limits**: Dependent on Cerebras API rate limits

### Resource Usage
- **Memory**: ~100-200MB for application
- **CPU**: Low usage, mostly I/O bound
- **Network**: Minimal except for LLM API calls

## 🔮 Future Enhancements

### Potential Improvements
1. **Database**: Migrate to persistent database (PostgreSQL, MongoDB)
2. **Caching**: Implement response caching for common queries
3. **Authentication**: Add user authentication and personalization
4. **Real-time**: WebSocket support for real-time updates
5. **Monitoring**: Add logging, metrics, and health checks
6. **Deployment**: Container-based deployment with orchestration

### Scalability Considerations
1. **Multi-process**: Deploy with multiple Streamlit processes
2. **Load Balancing**: Add load balancer for high availability
3. **Database Scaling**: Implement database clustering
4. **API Optimization**: Batch API calls and implement caching
5. **CDN**: Use CDN for static assets and improved performance

## 📈 Mermaid Sequence Diagrams

For detailed interaction flows, see the [Mermaid Sequence Diagrams](mermaid_sequence_diagram.md) which include:

- **Complete User Interaction Flow**: End-to-end conversation flow from user query to reservation confirmation
- **Tool-Specific Flows**: Individual flows for search, reservation, and cancellation operations
- **Error Handling Flow**: How the system gracefully handles errors and provides user feedback
- **MCP Protocol Communication**: Low-level JSON-RPC 2.0 protocol interactions

## 🔧 Diagram Generation Code

All diagram generation code is stored in [`diagram_generators.py`](diagram_generators.py) for easy modifications and regeneration:

```python
# Generate individual diagrams
from diagram_generators import generate_system_architecture
generate_system_architecture()

# Generate all diagrams at once
from diagram_generators import generate_all_diagrams
generate_all_diagrams()
```

---

This architecture provides a solid foundation for a conversational AI restaurant reservation system with clear separation of concerns, robust tool calling capabilities, and room for future enhancements.

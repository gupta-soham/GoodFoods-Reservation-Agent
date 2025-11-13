# 🍽️ GoodFoods Reservation Agent

A conversational AI agent for restaurant discovery and reservation management, built with Streamlit and powered by Cerebras Cloud API.

## Features

- **Natural Language Search**: Find restaurants using conversational queries about cuisine, location, party size, and timing
- **Smart Recommendations**: Get personalized restaurant suggestions based on your preferences
- **Real-time Availability**: Check restaurant availability and get alternative time slots
- **Easy Reservations**: Make and cancel reservations through natural conversation
- **Streaming Responses**: Experience smooth, real-time AI responses with adjustable speed (Slow/Normal/Fast)
- **Minimal Thinking Indicator**: Clean post-tool animation showing AI is processing
- **Tool Calling**: Leverages Model Context Protocol (MCP) for structured tool execution
- **Fast Inference**: Powered by Cerebras Cloud for ultra-fast LLM responses

## UI Features

### Speed Control

In the top-right corner, use the "Speed" dropdown to control streaming speed:

- **Slow**: Leisurely, easy-to-read word-by-word streaming
- **Normal** (default): Balanced streaming speed for natural conversation
- **Fast**: Quick streaming for faster interactions

### Tool Calling Visualization

When the agent uses tools, a "View tool calls" expander appears with:

- Live, pulsing badge for the currently executing tool
- Tool arguments displayed as formatted JSON
- Tool results rendered with full Markdown support

### Thinking Indicator

After tools complete execution:

- A minimal "Thinking …" indicator appears briefly
- Automatically disappears when the assistant begins streaming the response
- Provides visual feedback during the transition from tool execution to response generation

All assistant responses and tool results support full Markdown formatting, including code blocks, lists, tables, and emphasis.

## Architecture

The application consists of four main components:

1. **Streamlit Frontend** (`app.py`): Clean, professional chat interface
2. **Reservation Agent** (`agent/`): Custom agent loop with tool calling capabilities using Cerebras llama-3.3-70b
3. **MCP Server** (`mcp_server/`): JSON-RPC 2.0 server providing restaurant tools and resources
4. **Restaurant Database** (`database/`): In-memory database with seed data

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Cerebras API key ([Get one here](https://cloud.cerebras.ai/))

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/gupta-soham/goodfoods-reservation-agent.git
   cd goodfoods-reservation-agent
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and add your Cerebras API key
   CEREBRAS_API_KEY=your_api_key_here
   ```

5. **Test the Cerebras integration (optional)**

   ```bash
   python test_cerebras.py
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

The application will open in your default browser at `http://localhost:8501`

## Usage Guide

### Example Interactions

**Search for restaurants:**

```
User: I'm looking for Italian restaurants in Downtown for 4 people
Agent: [Searches and displays matching restaurants with details]
```

**Check availability:**

```
User: Is Bella Italia available tonight at 7pm for 4 people?
Agent: [Checks availability and suggests alternative times if needed]
```

**Make a reservation:**

```
User: Book a table at Bella Italia for tomorrow at 7pm for 4 people under John Smith
Agent: [Creates reservation and provides confirmation with reservation ID]
```

**Get recommendations:**

```
User: Recommend some highly-rated restaurants with outdoor seating
Agent: [Provides ranked recommendations based on preferences]
```

**Cancel a reservation:**

```
User: Cancel reservation abc-123-def
Agent: [Cancels reservation and confirms]
```

## Project Structure

```
goodfoods-reservation-agent/
├── agent/
│   ├── __init__.py
│   ├── agent.py              # Core agent with tool calling loop
│   └── cerebras_client.py    # Cerebras API client
├── mcp_server/
│   ├── __init__.py
│   └── server.py             # MCP Server implementation
├── database/
│   ├── __init__.py
│   ├── models.py             # Restaurant and Reservation models
│   ├── restaurant_db.py      # In-memory database
│   └── seed_data.py          # Sample restaurant data
├── docs/                     # Additional documentation
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── app.py                    # Main Streamlit application
├── test_cerebras.py          # Test script for Cerebras integration
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── CEREBRAS_MIGRATION.md     # Migration guide
├── .gitignore
└── README.md
```

## Troubleshooting

### API Key Issues

**Problem**: "Cerebras API Key Not Found" error

**Solution**:

- Ensure you've created a `.env` file (not `.env.example`)
- Verify your API key is correctly set: `CEREBRAS_API_KEY=csk-...`
- Restart the Streamlit application after updating `.env`

### Connection Errors

**Problem**: "I'm having trouble connecting to the AI service"

**Solution**:

- Check your internet connection
- Verify your API key is valid at [Cerebras Cloud](https://cloud.cerebras.ai/)
- Check if you have API credits remaining

### Rate Limiting

**Problem**: "We've reached the rate limit"

**Solution**:

- Wait a few moments before making another request
- Consider upgrading your OpenRouter plan for higher limits

### Slow Responses

**Problem**: Responses take a long time

**Solution**:

- Cerebras is known for fast inference, but network latency can affect response times
- Try simplifying your query
- Check your internet connection

## Technology Stack

- **Frontend**: Streamlit 1.28+
- **LLM Provider**: Cerebras Cloud (llama-3.3-70b)
- **Protocol**: Model Context Protocol (MCP) with JSON-RPC 2.0
- **Language**: Python 3.8+
- **SDK**: Cerebras Cloud SDK for Python

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## Documentation

- [API Reference](docs/API_REFERENCE.md) - Detailed API documentation
- [Architecture Guide](docs/ARCHITECTURE.md) - System design and architecture
- [Tool Calling Guide](docs/TOOL_CALLING_GUIDE.md) - How tool calling works
- [MCP Protocol](docs/MCP_PROTOCOL.md) - MCP implementation details
- [Deployment Guide](docs/DEPLOYMENT.md) - Deployment instructions
- [Test Results](docs/TEST_RESULTS.md) - Testing documentation and results
- [Project Summary](PROJECT_COMPLETION_SUMMARY.md) - Complete project overview

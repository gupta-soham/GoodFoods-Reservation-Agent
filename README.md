# 🍽️ GoodFoods Reservation Agent

A conversational AI agent for restaurant discovery and reservation management, built with Streamlit and powered by OpenRouter's LLM API.

## Features

- **Natural Language Search**: Find restaurants using conversational queries about cuisine, location, party size, and timing
- **Smart Recommendations**: Get personalized restaurant suggestions based on your preferences
- **Real-time Availability**: Check restaurant availability and get alternative time slots
- **Easy Reservations**: Make and cancel reservations through natural conversation
- **Streaming Responses**: Experience smooth, real-time AI responses with minimal animations
- **Tool Calling**: Leverages Model Context Protocol (MCP) for structured tool execution

## Architecture

The application consists of four main components:

1. **Streamlit Frontend** (`app.py`): Clean, professional chat interface
2. **Reservation Agent** (`agent/`): Custom agent loop with tool calling capabilities
3. **MCP Server** (`mcp_server/`): JSON-RPC 2.0 server providing restaurant tools and resources
4. **Restaurant Database** (`database/`): In-memory database with seed data

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenRouter API key ([Get one here](https://openrouter.ai/keys))

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

   # Edit .env and add your OpenRouter API key
   OPENROUTER_API_KEY=your_api_key_here
   ```

5. **Run the application**
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
│   └── openrouter_client.py  # OpenRouter API client
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
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── .gitignore
└── README.md
```

## Troubleshooting

### API Key Issues

**Problem**: "OpenRouter API Key Not Found" error

**Solution**:

- Ensure you've created a `.env` file (not `.env.example`)
- Verify your API key is correctly set: `OPENROUTER_API_KEY=sk-or-...`
- Restart the Streamlit application after updating `.env`

### Connection Errors

**Problem**: "I'm having trouble connecting to the AI service"

**Solution**:

- Check your internet connection
- Verify your API key is valid at [OpenRouter](https://openrouter.ai/keys)
- Check if you have API credits remaining

### Rate Limiting

**Problem**: "We've reached the rate limit"

**Solution**:

- Wait a few moments before making another request
- Consider upgrading your OpenRouter plan for higher limits

### Slow Responses

**Problem**: Responses take a long time

**Solution**:

- The free tier model may have slower response times during peak usage
- Try simplifying your query
- Consider using a paid model for faster responses

## Technology Stack

- **Frontend**: Streamlit 1.28+
- **LLM Provider**: OpenRouter (meta-llama/llama-3.3-70b-instruct:free)
- **Protocol**: Model Context Protocol (MCP) with JSON-RPC 2.0
- **Language**: Python 3.8+
- **HTTP Client**: Requests library

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

"""
GoodFoods Reservation Agent - Streamlit Frontend

A conversational AI interface for restaurant discovery and reservation management.
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="GoodFoods Reservation Agent",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for clean, professional, minimal design
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styling */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Clean background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
    }
    
    /* Main content area */
    .main {
        background-color: transparent;
        scroll-behavior: smooth;
        max-width: 900px;
        padding: 2rem 1rem;
    }
    
    /* Title styling */
    h1 {
        color: #1a1a1a !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.02em;
    }
    
    /* Subtitle styling */
    .main p, .main em {
        color: #6b7280 !important;
        font-size: 1.125rem !important;
        font-weight: 400 !important;
        line-height: 1.6 !important;
    }
    
    /* Horizontal rule */
    hr {
        margin: 2rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #e5e7eb, transparent) !important;
    }
    
    /* Chat message container */
    .stChatMessage {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
        animation: slideIn 0.3s ease-out;
        border: 1px solid #f3f4f6;
        transition: all 0.2s ease;
    }
    
    .stChatMessage:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.05);
        transform: translateY(-1px);
    }
    
    /* Slide-in animation */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Chat message content */
    [data-testid="stChatMessageContent"] {
        background-color: transparent;
        color: #1f2937 !important;
    }
    
    [data-testid="stChatMessageContent"] p {
        color: #1f2937 !important;
        font-size: 1rem !important;
        line-height: 1.7 !important;
        margin: 0 !important;
    }
    
    /* User message styling */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]) {
        background: linear-gradient(135deg, #dbeafe 0%, #e0f2fe 100%);
        border-left: 4px solid #3b82f6;
        border: 1px solid #bfdbfe;
    }
    
    /* Assistant message styling */
    .stChatMessage[data-testid="assistant"] {
        background: linear-gradient(135deg, #fef3c7 0%, #fef9e7 100%);
        border-left: 4px solid #f59e0b;
        border: 1px solid #fde68a;
    }
    
    /* Input container */
    .stChatInputContainer {
        border-top: 1px solid #e5e7eb;
        padding-top: 1.5rem;
        background-color: transparent;
        margin-top: 1rem;
    }
    
    /* Input field styling */
    .stChatInputContainer input {
        color: #1f2937 !important;
        font-size: 1rem !important;
        border-radius: 12px !important;
        border: 2px solid #e5e7eb !important;
        padding: 0.875rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stChatInputContainer input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    .stChatInputContainer input::placeholder {
        color: #9ca3af !important;
        opacity: 1 !important;
    }
    
    /* Status expander styling */
    .stStatus {
        background-color: #f0fdf4 !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: 12px !important;
        padding: 0.75rem !important;
        margin: 0.75rem 0 !important;
    }
    
    .stStatus summary {
        color: #15803d !important;
        font-weight: 500 !important;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: #f59e0b transparent transparent transparent !important;
    }
    
    /* Tool call badge */
    .tool-badge {
        display: inline-block;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.375rem 0.75rem;
        border-radius: 8px;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.25rem 0.25rem 0.25rem 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Error message styling */
    .stAlert {
        border-radius: 12px !important;
        border-left-width: 4px !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f3f4f6;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #d1d5db;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #9ca3af;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🍽️ GoodFoods Reservation Agent")
st.markdown("*Your AI assistant for restaurant discovery and reservations*")
st.markdown("---")

# Check for API key
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    st.error("⚠️ **OpenRouter API Key Not Found**")
    st.markdown("""
    Please set up your OpenRouter API key to use this application:
    
    1. Copy `.env.example` to `.env`
    2. Get your API key from [OpenRouter](https://openrouter.ai/keys)
    3. Add your key to the `.env` file: `OPENROUTER_API_KEY=your_key_here`
    4. Restart the application
    """)
    st.stop()

# Initialize components (only once)
@st.cache_resource
def initialize_components():
    """Initialize database, MCP server, client, and agent."""
    from database.restaurant_db import RestaurantDatabase
    from database.seed_data import generate_restaurants
    from mcp_server.server import MCPServer
    from agent.openrouter_client import OpenRouterClient
    from agent.agent import ReservationAgent
    
    # Initialize and seed database
    db = RestaurantDatabase()
    restaurants = generate_restaurants()
    for restaurant in restaurants:
        db.add_restaurant(restaurant)
    
    # Initialize MCP Server
    mcp_server = MCPServer(db)
    
    # Initialize OpenRouter Client
    client = OpenRouterClient(api_key)
    
    # Initialize Agent
    agent = ReservationAgent(mcp_server, client)
    
    return agent

# Initialize agent
try:
    agent = initialize_components()
except Exception as e:
    st.error(f"⚠️ **Initialization Error**: {str(e)}")
    st.stop()

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm your GoodFoods Reservation Agent. I can help you discover restaurants, check availability, make reservations, and get personalized recommendations. How can I assist you today?",
        "tool_calls": []
    })

# Initialize tool calls tracking
if "tool_calls_history" not in st.session_state:
    st.session_state.tool_calls_history = {}

# Implement conversation history limit (last 20 messages)
MAX_MESSAGES = 20
if len(st.session_state.messages) > MAX_MESSAGES:
    # Keep the welcome message and the last 19 messages
    st.session_state.messages = [st.session_state.messages[0]] + st.session_state.messages[-(MAX_MESSAGES-1):]

# Display chat messages
for idx, message in enumerate(st.session_state.messages):
    role = message["role"]
    content = message["content"]
    tool_calls = message.get("tool_calls", [])
    
    with st.chat_message(role):
        # Display tool calls if any
        if tool_calls and len(tool_calls) > 0:
            with st.expander("🔧 View tool calls", expanded=False):
                for tool_call in tool_calls:
                    tool_name = tool_call.get("name", "Unknown")
                    tool_args = tool_call.get("arguments", {})
                    tool_result = tool_call.get("result", "")
                    
                    # Create friendly tool names
                    tool_display = {
                        "search_restaurants": "🔍 Search Restaurants",
                        "get_availability": "📅 Check Availability",
                        "make_reservation": "✅ Make Reservation",
                        "cancel_reservation": "❌ Cancel Reservation",
                        "get_recommendations": "⭐ Get Recommendations"
                    }.get(tool_name, f"🔧 {tool_name}")
                    
                    st.markdown(f"**{tool_display}**")
                    
                    if tool_args:
                        st.json(tool_args, expanded=False)
                    
                    if tool_result:
                        with st.expander("Result", expanded=False):
                            st.text(tool_result[:500] + ("..." if len(tool_result) > 500 else ""))
                    
                    st.markdown("---")
        
        st.markdown(content)

# Chat input
user_input = st.chat_input("Ask me about restaurants, reservations, or recommendations...")

if user_input:
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Append user message to session state
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "tool_calls": []
    })

    # Generate and stream assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        tool_expander_placeholder = st.empty()
        full_response = ""
        tool_calls_data = []
        current_tool_calls = []
        
        try:
            # Process message and stream response
            for chunk in agent.process_message(user_input):
                # Check if this is a tool call data chunk (dict with tool info)
                if isinstance(chunk, dict) and "tool_name" in chunk:
                    tool_calls_data.append(chunk)
                    current_tool_calls.append(chunk["tool_name"])
                    
                    # Display tool calling status with live updates
                    with tool_expander_placeholder.expander("🔧 View tool calls", expanded=True):
                        for tool_call in tool_calls_data:
                            tool_name = tool_call.get("tool_name", "Unknown")
                            tool_args = tool_call.get("arguments", {})
                            tool_result = tool_call.get("result", "")
                            
                            # Create friendly tool names
                            tool_display = {
                                "search_restaurants": "🔍 Search Restaurants",
                                "get_availability": "📅 Check Availability",
                                "make_reservation": "✅ Make Reservation",
                                "cancel_reservation": "❌ Cancel Reservation",
                                "get_recommendations": "⭐ Get Recommendations"
                            }.get(tool_name, f"🔧 {tool_name}")
                            
                            st.markdown(f"**{tool_display}**")
                            
                            if tool_args:
                                st.json(tool_args, expanded=False)
                            
                            if tool_result:
                                with st.expander("Result", expanded=False):
                                    st.text(tool_result[:500] + ("..." if len(tool_result) > 500 else ""))
                            
                            st.markdown("---")
                
                # Check if this is a status message (contains "Using tools:")
                elif isinstance(chunk, str) and "Using tools:" in chunk:
                    # Extract tool names from the status message
                    tools_str = chunk.replace("Using tools:", "").strip().rstrip("...")
                    tools = [t.strip() for t in tools_str.split(",")]
                    
                    # Display simple status
                    message_placeholder.markdown("*Processing your request...*")
                
                elif isinstance(chunk, str):
                    # This is actual response content
                    full_response += chunk
                    # Display streaming text with cursor animation
                    message_placeholder.markdown(full_response + " ●")
            
            # Display final response without cursor
            message_placeholder.markdown(full_response)
            
            # Update tool expander to be collapsed by default after completion
            if tool_calls_data:
                with tool_expander_placeholder.expander("🔧 View tool calls", expanded=False):
                    for tool_call in tool_calls_data:
                        tool_name = tool_call.get("tool_name", "Unknown")
                        tool_args = tool_call.get("arguments", {})
                        tool_result = tool_call.get("result", "")
                        
                        # Create friendly tool names
                        tool_display = {
                            "search_restaurants": "🔍 Search Restaurants",
                            "get_availability": "📅 Check Availability",
                            "make_reservation": "✅ Make Reservation",
                            "cancel_reservation": "❌ Cancel Reservation",
                            "get_recommendations": "⭐ Get Recommendations"
                        }.get(tool_name, f"🔧 {tool_name}")
                        
                        st.markdown(f"**{tool_display}**")
                        
                        if tool_args:
                            st.json(tool_args, expanded=False)
                        
                        if tool_result:
                            with st.expander("Result", expanded=False):
                                st.text(tool_result[:500] + ("..." if len(tool_result) > 500 else ""))
                        
                        st.markdown("---")
            
        except Exception as e:
            # Handle and display API errors gracefully
            error_type = type(e).__name__
            error_message = str(e)
            
            # Provide user-friendly error messages
            if "API" in error_message or "401" in error_message or "403" in error_message:
                full_response = "⚠️ I'm having trouble connecting to the AI service. Please check your API key configuration."
            elif "timeout" in error_message.lower() or "timed out" in error_message.lower():
                full_response = "⏱️ The request took too long to process. Please try again with a simpler query."
            elif "rate limit" in error_message.lower():
                full_response = "⏸️ We've reached the rate limit. Please wait a moment and try again."
            else:
                full_response = f"❌ I apologize, but I encountered an error: {error_message}"
            
            message_placeholder.markdown(full_response)
    
    # Append complete response to session state with tool calls
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "tool_calls": [
            {
                "name": tc.get("tool_name"),
                "arguments": tc.get("arguments"),
                "result": tc.get("result")
            }
            for tc in tool_calls_data
        ]
    })
    
    # Rerun to update the display
    st.rerun()

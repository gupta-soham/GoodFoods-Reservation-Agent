"""
GoodFoods Reservation Agent - Streamlit Frontend

A conversational AI interface for restaurant discovery and reservation management.
"""

import streamlit as st
import os
import time
import re
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

# Custom CSS for clean, professional, minimal design with animations
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Clean background with subtle gradient */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #ffffff 100%);
        background-attachment: fixed;
    }
    
    /* Main content area */
    .main {
        background-color: transparent;
        scroll-behavior: smooth;
        max-width: 850px;
        padding: 1.5rem 1rem 2rem;
    }
    
    /* Title styling with gradient */
    h1 {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
        font-size: 2.75rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.03em;
        animation: fadeInDown 0.6s ease-out;
    }
    
    /* Subtitle styling */
    .main > div > div > p:first-of-type,
    .main em {
        color: #64748b !important;
        font-size: 1.125rem !important;
        font-weight: 400 !important;
        line-height: 1.6 !important;
        animation: fadeIn 0.8s ease-out;
    }
    
    /* Horizontal rule */
    hr {
        margin: 1.5rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #e5e7eb, transparent) !important;
    }
    
    /* Chat message container */
    .stChatMessage {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.03);
        animation: slideInUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stChatMessage::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, #cbd5e1, transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stChatMessage:hover {
        box-shadow: 0 10px 20px rgba(0,0,0,0.08), 0 3px 6px rgba(0,0,0,0.05);
        transform: translateY(-2px);
        border-color: #cbd5e1;
    }
    
    .stChatMessage:hover::before {
        opacity: 1;
    }
    
    /* Fade in animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Slide-in animation with bounce */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px) scale(0.98);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    /* Pulse animation for loading */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    /* Pulse glow animation for tool badges */
    @keyframes pulse-glow {
        0%, 100% {
            opacity: 1;
            box-shadow: 0 0 8px rgba(16, 185, 129, 0.4), 0 0 16px rgba(16, 185, 129, 0.2);
            transform: scale(1);
        }
        50% {
            opacity: 0.9;
            box-shadow: 0 0 16px rgba(16, 185, 129, 0.6), 0 0 32px rgba(16, 185, 129, 0.3);
            transform: scale(1.02);
        }
    }
    
    /* Cursor blink animation for streaming */
    @keyframes blink {
        0%, 49% {
            opacity: 1;
        }
        50%, 100% {
            opacity: 0;
        }
    }
    
    /* Typing indicator */
    @keyframes typingDot {
        0%, 20% {
            transform: translateY(0);
            opacity: 0.4;
        }
        50% {
            transform: translateY(-8px);
            opacity: 1;
        }
        100% {
            transform: translateY(0);
            opacity: 0.4;
        }
    }
    
    /* Minimal thinking indicator shown after tools tooltip */
    .thinking-mini {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 10px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        color: #64748b;
        font-size: 0.9rem;
    }

    .thinking-mini .dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #94a3b8;
        animation: typingDot 1.4s infinite;
    }

    .thinking-mini .dot:nth-child(2) { animation-delay: 0.2s; }
    .thinking-mini .dot:nth-child(3) { animation-delay: 0.4s; }

    /* Chat message content */
    [data-testid="stChatMessageContent"] {
        background-color: transparent;
        color: #1e293b !important;
    }
    
    [data-testid="stChatMessageContent"] p {
        color: #1e293b !important;
        font-size: 0.975rem !important;
        line-height: 1.75 !important;
        margin: 0 !important;
    }
    
    /* User message styling with gradient */
    [data-testid="stChatMessage"]:has([aria-label="user"]) {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 3px solid #3b82f6;
        border: 1px solid #bfdbfe;
    }
    
    /* Assistant message styling with gradient */
    [data-testid="stChatMessage"]:has([aria-label="assistant"]) {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 3px solid #f59e0b;
        border: 1px solid #fde68a;
    }
    
    /* Input container with better positioning */
    .stChatInputContainer {
        position: sticky;
        bottom: 0;
        background: linear-gradient(to top, #ffffff 80%, transparent);
        border-top: 1px solid #e2e8f0;
        padding: 1.5rem 0 1rem;
        margin-top: 2rem;
        z-index: 100;
    }
    
    /* Input field styling with smooth transitions */
    .stChatInputContainer input,
    .stChatInputContainer textarea {
        color: #1e293b !important;
        font-size: 0.975rem !important;
        border-radius: 16px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 1rem 1.25rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        background: #ffffff !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03) !important;
    }
    
    .stChatInputContainer input:hover,
    .stChatInputContainer textarea:hover {
        border-color: #cbd5e1 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    
    .stChatInputContainer input:focus,
    .stChatInputContainer textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important;
        outline: none !important;
    }
    
    .stChatInputContainer input::placeholder,
    .stChatInputContainer textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 12px !important;
        padding: 0.5rem 1.25rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        border-radius: 12px !important;
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #f1f5f9 !important;
        border-color: #cbd5e1 !important;
    }
    
    /* Status container */
    .stStatus {
        background-color: #f0fdf4 !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        margin: 0.75rem 0 !important;
        animation: fadeIn 0.3s ease-out;
    }
    
    .stStatus summary {
        color: #15803d !important;
        font-weight: 500 !important;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: #f59e0b transparent transparent transparent !important;
        animation: spin 0.8s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Tool call badge with hover effect */
    .tool-badge {
        display: inline-block;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.375rem 0.875rem;
        border-radius: 10px;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.25rem 0.25rem 0.25rem 0;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
        transition: all 0.2s ease;
        cursor: default;
    }
    
    .tool-badge:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
    }
    
    /* Active tool badge with pulsing glow effect */
    .tool-badge-active {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 12px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        animation: pulse-glow 2s ease-in-out infinite;
        cursor: default;
    }
    
    /* Spinner for active tool badge */
    .tool-badge-spinner {
        width: 14px;
        height: 14px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top-color: white;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }
    
    /* Streaming cursor */
    .streaming-cursor {
        display: inline-block;
        width: 2px;
        height: 1.2em;
        background-color: #1e293b;
        margin-left: 2px;
        animation: blink 1s step-end infinite;
        vertical-align: text-bottom;
    }
    
    /* Error message styling */
    .stAlert {
        border-radius: 12px !important;
        border-left-width: 3px !important;
        animation: slideInUp 0.3s ease-out;
    }
    
    /* Success message */
    .element-container .stSuccess {
        background-color: #f0fdf4 !important;
        border-left-color: #10b981 !important;
    }
    
    /* Info message */
    .element-container .stInfo {
        background-color: #eff6ff !important;
        border-left-color: #3b82f6 !important;
    }
    
    /* Warning message */
    .element-container .stWarning {
        background-color: #fffbeb !important;
        border-left-color: #f59e0b !important;
    }
    
    /* Error message */
    .element-container .stError {
        background-color: #fef2f2 !important;
        border-left-color: #ef4444 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #cbd5e1, #94a3b8);
        border-radius: 5px;
        border: 2px solid #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #94a3b8, #64748b);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem !important;
        }
        
        .main {
            padding: 1rem 0.75rem;
        }
        
        .stChatMessage {
            padding: 1rem 1.25rem;
            border-radius: 16px;
        }
        
        .stChatInputContainer {
            padding: 1rem 0 0.75rem;
        }
    }
    
    /* Focus visible for accessibility */
    *:focus-visible {
        outline: 2px solid #3b82f6;
        outline-offset: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# Header with clear chat button
col1, col2 = st.columns([4, 1])
with col1:
    st.title("🍽️ GoodFoods Reservation Agent")
    st.markdown("*Your AI assistant for restaurant discovery and reservations*")
with col2:
    # Speed selector (Slow/Normal/Fast)
    if "streaming_speed" not in st.session_state:
        st.session_state.streaming_speed = "Normal"

    st.session_state.streaming_speed = st.selectbox(
        "Speed",
        options=["Slow", "Normal", "Fast"],
        index=1,  # Default to Normal
        help="Choose streaming speed: Slow (leisurely), Normal (balanced), Fast (quick)",
        key="speed_select"
    )

    if st.button("🗑️ Clear Chat", key="clear_chat", help="Clear all messages", use_container_width=True):
        st.session_state.messages = []
        st.session_state.tool_calls_history = {}
        st.rerun()

st.markdown("---")

# Check for API key
api_key = os.getenv("CEREBRAS_API_KEY")
if not api_key:
    st.error("⚠️ **Cerebras API Key Not Found**")
    st.markdown("""
    Please set up your Cerebras API key to use this application:
    
    1. Copy `.env.example` to `.env`
    2. Get your API key from [Cerebras](https://cloud.cerebras.ai/)
    3. Add your key to the `.env` file: `CEREBRAS_API_KEY=your_key_here`
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
    from agent.cerebras_client import CerebrasClient
    from agent.agent import ReservationAgent
    
    # Initialize and seed database
    db = RestaurantDatabase()
    restaurants = generate_restaurants()
    for restaurant in restaurants:
        db.add_restaurant(restaurant)
    
    # Initialize MCP Server
    mcp_server = MCPServer(db)
    
    # Initialize Cerebras Client
    client = CerebrasClient(api_key)
    
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
        thinking_placeholder = st.empty()

        full_response = ""
        tool_calls_data = []
        active_tools = []
        showed_post_tool_thinking = False
        first_content_received = False
        tool_section_initialized = False

        try:
            # Process message and stream response
            for chunk in agent.process_message(user_input):
                # Check if this is a tool call data chunk (dict with tool info)
                if isinstance(chunk, dict) and "tool_name" in chunk:
                    tool_calls_data.append(chunk)
                    
                    # Get tool display name
                    tool_name = chunk.get("tool_name", "Unknown")
                    tool_display = {
                        "search_restaurants": "🔍 Search Restaurants",
                        "get_availability": "📅 Check Availability",
                        "make_reservation": "✅ Make Reservation",
                        "cancel_reservation": "❌ Cancel Reservation",
                        "get_recommendations": "⭐ Get Recommendations"
                    }.get(tool_name, f"🔧 {tool_name}")
                    
                    # Display tool calling status with live updates in expander
                    with tool_expander_placeholder.expander("🔧 View tool calls", expanded=True):
                        for tool_call in tool_calls_data:
                            tool_name = tool_call.get("tool_name", "Unknown")
                            tool_args = tool_call.get("arguments", {})
                            tool_result = tool_call.get("result", "")
                            
                            # Create friendly tool names
                            tool_display_name = {
                                "search_restaurants": "🔍 Search Restaurants",
                                "get_availability": "📅 Check Availability",
                                "make_reservation": "✅ Make Reservation",
                                "cancel_reservation": "❌ Cancel Reservation",
                                "get_recommendations": "⭐ Get Recommendations"
                            }.get(tool_name, f"🔧 {tool_name}")
                            
                            # Highlight currently executing tool with pulsing badge
                            if tool_name == chunk.get("tool_name"):
                                st.markdown(
                                    f'<div class="tool-badge-active"><div class="tool-badge-spinner"></div>{tool_display_name}</div>',
                                    unsafe_allow_html=True
                                )
                            else:
                                st.markdown(f"**{tool_display_name}**")
                            
                            if tool_args:
                                st.json(tool_args, expanded=False)
                            
                            if tool_result:
                                with st.expander("Result", expanded=False):
                                    # Render Markdown in tool results for better formatting
                                    st.markdown(tool_result)
                            
                            st.markdown("---")

                    # After rendering tool tooltip the first time, show a minimal thinking indicator
                    if not tool_section_initialized:
                        tool_section_initialized = True
                        if not showed_post_tool_thinking:
                            thinking_placeholder.markdown(
                                '<div class="thinking-mini">Thinking <span class="dot"></span><span class="dot"></span><span class="dot"></span></div>',
                                unsafe_allow_html=True
                            )
                
                # Check if this is a status message (contains "Using tools:")
                elif isinstance(chunk, str) and "Using tools:" in chunk:
                    # Extract tool names from the status message
                    tools_str = chunk.replace("Using tools:", "").strip().rstrip("...")
                    active_tools = [t.strip() for t in tools_str.split(",")]
                
                elif isinstance(chunk, str):
                    # This is actual response content
                    # Hide the post-tool thinking indicator when the first content chunk arrives
                    if not first_content_received:
                        first_content_received = True
                        if tool_calls_data and not showed_post_tool_thinking:
                            thinking_placeholder.empty()
                            showed_post_tool_thinking = True

                    # Accumulate the full response
                    full_response += chunk
            
            # Display final response with speed-controlled streaming or all at once
            speed = st.session_state.get("streaming_speed", "Normal")
            
            # Accumulate and display the complete response with proper Markdown formatting
            # The full response is rendered at once to preserve Markdown formatting (bold, lists, etc.)
            # Speed selector is available for future streaming implementation
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
                                # Render Markdown in tool results for better formatting
                                st.markdown(tool_result)

                        st.markdown("---")

        except Exception as e:
            # Handle and display API errors gracefully
            error_type = type(e).__name__
            error_message = str(e)
            
            # Provide user-friendly error messages with retry option
            if "API" in error_message or "401" in error_message or "403" in error_message:
                full_response = "⚠️ I'm having trouble connecting to the AI service. Please check your API key configuration."
            elif "timeout" in error_message.lower() or "timed out" in error_message.lower():
                full_response = "⏱️ The request took too long to process. Please try again with a simpler query."
            elif "rate limit" in error_message.lower():
                full_response = "⏸️ We've reached the rate limit. Please wait a moment and try again."
            else:
                full_response = f"❌ I apologize, but I encountered an error: {error_message}"
            
            message_placeholder.markdown(full_response)
            
            # Show retry suggestion
            st.info("💡 Tip: Try rephrasing your question or check your connection.")
    
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
    
    # Scroll to bottom using JavaScript
    st.markdown(
        """
        <script>
        window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});
        </script>
        """,
        unsafe_allow_html=True
    )
    
    # Rerun to update the display
    st.rerun()

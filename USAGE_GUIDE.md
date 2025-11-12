# GoodFoods Reservation Agent - Usage Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenRouter API key
OPENROUTER_API_KEY=your_key_here
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Features

### 🔍 Search Restaurants

Ask natural questions like:

- "Show me Italian restaurants in Downtown"
- "Find Japanese restaurants for 4 people"
- "I'm looking for Mexican food in Uptown"

### ⭐ Get Recommendations

Request personalized suggestions:

- "Recommend some highly-rated restaurants"
- "Suggest restaurants with outdoor seating"
- "What are the best restaurants in Downtown?"

### 📅 Check Availability

Verify restaurant capacity:

- "Is Bella Italia available tonight at 7pm for 4 people?"
- "Check availability at Sushi Zen tomorrow at 6pm"

### ✅ Make Reservations

Book tables easily:

- "Book a table at Osteria Bella Luna for tomorrow at 7pm for 4 people under John Smith"
- "Reserve a table for 2 at Le Maison Sol on Friday at 8pm under Jane Doe"

### ❌ Cancel Reservations

Cancel existing bookings:

- "Cancel reservation abc-123-def"
- "Cancel my reservation with ID xyz-789"

## New Feature: Tool Call Tracking

### What It Shows

Every assistant response now includes a "🔧 View tool calls" expander that reveals:

- Which tools the agent used
- What parameters were sent
- What results were returned

### How to Use It

1. Ask any question
2. Wait for the response
3. Click "🔧 View tool calls" to expand
4. See the tool name (e.g., "⭐ Get Recommendations")
5. Click the JSON to see arguments
6. Click "Result" to see the raw output

### Why It's Useful

- **Transparency**: See exactly what the agent is doing
- **Debugging**: Understand why you got certain results
- **Learning**: See how the system works behind the scenes

## Example Conversations

### Example 1: Finding and Booking

```
You: I'm looking for Italian restaurants in Downtown for 4 people

Agent: [Searches and shows 2 Italian restaurants]
      Here are some Italian restaurants in Downtown...

You: Book a table at Osteria Bella Luna for tomorrow at 7pm for 4 people under John Smith

Agent: [Makes reservation]
      Reservation confirmed! Your reservation ID is: abc-123-def
```

### Example 2: Getting Recommendations

```
You: Recommend some highly-rated restaurants with outdoor seating

Agent: [Gets recommendations]
      Here are some highly-rated restaurants with outdoor seating:
      1. Hana Yuki House: A cozy Japanese spot with a 5.0 rating...
      2. El La Luna: A contemporary Mexican restaurant...
      [Shows 10 restaurants total]
```

### Example 3: Checking Availability

```
You: Is Bella Italia available tonight at 7pm for 4 people?

Agent: [Checks availability]
      Restaurant is available for 4 guests on 2025-11-11 at 19:00.
      Would you like me to make a reservation?
```

## Tips for Best Results

### 1. Be Specific

✅ Good: "Italian restaurants in Downtown for 4 people"
❌ Vague: "restaurants"

### 2. Include Details for Reservations

✅ Good: "Book at Bella Italia for tomorrow at 7pm for 4 people under John Smith"
❌ Missing info: "Book a table"

### 3. Use Natural Language

The agent understands conversational queries:

- "I'm looking for..."
- "Can you recommend..."
- "Show me..."
- "Find me..."

### 4. Check Tool Calls

If you get unexpected results:

1. Click "🔧 View tool calls"
2. Check what parameters were sent
3. Verify the tool results
4. Rephrase your question if needed

## Troubleshooting

### "OpenRouter API Key Not Found"

**Solution**:

1. Create a `.env` file (not `.env.example`)
2. Add your API key: `OPENROUTER_API_KEY=sk-or-...`
3. Restart the app

### "Rate limit exceeded"

**Solution**:

- Free tier: 50 requests/day
- Wait until the limit resets (shown in error message)
- Or add credits to your OpenRouter account

### "I'm having trouble connecting"

**Solution**:

1. Check your internet connection
2. Verify your API key is valid
3. Check OpenRouter status

### No Results Found

**Solution**:

1. Click "🔧 View tool calls" to see what was searched
2. Try broader criteria (e.g., remove location filter)
3. Check if the restaurant exists in the database

## Advanced Features

### Conversation History

- The app remembers the last 20 messages
- Context is maintained across questions
- You can ask follow-up questions

### Multi-Tool Execution

- The agent can use multiple tools in one response
- Example: Search restaurants, then check availability
- All tool calls are shown in the expander

### Streaming Responses

- Responses appear in real-time
- Smooth typing animation
- Tool calls execute in the background

## API Rate Limits

### Free Tier

- 50 requests per day
- Resets at midnight UTC
- Shared across all free models

### Paid Tier

- 1000+ requests per day
- Faster response times
- Priority access

### Monitoring Usage

Check your usage at: https://openrouter.ai/activity

## Support

### Documentation

- [API Reference](docs/API_REFERENCE.md)
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Tool Calling Guide](docs/TOOL_CALLING_GUIDE.md)

### Issues

If you encounter problems:

1. Check the tool call expander for details
2. Review the error message
3. Check the troubleshooting section
4. Verify your API key and credits

## Best Practices

### For Users

1. Start with simple queries
2. Use the tool call expander to learn
3. Be specific with dates and times
4. Save your reservation IDs

### For Developers

1. Monitor API usage
2. Test with various queries
3. Check tool call data for debugging
4. Update the database with real restaurants

## What's New

### Latest Updates (November 11, 2025)

✨ **Tool Call Tracking**: See exactly what the agent is doing
✨ **Fixed Recommendations**: Now works perfectly end-to-end
✨ **Improved UI**: Expandable tool call details
✨ **Better Error Handling**: Clear, actionable error messages

---

**Enjoy using GoodFoods Reservation Agent!** 🍽️

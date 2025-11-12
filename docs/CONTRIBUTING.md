# Contributing to GoodFoods Reservation Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## Getting Started

### Development Setup

1. **Fork the repository**

   ```bash
   # Click "Fork" on GitHub
   git clone https://github.com/gupta-soham/goodfoods-reservation-agent.git
   cd goodfoods-reservation-agent
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**

   ```bash
   cp .env.example .env
   # Add your OPENROUTER_API_KEY to .env
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Code Style Guidelines

### Python Style (PEP 8)

Follow [PEP 8](https://pep8.org/) style guide:

```python
# Good
def search_restaurants(cuisine: str, location: str) -> List[Restaurant]:
    """
    Search for restaurants based on criteria.

    Args:
        cuisine: Type of cuisine to search for
        location: Geographic location

    Returns:
        List of matching restaurants
    """
    results = []
    # Implementation
    return results

# Bad
def searchRestaurants(cuisine,location):
    results=[]
    return results
```

### Type Hints

Always use type hints:

```python
from typing import List, Dict, Optional, Any

def process_message(self, user_message: str) -> Generator[str, None, None]:
    """Process user message and yield response chunks."""
    pass

def get_restaurant(self, restaurant_id: str) -> Optional[Restaurant]:
    """Get restaurant by ID, returns None if not found."""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def create_reservation(
    self,
    restaurant_id: str,
    date: str,
    time: str,
    party_size: int,
    customer_name: str
) -> Optional[Reservation]:
    """
    Create a new reservation.

    Args:
        restaurant_id: Unique identifier of the restaurant
        date: Reservation date in YYYY-MM-DD format
        time: Reservation time in HH:MM format (24-hour)
        party_size: Number of guests in the party
        customer_name: Full name of the customer

    Returns:
        Reservation object if successful, None if unavailable

    Example:
        >>> reservation = db.create_reservation(
        ...     restaurant_id="rest_001",
        ...     date="2025-11-15",
        ...     time="19:00",
        ...     party_size=4,
        ...     customer_name="John Smith"
        ... )
    """
    pass
```

### Code Organization

```python
# 1. Standard library imports
import os
import json
from datetime import datetime
from typing import List, Dict, Optional

# 2. Third-party imports
import streamlit as st
import requests

# 3. Local imports
from database.models import Restaurant, Reservation
from agent.agent import ReservationAgent
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `ReservationAgent`, `MCPServer`)
- **Functions/Methods**: `snake_case` (e.g., `process_message`, `search_restaurants`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`, `DEFAULT_MODEL`)
- **Private methods**: `_leading_underscore` (e.g., `_execute_tool`, `_format_result`)

## Testing Requirements

### Unit Tests

Write unit tests for all new functionality:

```python
import unittest
from database.restaurant_db import RestaurantDatabase
from database.models import Restaurant

class TestRestaurantDatabase(unittest.TestCase):
    def setUp(self):
        self.db = RestaurantDatabase()
        self.restaurant = Restaurant(
            id="test_001",
            name="Test Restaurant",
            cuisine="Italian",
            location="Downtown",
            address="123 Test St",
            seating_capacity=50,
            operating_hours={"mon-fri": "11:00-22:00"},
            price_range="$$",
            rating=4.5,
            description="Test description"
        )
        self.db.add_restaurant(self.restaurant)

    def test_get_restaurant(self):
        result = self.db.get_restaurant("test_001")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Test Restaurant")

    def test_search_by_cuisine(self):
        results = self.db.search_restaurants(cuisine="Italian")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, "test_001")
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests/test_database.py

# Run with coverage
pip install coverage
coverage run -m unittest discover tests
coverage report
```

## Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

Branch naming:

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/updates

### 2. Make Changes

- Write clean, documented code
- Follow style guidelines
- Add tests for new functionality
- Update documentation

### 3. Commit Changes

Write clear commit messages:

```bash
# Good
git commit -m "Add get_restaurant_reviews tool"
git commit -m "Fix availability check for edge cases"
git commit -m "Update API documentation for new endpoints"

# Bad
git commit -m "updates"
git commit -m "fix bug"
git commit -m "changes"
```

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:

- Clear title describing the change
- Description of what was changed and why
- Reference to related issues (if any)
- Screenshots (for UI changes)

### 5. PR Review

- Address reviewer feedback
- Make requested changes
- Keep discussion professional and constructive

### 6. Merge

Once approved, your PR will be merged!

## What to Contribute

### Good First Issues

- Fix typos in documentation
- Add examples to docstrings
- Improve error messages
- Add unit tests
- Update README

### Feature Ideas

- Add new tools (e.g., get_reviews, get_menu)
- Improve recommendation algorithm
- Add persistent database support
- Implement user authentication
- Add multi-language support
- Create admin dashboard

### Bug Fixes

- Check [Issues](https://github.com/your-repo/issues) for reported bugs
- Reproduce the bug
- Write a test that fails
- Fix the bug
- Verify test passes

## Development Guidelines

### Adding a New Tool

1. **Define tool schema** in `agent/agent.py`:

```python
{
    "type": "function",
    "function": {
        "name": "new_tool",
        "description": "Clear description",
        "parameters": {...}
    }
}
```

2. **Add to MCP Server** in `mcp_server/server.py`:

```python
def _define_tools(self):
    return [
        # ... existing tools
        {
            "name": "new_tool",
            "description": "Clear description",
            "inputSchema": {...}
        }
    ]

def call_tool(self, tool_name, arguments):
    if tool_name == "new_tool":
        return self._new_tool(arguments)
    # ... existing tools

def _new_tool(self, arguments):
    # Implementation
    return {"content": [{"type": "text", "text": result}]}
```

3. **Add tests**
4. **Update documentation**

### Adding Database Methods

1. **Add method** to `database/restaurant_db.py`
2. **Add type hints and docstring**
3. **Write unit tests**
4. **Update API documentation**

### Modifying Frontend

1. **Make changes** to `app.py`
2. **Test in browser**
3. **Ensure responsive design**
4. **Update screenshots if needed**

## Documentation

### When to Update Docs

- Adding new features
- Changing APIs
- Fixing bugs that affect usage
- Adding configuration options

### Documentation Files

- `README.md` - Overview and quick start
- `docs/API_REFERENCE.md` - API documentation
- `docs/ARCHITECTURE.md` - System design
- `docs/TOOL_CALLING_GUIDE.md` - Tool calling details
- `docs/MCP_PROTOCOL.md` - MCP implementation
- `docs/DEPLOYMENT.md` - Deployment guide

## Questions?

- Open an [Issue](https://github.com/your-repo/issues)
- Start a [Discussion](https://github.com/your-repo/discussions)
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

"""
MCP Server implementation for the GoodFoods Reservation Agent.

This module implements a Model Context Protocol (MCP) server that provides
tools and resources for restaurant search and reservation management.
"""

from typing import Any, Dict, List, Optional
from database.restaurant_db import RestaurantDatabase


class MCPServer:
    """
    MCP Server implementing JSON-RPC 2.0 protocol.
    
    Provides tools for restaurant operations and resources for accessing
    restaurant data.
    """
    
    def __init__(self, database: RestaurantDatabase):
        """
        Initialize the MCP Server.
        
        Args:
            database: RestaurantDatabase instance for data operations
        """
        self.database = database
        self.tools = self._define_tools()
        self.resources = self._define_resources()
    
    def _define_tools(self) -> List[Dict[str, Any]]:
        """
        Define available tools for the MCP server.
        
        Returns:
            List of tool definitions
        """
        return [
            {
                "name": "search_restaurants",
                "description": "Search for restaurants based on criteria",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "cuisine": {"type": "string", "description": "Type of cuisine"},
                        "location": {"type": "string", "description": "Geographic location"},
                        "party_size": {"type": "integer", "description": "Number of guests"},
                        "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                        "time": {"type": "string", "description": "Time in HH:MM format"}
                    }
                }
            },
            {
                "name": "get_availability",
                "description": "Check availability for a restaurant at a specific time",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "restaurant_id": {"type": "string", "description": "Restaurant ID"},
                        "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                        "time": {"type": "string", "description": "Time in HH:MM format"},
                        "party_size": {"type": "integer", "description": "Number of guests"}
                    },
                    "required": ["restaurant_id", "date", "time", "party_size"]
                }
            },
            {
                "name": "make_reservation",
                "description": "Create a new reservation at a restaurant",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "restaurant_id": {"type": "string", "description": "Restaurant ID"},
                        "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                        "time": {"type": "string", "description": "Time in HH:MM format"},
                        "party_size": {"type": "integer", "description": "Number of guests"},
                        "customer_name": {"type": "string", "description": "Customer name"}
                    },
                    "required": ["restaurant_id", "date", "time", "party_size", "customer_name"]
                }
            },
            {
                "name": "cancel_reservation",
                "description": "Cancel an existing reservation",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {"type": "string", "description": "Reservation ID"}
                    },
                    "required": ["reservation_id"]
                }
            },
            {
                "name": "get_recommendations",
                "description": "Get restaurant recommendations based on preferences",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "preferences": {
                            "type": "object",
                            "description": "User preferences for recommendations",
                            "properties": {
                                "cuisine": {"type": "string"},
                                "location": {"type": "string"},
                                "price_range": {"type": "string"},
                                "min_rating": {"type": "number"}
                            }
                        }
                    }
                }
            }
        ]
    
    def _define_resources(self) -> List[Dict[str, Any]]:
        """
        Define available resources for the MCP server.
        
        Returns:
            List of resource definitions
        """
        return [
            {
                "uri": "restaurants://list",
                "name": "All Restaurants",
                "description": "List of all available restaurants",
                "mimeType": "application/json"
            },
            {
                "uri": "restaurants://{id}",
                "name": "Restaurant Details",
                "description": "Detailed information about a specific restaurant",
                "mimeType": "application/json"
            }
        ]
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming JSON-RPC 2.0 requests.
        
        Args:
            request: JSON-RPC request object
            
        Returns:
            JSON-RPC response object
        """
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "tools/list":
                result = self.list_tools()
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_params = params.get("arguments", {})
                result = self.call_tool(tool_name, tool_params)
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
    
    def list_tools(self) -> Dict[str, Any]:
        """
        Return list of available tools.
        
        Returns:
            Dictionary containing tools list
        """
        return {"tools": self.tools}
    
    def list_resources(self) -> Dict[str, Any]:
        """
        Return list of available resources.
        
        Returns:
            Dictionary containing resources list
        """
        return {"resources": self.resources}
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool with given arguments.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        if tool_name == "search_restaurants":
            return self._search_restaurants(arguments)
        elif tool_name == "get_availability":
            return self._get_availability(arguments)
        elif tool_name == "make_reservation":
            return self._make_reservation(arguments)
        elif tool_name == "cancel_reservation":
            return self._cancel_reservation(arguments)
        elif tool_name == "get_recommendations":
            return self._get_recommendations(arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    def _search_restaurants(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search for restaurants based on criteria.
        
        Args:
            arguments: Search parameters
            
        Returns:
            Dictionary containing search results
        """
        cuisine = arguments.get("cuisine")
        location = arguments.get("location")
        party_size = arguments.get("party_size")
        date = arguments.get("date")
        time = arguments.get("time")
        
        results = self.database.search_restaurants(
            cuisine=cuisine,
            location=location,
            party_size=party_size,
            date=date,
            time=time
        )
        
        if not results:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "No restaurants found matching your criteria."
                    }
                ]
            }
        
        # Format results
        import json
        restaurants_data = [
            {
                "id": r.id,
                "name": r.name,
                "cuisine": r.cuisine,
                "location": r.location,
                "address": r.address,
                "seating_capacity": r.seating_capacity,
                "price_range": r.price_range,
                "rating": r.rating,
                "description": r.description
            }
            for r in results
        ]
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Found {len(results)} restaurant(s):\n\n" + json.dumps(restaurants_data, indent=2)
                }
            ]
        }
    
    def read_resource(self, uri: str) -> Dict[str, Any]:
        """
        Read a resource by URI.
        
        Args:
            uri: Resource URI
            
        Returns:
            Resource data
        """
        if uri == "restaurants://list":
            return self._get_restaurants_list()
        elif uri.startswith("restaurants://"):
            restaurant_id = uri.replace("restaurants://", "")
            return self._get_restaurant(restaurant_id)
        else:
            raise ValueError(f"Unknown resource URI: {uri}")
    
    def _get_restaurants_list(self) -> Dict[str, Any]:
        """
        Get list of all restaurants.
        
        Returns:
            Dictionary containing all restaurants
        """
        restaurants = list(self.database.restaurants.values())
        return {
            "contents": [
                {
                    "uri": f"restaurants://{r.id}",
                    "mimeType": "application/json",
                    "text": self._format_restaurant(r)
                }
                for r in restaurants
            ]
        }
    
    def _get_restaurant(self, restaurant_id: str) -> Dict[str, Any]:
        """
        Get details for a specific restaurant.
        
        Args:
            restaurant_id: Restaurant ID
            
        Returns:
            Dictionary containing restaurant details
        """
        restaurant = self.database.get_restaurant(restaurant_id)
        if not restaurant:
            raise ValueError(f"Restaurant not found: {restaurant_id}")
        
        return {
            "contents": [
                {
                    "uri": f"restaurants://{restaurant_id}",
                    "mimeType": "application/json",
                    "text": self._format_restaurant(restaurant)
                }
            ]
        }
    
    def _format_restaurant(self, restaurant) -> str:
        """
        Format restaurant data as JSON string.
        
        Args:
            restaurant: Restaurant object
            
        Returns:
            JSON string representation
        """
        import json
        return json.dumps({
            "id": restaurant.id,
            "name": restaurant.name,
            "cuisine": restaurant.cuisine,
            "location": restaurant.location,
            "address": restaurant.address,
            "seating_capacity": restaurant.seating_capacity,
            "operating_hours": restaurant.operating_hours,
            "price_range": restaurant.price_range,
            "rating": restaurant.rating,
            "description": restaurant.description
        }, indent=2)

    def _get_availability(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check availability for a restaurant at a specific time.
        
        Args:
            arguments: Availability check parameters
            
        Returns:
            Dictionary containing availability information
        """
        restaurant_id = arguments.get("restaurant_id")
        date = arguments.get("date")
        time = arguments.get("time")
        party_size = arguments.get("party_size")
        
        if not all([restaurant_id, date, time, party_size]):
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Missing required parameters: restaurant_id, date, time, party_size"
                    }
                ]
            }
        
        is_available = self.database.check_availability(
            restaurant_id, date, time, party_size
        )
        
        if is_available:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Restaurant is available for {party_size} guests on {date} at {time}."
                    }
                ]
            }
        else:
            # Generate alternative time slots
            alternative_times = self._get_alternative_times(restaurant_id, date, time, party_size)
            
            if alternative_times:
                times_str = ", ".join(alternative_times)
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Restaurant is not available at {time}. Alternative times: {times_str}"
                        }
                    ]
                }
            else:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Restaurant is not available for {party_size} guests on {date}."
                        }
                    ]
                }
    
    def _get_alternative_times(self, restaurant_id: str, date: str, requested_time: str, party_size: int) -> List[str]:
        """
        Find alternative available time slots.
        
        Args:
            restaurant_id: Restaurant ID
            date: Date in YYYY-MM-DD format
            requested_time: Requested time in HH:MM format
            party_size: Number of guests
            
        Returns:
            List of available time slots
        """
        # Check common dining times
        time_slots = [
            "11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
            "17:00", "17:30", "18:00", "18:30", "19:00", "19:30",
            "20:00", "20:30", "21:00", "21:30"
        ]
        
        available_times = []
        for time_slot in time_slots:
            if time_slot != requested_time:
                if self.database.check_availability(restaurant_id, date, time_slot, party_size):
                    available_times.append(time_slot)
                    if len(available_times) >= 3:  # Return up to 3 alternatives
                        break
        
        return available_times

    def _make_reservation(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new reservation at a restaurant.
        
        Args:
            arguments: Reservation parameters
            
        Returns:
            Dictionary containing reservation confirmation
        """
        restaurant_id = arguments.get("restaurant_id")
        date = arguments.get("date")
        time = arguments.get("time")
        party_size = arguments.get("party_size")
        customer_name = arguments.get("customer_name")
        
        if not all([restaurant_id, date, time, party_size, customer_name]):
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Missing required parameters: restaurant_id, date, time, party_size, customer_name"
                    }
                ]
            }
        
        # Check if restaurant exists
        restaurant = self.database.get_restaurant(restaurant_id)
        if not restaurant:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Restaurant not found: {restaurant_id}"
                    }
                ]
            }
        
        # Create reservation
        reservation = self.database.create_reservation(
            restaurant_id=restaurant_id,
            date=date,
            time=time,
            party_size=party_size,
            customer_name=customer_name
        )
        
        if reservation:
            import json
            confirmation = {
                "reservation_id": reservation.id,
                "restaurant_name": restaurant.name,
                "date": reservation.date,
                "time": reservation.time,
                "party_size": reservation.party_size,
                "customer_name": reservation.customer_name,
                "status": reservation.status
            }
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Reservation confirmed!\n\n{json.dumps(confirmation, indent=2)}"
                    }
                ]
            }
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Unable to create reservation. Restaurant is not available for {party_size} guests on {date} at {time}."
                    }
                ]
            }

    def _cancel_reservation(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cancel an existing reservation.
        
        Args:
            arguments: Cancellation parameters
            
        Returns:
            Dictionary containing cancellation confirmation
        """
        reservation_id = arguments.get("reservation_id")
        
        if not reservation_id:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "Missing required parameter: reservation_id"
                    }
                ]
            }
        
        # Get reservation details before canceling
        reservation = self.database.get_reservation(reservation_id)
        if not reservation:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Reservation not found: {reservation_id}"
                    }
                ]
            }
        
        # Cancel the reservation
        success = self.database.cancel_reservation(reservation_id)
        
        if success:
            restaurant = self.database.get_restaurant(reservation.restaurant_id)
            restaurant_name = restaurant.name if restaurant else "Unknown"
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Reservation {reservation_id} has been cancelled.\n\nDetails:\n- Restaurant: {restaurant_name}\n- Date: {reservation.date}\n- Time: {reservation.time}\n- Party size: {reservation.party_size}"
                    }
                ]
            }
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Failed to cancel reservation: {reservation_id}"
                    }
                ]
            }

    def _get_recommendations(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get restaurant recommendations based on preferences.
        
        Args:
            arguments: Recommendation parameters
            
        Returns:
            Dictionary containing recommended restaurants
        """
        preferences = arguments.get("preferences", {})
        
        # Get all restaurants
        all_restaurants = list(self.database.restaurants.values())
        
        # Filter by preferences
        filtered = all_restaurants
        
        if "cuisine" in preferences and preferences["cuisine"]:
            cuisine = preferences["cuisine"]
            filtered = [r for r in filtered if r.cuisine.lower() == cuisine.lower()]
        
        if "location" in preferences and preferences["location"]:
            location = preferences["location"]
            filtered = [r for r in filtered if r.location.lower() == location.lower()]
        
        if "price_range" in preferences and preferences["price_range"]:
            price_range = preferences["price_range"]
            filtered = [r for r in filtered if r.price_range == price_range]
        
        if "min_rating" in preferences and preferences["min_rating"]:
            min_rating = preferences["min_rating"]
            filtered = [r for r in filtered if r.rating >= min_rating]
        
        # Score and rank restaurants
        scored_restaurants = []
        for restaurant in filtered:
            score = self._calculate_recommendation_score(restaurant, preferences)
            scored_restaurants.append((restaurant, score))
        
        # Sort by score (descending)
        scored_restaurants.sort(key=lambda x: x[1], reverse=True)
        
        # Get top 5-10 recommendations
        top_recommendations = scored_restaurants[:10]
        
        if not top_recommendations:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": "No restaurants found matching your preferences."
                    }
                ]
            }
        
        # Format recommendations
        import json
        recommendations_data = [
            {
                "id": r.id,
                "name": r.name,
                "cuisine": r.cuisine,
                "location": r.location,
                "address": r.address,
                "price_range": r.price_range,
                "rating": r.rating,
                "description": r.description,
                "recommendation_score": round(score, 2)
            }
            for r, score in top_recommendations
        ]
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Top {len(recommendations_data)} recommendations:\n\n{json.dumps(recommendations_data, indent=2)}"
                }
            ]
        }
    
    def _calculate_recommendation_score(self, restaurant, preferences: Dict[str, Any]) -> float:
        """
        Calculate recommendation score for a restaurant.
        
        Args:
            restaurant: Restaurant object
            preferences: User preferences
            
        Returns:
            Recommendation score (higher is better)
        """
        score = 0.0
        
        # Base score from rating (0-5 points)
        score += restaurant.rating
        
        # Bonus for exact cuisine match (3 points)
        if "cuisine" in preferences and preferences["cuisine"]:
            if restaurant.cuisine.lower() == preferences["cuisine"].lower():
                score += 3.0
        
        # Bonus for exact location match (2 points)
        if "location" in preferences and preferences["location"]:
            if restaurant.location.lower() == preferences["location"].lower():
                score += 2.0
        
        # Bonus for price range match (1 point)
        if "price_range" in preferences and preferences["price_range"]:
            if restaurant.price_range == preferences["price_range"]:
                score += 1.0
        
        # Bonus for high ratings (1-2 points)
        if restaurant.rating >= 4.5:
            score += 2.0
        elif restaurant.rating >= 4.0:
            score += 1.0
        
        return score

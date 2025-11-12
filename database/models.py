"""
Data models for the GoodFoods Reservation Agent.

This module defines the core data structures for restaurants and reservations.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class Restaurant:
    """
    Represents a restaurant in the GoodFoods system.
    
    Attributes:
        id: Unique identifier for the restaurant
        name: Restaurant name
        cuisine: Type of cuisine (e.g., Italian, Chinese, Japanese)
        location: Geographic area (e.g., Downtown, Midtown)
        address: Full street address
        seating_capacity: Maximum number of guests the restaurant can accommodate
        operating_hours: Dictionary mapping day names to open/close times
        price_range: Price indicator ($, $$, $$$, $$$$)
        rating: Restaurant rating from 1.0 to 5.0
        description: Brief description of the restaurant
    """
    id: str
    name: str
    cuisine: str
    location: str
    address: str
    seating_capacity: int
    operating_hours: Dict[str, Dict[str, str]]
    price_range: str
    rating: float
    description: str


@dataclass
class Reservation:
    """
    Represents a reservation at a restaurant.
    
    Attributes:
        id: Unique identifier for the reservation
        restaurant_id: ID of the restaurant where the reservation is made
        date: Reservation date in YYYY-MM-DD format
        time: Reservation time in HH:MM format
        party_size: Number of guests
        customer_name: Name of the customer making the reservation
        created_at: Timestamp when the reservation was created
        status: Current status of the reservation (confirmed, cancelled)
    """
    id: str
    restaurant_id: str
    date: str
    time: str
    party_size: int
    customer_name: str
    created_at: datetime
    status: str

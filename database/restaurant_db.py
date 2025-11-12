"""
Restaurant database implementation for the GoodFoods Reservation Agent.

This module provides an in-memory database for managing restaurants and reservations.
"""

from datetime import datetime
from typing import Dict, List, Optional
import uuid

from database.models import Restaurant, Reservation


class RestaurantDatabase:
    """
    In-memory database for managing restaurants and reservations.
    
    This class provides methods for searching restaurants, checking availability,
    and managing reservations.
    """
    
    def __init__(self):
        """Initialize the database with empty storage."""
        self.restaurants: Dict[str, Restaurant] = {}
        self.reservations: Dict[str, Reservation] = {}
    
    def add_restaurant(self, restaurant: Restaurant) -> None:
        """
        Add a restaurant to the database.
        
        Args:
            restaurant: Restaurant object to add
        """
        self.restaurants[restaurant.id] = restaurant
    
    def get_restaurant(self, restaurant_id: str) -> Optional[Restaurant]:
        """
        Retrieve a restaurant by ID.
        
        Args:
            restaurant_id: Unique identifier of the restaurant
            
        Returns:
            Restaurant object if found, None otherwise
        """
        return self.restaurants.get(restaurant_id)
    
    def search_restaurants(
        self,
        cuisine: Optional[str] = None,
        location: Optional[str] = None,
        party_size: Optional[int] = None,
        date: Optional[str] = None,
        time: Optional[str] = None
    ) -> List[Restaurant]:
        """
        Search for restaurants based on criteria.
        
        Args:
            cuisine: Filter by cuisine type (case-insensitive)
            location: Filter by location (case-insensitive)
            party_size: Filter by seating capacity
            date: Filter by availability on date (YYYY-MM-DD)
            time: Filter by availability at time (HH:MM)
            
        Returns:
            List of restaurants matching all provided criteria
        """
        results = list(self.restaurants.values())
        
        # Filter by cuisine
        if cuisine:
            results = [
                r for r in results
                if r.cuisine.lower() == cuisine.lower()
            ]
        
        # Filter by location
        if location:
            results = [
                r for r in results
                if r.location.lower() == location.lower()
            ]
        
        # Filter by seating capacity
        if party_size:
            results = [
                r for r in results
                if r.seating_capacity >= party_size
            ]
        
        # Filter by availability
        if date and time:
            results = [
                r for r in results
                if self.check_availability(r.id, date, time, party_size or 1)
            ]
        
        return results
    
    def check_availability(
        self,
        restaurant_id: str,
        date: str,
        time: str,
        party_size: int
    ) -> bool:
        """
        Check if a restaurant can accommodate a party at the specified time.
        
        Args:
            restaurant_id: ID of the restaurant
            date: Reservation date (YYYY-MM-DD)
            time: Reservation time (HH:MM)
            party_size: Number of guests
            
        Returns:
            True if the restaurant has capacity, False otherwise
        """
        restaurant = self.get_restaurant(restaurant_id)
        if not restaurant:
            return False
        
        # Check if party size exceeds capacity
        if party_size > restaurant.seating_capacity:
            return False
        
        # Count existing reservations for this date and time
        existing_reservations = [
            res for res in self.reservations.values()
            if res.restaurant_id == restaurant_id
            and res.date == date
            and res.time == time
            and res.status == "confirmed"
        ]
        
        # Calculate total party size for existing reservations
        total_reserved = sum(res.party_size for res in existing_reservations)
        
        # Check if there's enough capacity
        return (total_reserved + party_size) <= restaurant.seating_capacity
    
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
            restaurant_id: ID of the restaurant
            date: Reservation date (YYYY-MM-DD)
            time: Reservation time (HH:MM)
            party_size: Number of guests
            customer_name: Name of the customer
            
        Returns:
            Reservation object if successful, None if unavailable
        """
        # Check availability
        if not self.check_availability(restaurant_id, date, time, party_size):
            return None
        
        # Create reservation
        reservation = Reservation(
            id=str(uuid.uuid4()),
            restaurant_id=restaurant_id,
            date=date,
            time=time,
            party_size=party_size,
            customer_name=customer_name,
            created_at=datetime.now(),
            status="confirmed"
        )
        
        self.reservations[reservation.id] = reservation
        return reservation
    
    def cancel_reservation(self, reservation_id: str) -> bool:
        """
        Cancel an existing reservation.
        
        Args:
            reservation_id: ID of the reservation to cancel
            
        Returns:
            True if cancellation was successful, False if reservation not found
        """
        reservation = self.reservations.get(reservation_id)
        if not reservation:
            return False
        
        reservation.status = "cancelled"
        return True
    
    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        """
        Retrieve a reservation by ID.
        
        Args:
            reservation_id: Unique identifier of the reservation
            
        Returns:
            Reservation object if found, None otherwise
        """
        return self.reservations.get(reservation_id)

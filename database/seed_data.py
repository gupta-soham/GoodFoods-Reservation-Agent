"""
Seed data generator for the GoodFoods Reservation Agent.

This module generates sample restaurant data for testing and demonstration.
"""

import random
from database.models import Restaurant


def generate_restaurants() -> list[Restaurant]:
    """
    Generate a diverse set of restaurant records.
    
    Returns:
        List of Restaurant objects with varied attributes
    """
    cuisines = [
        "Italian", "Chinese", "Japanese", "Mexican", "Indian",
        "French", "American", "Thai", "Mediterranean", "Korean"
    ]
    
    locations = [
        "Downtown", "Midtown", "Uptown", "Westside", "Eastside", "Waterfront"
    ]
    
    # Restaurant name templates by cuisine
    name_templates = {
        "Italian": ["Bella", "Trattoria", "Osteria", "Ristorante", "La", "Il"],
        "Chinese": ["Golden", "Dragon", "Jade", "Lotus", "Imperial", "Dynasty"],
        "Japanese": ["Sakura", "Zen", "Koi", "Hana", "Yuki", "Sushi"],
        "Mexican": ["El", "La", "Casa", "Cantina", "Taqueria", "Fiesta"],
        "Indian": ["Taj", "Spice", "Curry", "Masala", "Palace", "Garden"],
        "French": ["Le", "La", "Bistro", "Brasserie", "Chez", "Maison"],
        "American": ["The", "Grill", "Tavern", "House", "Kitchen", "Diner"],
        "Thai": ["Thai", "Siam", "Bangkok", "Orchid", "Basil", "Lemongrass"],
        "Mediterranean": ["Olive", "Aegean", "Cyprus", "Santorini", "Azure", "Coast"],
        "Korean": ["Seoul", "Kimchi", "BBQ", "Gangnam", "Han", "Arirang"]
    }
    
    restaurants = []
    restaurant_id = 1
    
    # Generate 80 restaurants (8 per cuisine type)
    for cuisine in cuisines:
        for i in range(8):
            # Generate restaurant name
            templates = name_templates[cuisine]
            name_parts = random.sample(templates, min(2, len(templates)))
            name = " ".join(name_parts)
            if cuisine in ["Italian", "French", "Mexican"]:
                name += f" {random.choice(['Rosa', 'Bella', 'Verde', 'Luna', 'Sol', 'Mar'])}"
            else:
                name += f" {random.choice(['House', 'Kitchen', 'Restaurant', 'Bistro', 'Cafe'])}"
            
            location = random.choice(locations)
            
            # Generate address
            street_number = random.randint(100, 9999)
            street_names = ["Main St", "Oak Ave", "Maple Dr", "Park Blvd", "River Rd", "Lake St"]
            address = f"{street_number} {random.choice(street_names)}, {location}"
            
            # Generate seating capacity (20-200)
            seating_capacity = random.choice([20, 30, 40, 50, 60, 75, 80, 100, 120, 150, 180, 200])
            
            # Generate operating hours
            operating_hours = {
                "Monday": {"open": "11:00", "close": "22:00"},
                "Tuesday": {"open": "11:00", "close": "22:00"},
                "Wednesday": {"open": "11:00", "close": "22:00"},
                "Thursday": {"open": "11:00", "close": "22:00"},
                "Friday": {"open": "11:00", "close": "23:00"},
                "Saturday": {"open": "10:00", "close": "23:00"},
                "Sunday": {"open": "10:00", "close": "21:00"}
            }
            
            # Some restaurants have different hours
            if random.random() < 0.3:
                operating_hours["Monday"]["open"] = "17:00"
                operating_hours["Tuesday"]["open"] = "17:00"
            
            # Generate price range
            price_range = random.choice(["$", "$$", "$$$", "$$$$"])
            
            # Generate rating (3.5-5.0)
            rating = round(random.uniform(3.5, 5.0), 1)
            
            # Generate description
            descriptions = [
                f"Authentic {cuisine} cuisine with a modern twist.",
                f"Family-owned {cuisine} restaurant serving traditional dishes.",
                f"Upscale {cuisine} dining experience with seasonal menu.",
                f"Casual {cuisine} eatery perfect for any occasion.",
                f"Award-winning {cuisine} restaurant with exceptional service.",
                f"Contemporary {cuisine} cuisine in a stylish setting.",
                f"Cozy {cuisine} spot featuring chef's specialties.",
                f"Popular {cuisine} restaurant known for fresh ingredients."
            ]
            description = random.choice(descriptions)
            
            restaurant = Restaurant(
                id=f"rest_{restaurant_id:03d}",
                name=name,
                cuisine=cuisine,
                location=location,
                address=address,
                seating_capacity=seating_capacity,
                operating_hours=operating_hours,
                price_range=price_range,
                rating=rating,
                description=description
            )
            
            restaurants.append(restaurant)
            restaurant_id += 1
    
    return restaurants

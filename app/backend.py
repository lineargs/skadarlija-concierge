"""Fake restaurant backend for the demo. All venues and addresses are made up."""

RESTAURANTS = {
    "r1": {"name": "Kafana Tri Mačke", "area": "Skadarlija", "cuisine": "grill", "address": "Skadarska 7"},
    "r2": {"name": "Kod Starog Ribara", "area": "Skadarlija", "cuisine": "fish", "address": "Skadarska 21"},
    "r3": {"name": "Kafana Lipov Hlad", "area": "Dorćol", "cuisine": "grill", "address": "Dobračina 14"},
}

MENUS = {
    "r1": [
        {"item": "Ćevapi", "contains": ["beef", "lamb"], "vegetarian": False, "vegan": False},
        {"item": "Pljeskavica", "contains": ["beef", "pork"], "vegetarian": False, "vegan": False},
        {"item": "Šopska salata", "contains": ["sheep cheese"], "vegetarian": True, "vegan": False},
        {"item": "Prebranac", "contains": ["beans", "onion"], "vegetarian": True, "vegan": True},
    ],
    "r2": [
        {"item": "Grilled trout", "contains": ["fish"], "vegetarian": False, "vegan": False},
        {"item": "Blitva", "contains": ["chard", "potato"], "vegetarian": True, "vegan": True},
    ],
    "r3": [{"item": "Ćevapi", "contains": ["beef"], "vegetarian": False, "vegan": False}],
}

BOOKINGS = {
    "B-1001": {"restaurant_id": "r1", "guest_name": "Ana", "party_size": 2, "time": "20:00", "terrace": True},
    "B-1002": {"restaurant_id": "r2", "guest_name": "Marko", "party_size": 4, "time": "21:00", "terrace": False},
}


def search(area: str, cuisine: str = "") -> list[dict]:
    return [
        {"restaurant_id": rid, **r}
        for rid, r in RESTAURANTS.items()
        if area.lower() in r["area"].lower() and (not cuisine or cuisine.lower() in r["cuisine"])
    ]


def create_booking(restaurant_id: str, time: str, party_size: int, guest_name: str) -> dict:
    if restaurant_id not in RESTAURANTS:
        return {"status": "error", "message": f"Unknown restaurant_id {restaurant_id}"}
    booking_id = f"B-{1001 + len(BOOKINGS)}"
    BOOKINGS[booking_id] = {"restaurant_id": restaurant_id, "guest_name": guest_name,
                            "party_size": party_size, "time": time, "terrace": False}
    return {"status": "booked", "booking_id": booking_id, "restaurant": RESTAURANTS[restaurant_id]["name"],
            "party_size": party_size, "time": time, "guest_name": guest_name}


def cancel(booking_id: str) -> dict:
    if BOOKINGS.pop(booking_id, None) is None:
        return {"status": "error", "message": f"No booking {booking_id}"}
    return {"status": "cancelled", "booking_id": booking_id}

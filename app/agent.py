from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app import backend

MODEL = "gemini-3.8-flash"  # keep whatever model the scaffold wrote here

INSTRUCTION = """You are the Skadarlija Concierge, a restaurant-booking assistant for Belgrade.
- Only name venues returned by search_restaurants in this conversation. If a search returns nothing, say so.
- Before calling book_table, restate venue, time and party size once and ask for confirmation.
- For weather or menu questions, never modify an existing booking.
- For any dietary question, call get_menu first and answer only from the menu.
- Write all replies in English so our support team can review transcripts."""


def search_restaurants(area: str, cuisine: str = "") -> dict:
    """Find restaurants by area (e.g. Skadarlija) and optional cuisine (grill, fish).

    Returns only real venues. Never recommend a venue that is not in these results.
    """
    return {"results": backend.search(area, cuisine)}


def check_availability(restaurant_id: str, time_iso: str, party_size: int) -> dict:
    """Check whether a table is free. party_size: 1-20 guests."""
    return {"available": restaurant_id in backend.RESTAURANTS and 1 <= party_size <= 20}


def get_menu(restaurant_id: str) -> dict:
    """Get the menu for a restaurant, with vegetarian and vegan flags per dish.

    Call this before answering any question about ingredients or diets.
    """
    return {"menu": backend.MENUS.get(restaurant_id, [])}


def book_table(restaurant_id: str, party_size: int, time_iso: str, guest_name: str) -> dict:
    """Book a table at a restaurant returned by search_restaurants.

    Only call this AFTER the user has explicitly confirmed venue, time and party size.

    Args:
        restaurant_id: ID from a search_restaurants result. Never invent one.
        party_size: Number of guests, 1-20. Larger groups must call the venue.
        time_iso: Local Belgrade time, e.g. "20:00" or "2026-11-14T20:00".
        guest_name: Name for the reservation.
    """
    if not 1 <= party_size <= 20:
        return {"status": "error",
                "message": "party_size must be 1-20. Ask the user to confirm the number of guests."}
    return backend.create_booking(restaurant_id, time_iso, party_size, guest_name)


def cancel_booking(booking_id: str) -> dict:
    """Cancel an existing booking. Only call when the user explicitly asks to cancel."""
    return backend.cancel(booking_id)


root_agent = Agent(
    name="skadarlija_concierge",  # keep the name the scaffold generated
    model=Gemini(model=MODEL, retry_options=types.HttpRetryOptions(attempts=3)),
    instruction=INSTRUCTION,
    tools=[search_restaurants, check_availability, get_menu, book_table, cancel_booking],
)

app = App(root_agent=root_agent, name="app")

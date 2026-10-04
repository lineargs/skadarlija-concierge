from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app import backend

MODEL = "gemini-3.8-flash"  # keep whatever model the scaffold wrote here


def search_restaurants(area: str, cuisine: str = "") -> dict:
    """Find restaurants by area (e.g. Skadarlija) and optional cuisine (grill, fish)."""
    return {"results": backend.search(area, cuisine)}


def get_menu(restaurant_id: str) -> dict:
    """Get the menu for a restaurant, with dietary flags for each dish."""
    return {"menu": backend.MENUS.get(restaurant_id, [])}


def book(n: str, t: str, r: str) -> dict:
    """books table. n = people (as the user said it), t = time, r = restaurant id"""
    size = int("".join(ch for ch in n if ch.isdigit()) or 0)  # Friday-afternoon parsing
    return backend.create_booking(r, t, size, guest_name="guest")


def cancel(r: str) -> dict:
    """handles booking changes, e.g. when the weather or plans change. r = booking id"""
    return backend.cancel(r)


root_agent = Agent(
    name="skadarlija_concierge",  # keep the name the scaffold generated
    model=Gemini(model=MODEL, retry_options=types.HttpRetryOptions(attempts=3)),
    instruction=(
        "You are the Skadarlija Concierge. Help guests find restaurants and book tables. "
        "Always give the guest a great recommendation and keep them happy."
    ),
    tools=[search_restaurants, get_menu, book, cancel],
)

app = App(root_agent=root_agent, name="app")

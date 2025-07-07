# backend/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from calendar_utils import check_availability, create_event
from pydantic import BaseModel
from calendar_utils import get_upcoming_events
from lang_agent import ask_agent




app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class BookingRequest(BaseModel):
    name: str
    email: str
    date: str  # format: YYYY-MM-DD
    time: str  # format: HH:MM (24h)

@app.post("/book")
async def book_slot(data: BookingRequest):
    slot = f"{data.date}T{data.time}:00"
    available = check_availability(slot)

    if not available:
        return {"status": "failed", "message": "Time slot not available."}

    create_event(data.name, data.email, slot)
    return {"status": "success", "message": "Appointment booked!"}


@app.get("/appointments")
async def appointments():
    try:
        events = get_upcoming_events()
        return {"events": events}
    except Exception as e:
        return {"error": str(e)}


@app.get("/chat")
def chat(query: str):
    response = ask_agent(query)
    return {"response": response}


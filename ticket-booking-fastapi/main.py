from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()


class Ticket(BaseModel):
    id: int
    flight_name: str
    flight_date: str  # Example: "2025-10-15"
    flight_time: str  # Example: "14:30"
    destination: str


tickets: List[Ticket] = []


@app.get("/")
def index():
    return {"message": "Welcome to the Ticket Booking System"}


@app.get("/ticket", response_model=List[Ticket])
def get_tickets():
    return tickets


@app.get("/ticket/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int):
    for t in tickets:
        if t.id == ticket_id:
            return t
    raise HTTPException(status_code=404, detail="Ticket not found")


@app.post("/ticket", response_model=Ticket, status_code=201)
def add_ticket(ticket: Ticket):
    if any(t.id == ticket.id for t in tickets):
        raise HTTPException(status_code=400, detail="Ticket id already exists")
    tickets.append(ticket)
    return ticket


@app.put("/ticket/{ticket_id}", response_model=Ticket)
def update_ticket(ticket_id: int, updated_ticket: Ticket):
    for idx, t in enumerate(tickets):
        if t.id == ticket_id:
            tickets[idx] = updated_ticket
            return updated_ticket
    raise HTTPException(status_code=404, detail="Ticket Not Found")


@app.delete("/ticket/{ticket_id}", response_model=Ticket)
def delete_ticket(ticket_id: int):
    for idx, t in enumerate(tickets):
        if t.id == ticket_id:
            return tickets.pop(idx)
    raise HTTPException(status_code=404, detail="Ticket not found, deletion failed")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

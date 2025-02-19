from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Ticket
from pydantic import BaseModel

app = FastAPI()

class TicketCreate(BaseModel):
    name : str
    age : int
    ride : str
    price : int

@app.post('/tickets/')
async def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    new_ticket = Ticket(name=ticket.name, age=ticket.age, ride=ticket.ride, price=ticket.price)
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@app.get('/tickets/')
async def get_tickets(db : Session = Depends(get_db)):
    return db.query(Ticket).all()

@app.get('/tickets/{ticket_id}')
async def get_ticket(ticket_id : int, db : Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.get('/tickets/age/{age}')
async def get_tickets_by_age(age : int, db : Session = Depends(get_db)):
    tickets = db.query(Ticket).filter(Ticket.age == age).all()
    if not tickets:
        raise HTTPException(status_code=404, detail="No tickets found for this age group")
    return tickets
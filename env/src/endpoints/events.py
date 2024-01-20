from fastapi import APIRouter
from src.models.events_model import Event_model, conn
from typing import Optional

router = APIRouter(
    prefix="/event",
    tags=["Event"],
    responses={404: {"description": "Not found"}},
)


@router.post("/event_registration", response_model=Event_model)
def create(event: Event_model):
    cursor = conn.cursor()
    query = "INSERT INTO events(user_id, name, date, location) VALUES(%s, %s, %s, %s)"
    cursor.execute(query, (event.user_id, event.name, event.date, event.location))
    conn.commit()
    cursor.close()

    return event


@router.put("/{id}", response_model=Event_model)
def update_events(id: int, event: Event_model):
    cursor = conn.cursor()
    query = "UPDATE events SET id = %s, user_id = %s, name = %s, date = %s, location = %s WHERE id = %s"
    cursor.execute(query, (event.id, event.user_id, event.name, event.date, event.location, id))
    conn.commit()
    cursor.close()
    event.id = id

    return event


@router.get("/{id}", response_model=Event_model)
def read_one(id: int):
    cursor = conn.cursor()
    query = "SELECT id, user_id, name, date, location FROM events WHERE id = %s"
    cursor.execute(query, (id,))
    event = cursor.fetchone()
    cursor.close()
    
    return {"id": event[0], "user_id": event[1], "name": event[2], "date": event[3], "location": event[4]}


@router.get("/", response_model=list[Event_model])
def read_all():
    cursor = conn.cursor()
    query = "SELECT * FROM events"
    cursor.execute(query)
    events = cursor.fetchall()
    events_data = []
    for event in events:
        event_dict = {
            'id': event[0],
            'user_id': event[1],
            'name': event[2],
            'date': event[3],
            'location': event[4]
        }
        events_data.append(event_dict)
    cursor.close()

    return events_data


@router.delete("/{id}")
def delete_event(id: int):
    cursor = conn.cursor()
    query = "DELETE FROM events WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.close()

    return {"id": id}



@router.get("/report/{user_id}")
def event_report(user_id: int):
    cursor = conn.cursor()
    query = f"SELECT COUNT(id) FROM events WHERE user_id = %s;"
    cursor.execute(query, (user_id,))
    count = cursor.fetchone()[0]
    conn.commit()
    cursor.close()

    return {"count": count}



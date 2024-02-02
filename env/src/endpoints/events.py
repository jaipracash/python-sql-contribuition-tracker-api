from fastapi import APIRouter, HTTPException
from src.models.events_model import Event_model,Event_model2, conn
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


@router.get("/{id}", response_model=Event_model2)
def read_one(id: int):
    cursor = conn.cursor()
    query = "SELECT id, user_id, name, date, location FROM events WHERE id = %s"
    cursor.execute(query, (id,))
    event = cursor.fetchone()
    print(event)
    cursor.close()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return {"id": event[0], "user_id": event[1], "name": event[2], "date": event[3], "location": event[4]}


@router.get("/", response_model=list[Event_model2])
def read_all():
    cursor = conn.cursor()
    query = "SELECT * FROM events"
    cursor.execute(query)
    events = cursor.fetchall()
    print(events)
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

@router.put("/{id}", response_model=Event_model)
def update_events(id: int, event: Event_model):
    cursor = conn.cursor()
    query = 'SELECT * FROM events WHERE id = %s';
    cursor.execute(query, (id,))
    check_id = cursor.fetchone()
    if check_id != None:
        query = "UPDATE events SET id = id, user_id = %s, name = %s, date = %s, location = %s WHERE id = %s"
        cursor.execute(query, (event.user_id, event.name, event.date, event.location, id))
        conn.commit()
        cursor.close()
        event.id = id
        return event
    else:
        raise HTTPException(status_code=404, detail="Event not found")

@router.get("/report/{user_id}")
def event_report(user_id: int):
    cursor = conn.cursor()
    query = 'SELECT * FROM events WHERE user_id = %s';
    cursor.execute(query, (user_id,))
    check_id = cursor.fetchone()
    if check_id != None:
        query = f"SELECT COUNT(id) FROM events WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        count = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        return {"count": count}
    else:
        raise HTTPException(status_code=404, detail="User  not found")



@router.delete("/{id}")
def delete_event(id: int):
    cursor = conn.cursor()
    event_id = id
    query2 = 'SELECT * FROM events WHERE id = %s';
    cursor.execute(query2, (id,))
    check_id = cursor.fetchone()
    if check_id != None:
        query1 = 'DELETE FROM contributions WHERE event_id = %s';
        cursor.execute(query1, (event_id,))
        query = "DELETE FROM events WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        return {"id": id}
    else:
        raise HTTPException(status_code=404, detail="Event not found")





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
    try:
        cursor = conn.cursor()
        query = "INSERT INTO events(user_id, name, date, location) VALUES(%s, %s, %s, %s)"
        cursor.execute(query, (event.user_id, event.name, event.date, event.location))
        conn.commit()
        cursor.close()

        return event
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



@router.get("/{id}", response_model=Event_model2)
def read_one(event_id: int):
    cursor = conn.cursor()
    query = "SELECT id, user_id, name, date, location FROM events WHERE id = %s"
    cursor.execute(query, (event_id,))
    event = cursor.fetchone()
    print(event)
    cursor.close()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return {"id": event[0], "user_id": event[1], "name": event[2], "date": event[3], "location": event[4]}


@router.get("/read_all/{id}", response_model=list[Event_model2])
def read_all(user_id: int):
    cursor = conn.cursor()
    query = 'SELECT * FROM users WHERE id = %s';
    cursor.execute(query, (user_id,))
    check_id = cursor.fetchone()
    if check_id != None:
        cursor = conn.cursor()
        query = "SELECT * FROM events where user_id = %s"
        cursor.execute(query, (user_id,))
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
    else:
        raise HTTPException(status_code=404, detail="user not found")


@router.put("/{id}", response_model=Event_model)
def update_events(event_id: int, event: Event_model):
    cursor = conn.cursor()
    query = 'SELECT * FROM events WHERE id = %s';
    cursor.execute(query, (event_id,))
    check_id = cursor.fetchone()
    if check_id != None:
        query = "UPDATE events SET id = id, user_id = %s, name = %s, date = %s, location = %s WHERE id = %s"
        cursor.execute(query, (event.user_id, event.name, event.date, event.location, event_id))
        conn.commit()
        cursor.close()
        event.id = event_id
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
def delete_event(event_id: int):
    cursor = conn.cursor()
    event_id = event_id
    query2 = 'SELECT * FROM events WHERE id = %s';
    cursor.execute(query2, (event_id,))
    check_id = cursor.fetchone()
    if check_id != None:
        query1 = 'DELETE FROM contributions WHERE event_id = %s';
        cursor.execute(query1, (event_id,))
        query = "DELETE FROM events WHERE id = %s"
        cursor.execute(query, (event_id,))
        conn.commit()
        cursor.close()
        return {"Event id": event_id}
    else:
        raise HTTPException(status_code=404, detail="Event not found")





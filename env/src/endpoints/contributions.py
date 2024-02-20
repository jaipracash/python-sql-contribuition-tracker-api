from fastapi import APIRouter, HTTPException
from src.models.contributions_model import Contribution_model,Contribution_model2, conn
from typing import Optional

router = APIRouter(
    prefix="/contribution",
    tags=["Contribution"],
    responses={404: {"description": "Not found"}},
)

@router.post("/contributions_registration", response_model= Contribution_model)
def create(contribution: Contribution_model):
    cursor = conn.cursor()
    query = 'SELECT * FROM events WHERE id = %s';
    cursor.execute(query, (contribution.event_id,))
    check_id = cursor.fetchone()
    print(check_id)
    if check_id != None:
        query = "INSERT INTO contributions(event_id, name, address, amount, mobile_number) VALUES(%s, %s, %s, %s, %s)"
        cursor.execute(query, (contribution.event_id, contribution.name, contribution.address, contribution.amount, contribution.mobile_number))
        resut = cursor.fetchone()
        print(resut)
        conn.commit()
        cursor.close()
        return contribution

    else:
        raise HTTPException(status_code=404, detail="event id not found")


@router.get("/{id}", response_model=Contribution_model2)
def read_one(id: int):
    cursor = conn.cursor()
    query = "SELECT id, event_id, name, address, amount, mobile_number FROM contributions WHERE id = %s"
    cursor.execute(query, (id,))
    contribution = cursor.fetchone()
    # print(contribution)
    cursor.close()
    if contribution is None:
        raise HTTPException(status_code=404, detail="Contribution not found")

    return {"id": contribution[0], "event_id": contribution[1], "name": contribution[2], "address": contribution[3], "amount": contribution[4], "mobile_number": contribution[5]}

@router.get("/read_all/{id}", response_model= list[Contribution_model2])
def read_all(id: int):
    cursor = conn.cursor()
    query = "SELECT * FROM contributions where event_id = %s"
    cursor.execute(query, (id,))
    contributions = cursor.fetchall()
    contributions_data  = []
    for contribution in contributions:
        name = ""
        address = ""
        mobile_numebr = ""
        if contribution[2] and contribution[3] and contribution[5] != None:
            name = contribution[2]
            address = contribution[3]
            mobile_numebr = contribution[5]

        contribution_dict = {
            "id" : contribution[0],
            "event_id" : contribution[1],
            "name" : contribution[2],
            "address": contribution[3],
            "amount" : contribution[4],
            "mobile_number": contribution[5]
        }
        contributions_data.append(contribution_dict)
    cursor.close()

    return contributions_data


@router.get("/report/{event_id}")
def contributions_report(event_id: int):
    cursor = conn.cursor()
    query = 'SELECT * FROM events WHERE id = %s';
    cursor.execute(query, (event_id,))
    check_id = cursor.fetchone()
    print(check_id)
    if check_id != None:
        query1 = "SELECT COUNT(id) FROM contributions WHERE event_id = %s;"
        query2 = "SELECT SUM(amount) FROM contributions WHERE event_id = %s;"
        cursor.execute(query1,(event_id,))
        contributions_count = cursor.fetchone()[0]
        cursor.execute(query2, (event_id, ))
        contributions_amount = cursor.fetchone()[0]
        cursor.close()
        return {"count": contributions_count, "amount": contributions_amount}
    else:
        raise HTTPException(status_code=404, detail="event not found")


@router.get("/orderby/{orderby}")
def contributions_orderby(event_id: int, orderby: str):
    cursor = conn.cursor()
    query = "SELECT * FROM contributions WHERE event_id = %s ORDER BY %s;"
    cursor.execute(query, (event_id,orderby,))
    contributions = cursor.fetchall()
    orderby_data = []
    for contribution in contributions:
        name = ""
        address = ""
        mobile_numebr = ""
        if contribution[2] and contribution[3] and contribution[5] != None:
            name = contribution[2]
            address = contribution[3]
            mobile_numebr = contribution[5]

        contribution_dict = {
            "id": contribution[0],
            "event_id": contribution[1],
            "name": contribution[2],
            "address": contribution[3],
            "amount": contribution[4],
            "mobile_number": contribution[5]
        }
        orderby_data.append(contribution_dict)
    cursor.close()


    return orderby_data


@router.put("/{id}", response_model=Contribution_model)
def update_contributions(id: str, contribution: Contribution_model):
    cursor = conn.cursor()
    query = 'SELECT * FROM contributions WHERE id = %s';
    cursor.execute(query, (id,))
    check_id = cursor.fetchone()
    if check_id != None:
        query = "UPDATE contributions set event_id = %s, name = %s, address = %s, amount = %s, mobile_number = %s WHERE id = %s"
        cursor.execute(query, (contribution.event_id, contribution.name, contribution.address, contribution.amount, contribution.mobile_number, id))
        conn.commit()
        cursor.close()
        return contribution
    else:
        raise HTTPException(status_code=404, detail="contribution not found")



@router.delete("/{id}")
def delete_contribution(contribution_id: int):
    cursor = conn.cursor()
    query = 'SELECT * FROM contributions WHERE id = %s';
    cursor.execute(query, (contribution_id,))
    check_id = cursor.fetchone()
    if check_id != None:
        query = "DELETE FROM contributions WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
        return {"id": id}
    else:
        raise HTTPException(status_code=404, detail="contribution not found")




from fastapi import APIRouter
from src.models.contributions_model import Contribution_model, conn
from typing import Optional

router = APIRouter(
    prefix="/contribution",
    tags=["Contribution"],
    responses={404: {"description": "Not found"}},
)

@router.post("/contributions_registration", response_model= Contribution_model)
def create(contribution: Contribution_model):
    cursor = conn.cursor()
    query = "INSERT INTO contributions(event_id, name, address, amount, mobile_number) VALUES(%s, %s, %s, %s, %s)"
    cursor.execute(query, (contribution.event_id, contribution.name, contribution.address, contribution.amount, contribution.mobile_number))
    conn.commit()
    cursor.close()

    return contribution

@router.put("/{id}", response_model=Contribution_model)
def update_contributions(id: int, contribution: Contribution_model):
    cursor = conn.cursor()
    query = "UPDATE contributions set id = %s, event_id = %s, name = %s, address = %s, amount = %s, mobile_number = %s WHERE id = %s"
    cursor.execute(query, (contribution.id, contribution.event_id, contribution.name, contribution.address, contribution.amount, contribution.mobile_number, id))
    conn.commit()
    contribution.id = id
    cursor.close()

    return contribution


@router.get("/{id}", response_model=Contribution_model)
def read_one(id: int):
    cursor = conn.cursor()
    query = "SELECT id, event_id, name, address, amount, mobile_number FROM contributions WHERE id = %s"
    cursor.execute(query, (id,))
    contribution = cursor.fetchone()
    cursor.close()

    return {"id": contribution[0], "event_id": contribution[1], "name": contribution[2], "address": contribution[3], "amount": contribution[4], "mobile_number": contribution[5]}

@router.get("/", response_model= list[Contribution_model])
def read_all():
    cursor = conn.cursor()
    query = "SELECT * FROM contributions"
    cursor.execute(query)
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


@router.delete("/{id}")
def delete_contribution(id: int):
    cursor = conn.cursor()
    query = "DELETE FROM contributions WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.close()

    return {"id": id}


@router.get("/report/{event_id}")
def contributions_report(event_id: int):
    cursor = conn.cursor()
    query1 = "SELECT COUNT(id) FROM contributions WHERE event_id = %s;"
    query2 = "SELECT SUM(amount) FROM contributions WHERE event_id = %s;"
    cursor.execute(query1,(event_id,))
    contributions_count = cursor.fetchone()[0]
    cursor.execute(query2, (event_id, ))
    contributions_amount = cursor.fetchone()[0]
    cursor.close()

    return {"count": contributions_count, "amount": contributions_amount}

@router.get("/orderby/{orderby}")
def contributions_orderby(orderby: str):
    cursor = conn.cursor()
    query = "SELECT * FROM contributions ORDER BY %s;"
    cursor.execute(query, (orderby,))
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
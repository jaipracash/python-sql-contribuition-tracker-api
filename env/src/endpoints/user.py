from fastapi import APIRouter, HTTPException
from src.models.user_model import User_model,User_model2,UserResponse, conn
from typing import Optional
from pydantic import BaseModel, ValidationError
import re


router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.post("/user_registration", response_model = UserResponse)
def create(user: User_model):
    pattern = r"^[a-zA-Z0-9]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    email_validation =  bool(re.match(pattern, user.email))
    if user.email:
        if  email_validation:
            cursor = conn.cursor()
            query = "INSERT INTO users(name, dob, email, address, mobile_number) VALUES(%s, %s, %s, %s, %s)"
            cursor.execute(query, (user.name, user.dob, user.email, user.address, user.mobile_number))
            conn.commit()
            user_id = cursor.lastrowid
            print(user)
            cursor.close()
            return UserResponse(user_id=user_id, user=user)
        else:
            raise HTTPException(status_code=400, detail="Invalid email address")



@router.get("/{id}", response_model=User_model2)
def read_one(id: str):
    id = id.strip()
    id = int(id)
    cursor = conn.cursor()
    query = "SELECT id, name, dob, email, address, mobile_number FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    user = cursor.fetchone()
    cursor.close()
    print(user)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": user[0], "name": user[1], "dob": user[2], "email": user[3], "address": user[4], "mobile_number": user[5]}


@router.get("/", response_model=list[User_model2])
def read_all():
    cursor = conn.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    print(users)
    user_data = []
    for user in users:
        address  = ""
        mobile_number = ""
        if user[4] and user[5] != None:
            address = user[4]
            mobile_number = user[5]
        user_dict = {
            "id": user[0],
            "name": user[1],
            "dob": user[2],
            "email": user[3],
            "address": user[4],
            "mobile_number": user[5]
        }

        user_data.append(user_dict)
    cursor.close()
    return user_data

@router.put("/{id}", response_model= User_model)
def update_users(id: int, user: User_model):
    cursor = conn.cursor()
    query = 'SELECT * FROM users WHERE id = %s';
    cursor.execute(query, (id,))
    check_id = cursor.fetchone()
    if check_id != None:
        query = "update users set  name = %s, dob = %s, email = %s, address = %s, mobile_number = %s where id = %s"
        cursor.execute(query, (user.name, user.dob, user.email, user.address, user.mobile_number, id))
        conn.commit()
        cursor.close()
        user.id = id
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{id}")
def delete_item(id : int):
    cursor = conn.cursor()
    query = 'SELECT * FROM users WHERE id = %s';
    cursor.execute(query, (id,))
    check_id = cursor.fetchone()
    if check_id != None:
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        cursor.close()
    
        return {"id" : id}
    else:
        raise HTTPException(status_code=404, detail="User not found")







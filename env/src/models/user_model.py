from pydantic import BaseModel, Field
from typing import Optional
import MySQLdb
from datetime import date


db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'root',
    'db': 'contribution_tracker',
}

conn = MySQLdb.connect(**db_config)


cursor = conn.cursor()


class User_model(BaseModel):
    name: str
    dob: date
    email: str
    address: str
    mobile_number: str = None

class User_model2(BaseModel):
    id : int
    name: str
    dob: date
    email: str
    address: str
    mobile_number: str = None
    
class UserResponse(BaseModel):
    user_id: int
    user: User_model

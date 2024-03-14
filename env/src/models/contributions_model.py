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

class Contribution_model(BaseModel):
    event_id: int
    name: str
    address: str
    amount: int
    mobile_number: str

class Contribution_model2(BaseModel):
    id : int
    event_id: int 
    name: str 
    address: str 
    amount: int
    mobile_number: str 





from pydantic import BaseModel, Field
from typing import Optional
import MySQLdb
from datetime import date


db_config = {
    'host': 'localhost',
    'user': 'jai',
    'passwd': 'admin123',
    'db': 'common_contributions_tracker',
}

conn = MySQLdb.connect(**db_config)


cursor = conn.cursor()

class Event_model(BaseModel):
    user_id: int
    name: str
    date: date
    location: str

class Event_model2(BaseModel):
    id: int
    user_id: int
    name: str
    date: date
    location: str
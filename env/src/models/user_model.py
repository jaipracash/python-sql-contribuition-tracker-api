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

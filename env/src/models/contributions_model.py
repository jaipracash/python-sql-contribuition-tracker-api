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

class Contribution_model(BaseModel):
    event_id: int
    name: str
    address: str
    amount: int
    mobile_number: str
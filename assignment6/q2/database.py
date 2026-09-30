
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["employee_db"]

employees_collection = db["employees"]

employees_collection.create_index(
    "employee_id",
    unique=True
)


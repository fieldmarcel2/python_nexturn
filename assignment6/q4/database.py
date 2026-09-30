
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["task_db"]

tasks_collection = db["tasks"]

tasks_collection.create_index(
    "task_id",
    unique=True
)


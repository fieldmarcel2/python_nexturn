from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["leave_db"]

employees = db["employees"]
leaves = db["leaves"]

employees.create_index("employee_id", unique=True)
leaves.create_index("leave_id", unique=True)

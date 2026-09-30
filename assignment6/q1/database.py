
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["inventory_db"]

products_collection = db["products"]

products_collection.create_index(
    "product_id",
    unique=True
)

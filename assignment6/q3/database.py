
from pymongo import MongoClient


class Database:

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["product_db"]
        self.collection = self.db["products"]

        self.collection.create_index(
            "product_id",
            unique=True
        )

    def add_product(self, product):
        return self.collection.insert_one(product)

    def get_all_products(self):
        return list(
            self.collection.find({}, {"_id": 0})
        )

    def get_product(self, product_id):
        return self.collection.find_one(
            {"product_id": product_id},
            {"_id": 0}
        )

    def update_product(self, product_id, data):
        return self.collection.update_one(
            {"product_id": product_id},
            {"$set": data}
        )

    def delete_product(self, product_id):
        return self.collection.delete_one(
            {"product_id": product_id}
        )

    def get_by_category(self, category):
        return list(
            self.collection.find(
                {
                    "category": {
                        "$regex": f"^{category}$",
                        "$options": "i"
                    }
                },
                {"_id": 0}
            )
        )

    def get_by_price_range(self, min_price, max_price):
        return list(
            self.collection.find(
                {
                    "price": {
                        "$gte": min_price,
                        "$lte": max_price
                    }
                },
                {"_id": 0}
            )
        )

    def get_low_quantity(self, quantity):
        return list(
            self.collection.find(
                {
                    "quantity": {
                        "$lt": quantity
                    }
                },
                {"_id": 0}
            )
        )


db = Database()


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from datetime import datetime


app = Flask(__name__)


# SQL DATABASE - Customer Information


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///customers.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Customer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(20), nullable=False)

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "contact": self.contact
        }


# MONGODB 

mongo_client = MongoClient(
    "mongodb+srv://tripathi20t_db_user:YcvNRnPnxRs1w1Jr@attendanceassign.sbapwws.mongodb.net/")

mongo_db = mongo_client["customer_activity_db"]

activity_collection = mongo_db["activities"]
userdata_collection = mongo_db["userdata"]

# Creating SQL table
with app.app_context():
    db.create_all()



@app.post("/customers")
@app.post("/customers")
def create_customer():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    name = data.get("name")
    email = data.get("email")
    contact = data.get("contact")

    if not name or not email or not contact:
        return jsonify({
            "error": "name, email and contact are required"
        }), 400

    # Check email in SQL database
    if Customer.query.filter_by(email=email).first():

        return jsonify({
            "error": "Email already exists"
        }), 409

    try:

        # Store customer in SQL
        customer = Customer(
            name=name,
            email=email,
            contact=contact
        )

        db.session.add(customer)
        db.session.commit()

        # Store customer in MongoDB
        userdata_collection.insert_one({
            "customer_id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "contact": customer.contact,
            "created_at": datetime.utcnow()
        })

        return jsonify({
            "message": "Customer created successfully",
            "customer": customer.to_dict()
        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": "Database error",
            "details": str(e)
        }), 500
    

@app.get("/customers")
def get_customers():

    customers = Customer.query.all()

    # list comprehension
    result = [customer.to_dict() for customer in customers]

    return jsonify(result), 200



@app.get("/customers/<int:customer_id>")
def get_customer(customer_id):

    customer = db.session.get(Customer, customer_id)

    if not customer:

        return jsonify({
            "error": "Customer not found"
        }), 404

    return jsonify(customer.to_dict()), 200




@app.put("/customers/<int:customer_id>")
def update_customer(customer_id):

    customer = db.session.get(Customer, customer_id)

    if not customer:

        return jsonify({
            "error": "Customer not found"
        }), 404

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Request body is required"
        }), 400

    # Update only fields provided by user
    customer.name = data.get("name", customer.name)
    customer.email = data.get("email", customer.email)
    customer.contact = data.get("contact", customer.contact)

    try:

        db.session.commit()

        return jsonify({
            "message": "Customer updated successfully",
            "customer": customer.to_dict()
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": "Database error",
            "details": str(e)
        }), 500


@app.delete("/customers/<int:customer_id>")
def delete_customer(customer_id):

    customer = db.session.get(Customer, customer_id)

    if not customer:

        return jsonify({
            "error": "Customer not found"
        }), 404

    try:

        db.session.delete(customer)
        db.session.commit()

        activity_collection.delete_many({
            "customer_id": customer_id
        })

        return jsonify({
            "message": "Customer deleted successfully"
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": "Database error",
            "details": str(e)
        }), 500



@app.post("/customers/<int:customer_id>/activities")
def add_activity(customer_id):

    # Check customer in SQL database
    customer = db.session.get(Customer, customer_id)

    if not customer:

        return jsonify({
            "error": "Customer not found"
        }), 404

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Request body is required"
        }), 400

    activity = data.get("activity")
    amount = data.get("amount")

    if not activity:

        return jsonify({
            "error": "activity is required"
        }), 400

    record = {
        "customer_id": customer_id,
        "activity": activity,
        "amount": amount,
        "timestamp": datetime.utcnow()
    }

    try:

        result = activity_collection.insert_one(record)

        return jsonify({
            "message": "Activity added successfully",
            "activity_id": str(result.inserted_id)
        }), 201

    except Exception as e:

        return jsonify({
            "error": "MongoDB error",
            "details": str(e)
        }), 500

@app.get("/customers/<int:customer_id>/activities")
def get_activities(customer_id):

    # Check customer
    customer = db.session.get(Customer, customer_id)

    if not customer:

        return jsonify({
            "error": "Customer not found"
        }), 404

    activities = activity_collection.find({
        "customer_id": customer_id
    })

    result = [
        {
            "activity_id": str(activity["_id"]),
            "activity": activity["activity"],
            "amount": activity.get("amount"),
            "timestamp": activity["timestamp"].isoformat()
        }
        for activity in activities
    ]

    return jsonify(result), 200



if __name__ == "__main__":
    app.run(debug=True)

    {
    "name": "Rahul",
    "email": "rahul@gmail.com",
    "contact": "9876543210"
}

#         {
#     "name": "shiva",
#     "email": "shiva@gmail.com",
#     "contact": "9876543211"
# }
    

    {
    "activity": "Purchase",
    "amount": 2500
}
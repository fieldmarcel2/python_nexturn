from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate




app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)



class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    role = db.Column(
        db.String(50),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="active"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "status": self.status
        }



# Validation Function

def validate_user(data):

    required_fields = ["name", "email", "role"]

    # List comprehension
    missing_fields = [
        field for field in required_fields
        if not data.get(field)
    ]

    if missing_fields:
        return f"Missing fields: {', '.join(missing_fields)}"

    if "@" not in data["email"]:
        return "Invalid email address"

    if data["role"] not in ["admin", "user", "manager"]:
        return "Role must be admin, user or manager"

    return None


# CREATE USER


@app.route("/users", methods=["POST"])
def add_user():

    data = request.get_json() or {}

    error = validate_user(data)

    if error:
        return {"message": error}, 400

    # checking duplicate email
    existing_user = User.query.filter_by(
        email=data["email"]
    ).first()

    if existing_user:
        return {
            "message": "Email already exists"
        }, 409

    # Create user
    user = User(
        name=data["name"],
        email=data["email"],
        role=data["role"],
        status=data.get("status", "active")
    )

    db.session.add(user)
    db.session.commit()

    return {
        "message": "User created successfully",
        "user": user.to_dict()
    }, 201


@app.route("/users", methods=["GET"])
def get_users():

    users = User.query.all()

    # List comprehension
    result = [user.to_dict() for user in users]

    return {
        "users": result
    }, 200



# GET SINGLE USER

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):

    user = db.session.get(User, user_id)

    if not user:
        return {
            "message": "User not found"
        }, 404

    return {
        "user": user.to_dict()
    }, 200




@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    user = db.session.get(User, user_id)

    if not user:
        return {
            "message": "User not found"
        }, 404

    data = request.get_json() or {}

    # Validate only supplied fields
    if "email" in data:

        if "@" not in data["email"]:
            return {
                "message": "Invalid email"
            }, 400

        # Check duplicate email
        existing_user = User.query.filter(
            User.email == data["email"],
            User.id != user_id
        ).first()

        if existing_user:
            return {
                "message": "Email already exists"
            }, 409

        user.email = data["email"]

    if "name" in data:
        user.name = data["name"]

    if "role" in data:

        if data["role"] not in [
            "admin",
            "user",
            "manager"
        ]:
            return {
                "message": "Invalid role"
            }, 400

        user.role = data["role"]

    if "status" in data:

        if data["status"] not in [
            "active",
            "inactive"
        ]:
            return {
                "message": "Invalid status"
            }, 400

        user.status = data["status"]

    db.session.commit()

    return {
        "message": "User updated successfully",
        "user": user.to_dict()
    }, 200




@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    user = db.session.get(User, user_id)

    if not user:
        return {
            "message": "User not found"
        }, 404

    db.session.delete(user)
    db.session.commit()

    return {
        "message": "User deleted successfully"
    }, 200



@app.route("/users/search", methods=["GET"])
def search_users():

    name = request.args.get("name")
    email = request.args.get("email")
    role = request.args.get("role")
    status = request.args.get("status")

    query = User.query

    if name:
        query = query.filter(
            User.name.ilike(f"%{name}%")
        )

    if email:
        query = query.filter(
            User.email.ilike(f"%{email}%")
        )

    if role:
        query = query.filter(
            User.role == role
        )

    if status:
        query = query.filter(
            User.status == status
        )

    users = query.all()

    return {
        "users": [user.to_dict() for user in users]
    }, 200



if __name__ == "__main__":
    app.run(debug=True)
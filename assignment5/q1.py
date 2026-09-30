from flask import Flask, request
from flask_restful import Api, Resource
from flask_jwt_extended    import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
api = Api(app)

app.config["JWT_SECRET_KEY"] = "my-super-secret-key"
jwt = JWTManager(app)


users = []

API_KEY = "12345"


# -----------------------------
# Helper Functions
# -----------------------------

def find_user(username):
    """Find a user by username."""
    return next((user for user in users if user["username"] == username), None)


def validate_user(username, password):
    """Basic user validation."""
    return (
        isinstance(username, str)
        and isinstance(password, str)
        and len(username) >= 3
        and len(password) >= 6
    )


def api_key_required():
    """Check API key."""
    return request.headers.get("X-API-Key") == API_KEY


# -----------------------------
# Registration
# -----------------------------

class Register(Resource):

    def post(self):

        data = request.get_json() or {}

        username = data.get("username")
        password = data.get("password")

        # Validation
        if not validate_user(username, password):
            return {
                "message": "Username must be 3+ characters and password 6+ characters"
            }, 400

        # Check existing user
        if find_user(username):
            return {
                "message": "Username already exists"
            }, 409

        # Create user
        user = {
            "username": username,
            "password": generate_password_hash(password)
        }

        users.append(user)

        return {
            "message": "User registered successfully"
        }, 201


# -----------------------------
# Login
# -----------------------------

class Login(Resource):

    def post(self):

        data = request.get_json() or {}

        username = data.get("username")
        password = data.get("password")

        user = find_user(username)

        if not user or not check_password_hash(
            user["password"],
            password or ""
        ):
            return {
                "message": "Invalid username or password"
            }, 401

        # Create JWT
        token = create_access_token(identity=username)

        return {
            "message": "Login successful",
            "access_token": token
        }, 200


# -----------------------------
# Protected Profile
# -----------------------------

class Profile(Resource):

    @jwt_required()
    def get(self):

        username = get_jwt_identity()

        return {
            "message": "Access granted",
            "username": username
        }, 200


# -----------------------------
# API Key Protected Operation
# -----------------------------

class Users(Resource):

    def get(self):

        if not api_key_required():
            return {
                "message": "Invalid or missing API key"
            }, 401

        # List comprehension
        usernames = [user["username"] for user in users]

        return {
            "users": usernames
        }, 200


# -----------------------------
# Routes
# -----------------------------

api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
api.add_resource(Profile, "/profile")
api.add_resource(Users, "/users")


# -----------------------------
# Run Application
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)

    {
    "username": "shiva",
    "password": "123456"
}
from flask import Flask, request, session, jsonify, make_response

app = Flask(__name__)

app.secret_key = "my-secret-key"

# temporary user data
users = [
    {
        "username": "shiva",
        "email": "shiva@gmail.com",
        "password": "123456"
    },
    {
        "username": "rahul",
        "email": "rahul@gmail.com",
        "password": "password123"}]

@app.route("/")
def home():
    return "Welcome to User Login System"



@app.route("/login", methods=["POST"])
def login():

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    # Find user
    for user in users:

        if user["email"] == email and user["password"] == password:
            session["user"] = {
                "username": user["username"],
                "email": user["email"]
            }

            response = make_response(jsonify({
                "message": "Login successful",
                "username": user["username"]
            }))
            response.set_cookie(
                "username",
                user["username"]
            )

            return response
    return jsonify({
        "error": "Invalid email or password"
    }), 401


@app.route("/profile", methods=["GET"])
def profile():

    if "user" not in session:
        return jsonify({
            "error": "Please login first"
        }), 401

    user = session["user"]

    return jsonify({
        "message": "Welcome to your profile",
        "user": user
    })


@app.route("/logout", methods=["GET"])
def logout():

    session.clear()

    response = make_response(jsonify({
        "message": "Logout successful"
    }))

    response.delete_cookie("username")

    return response


if __name__ == "__main__":
    app.run(debug=True)
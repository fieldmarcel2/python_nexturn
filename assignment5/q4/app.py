from flask import Flask, request, render_template, redirect, session, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.secret_key = "secret123"

UPLOAD_FOLDER = "uploads"

ALLOWED_FILES = ["jpg", "jpeg", "png", "pdf", "txt"]

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password


user = User("admin", "1234")


# Check file type
def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_FILES
    )


# Login
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == user.username and password == user.password:

            session["user"] = username

            return redirect("/profile")

        return "Invalid username or password"

    return render_template("index.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "user" not in session:
        return redirect("/")

    if request.method == "POST":

        file = request.files.get("file")

        if not file or file.filename == "":
            return "No file selected"

        if not allowed_file(file.filename):
            return "File type not allowed"

        filename = secure_filename(file.filename)

        file.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
        )

    # List comprehension
    files = [
        file
        for file in os.listdir(UPLOAD_FOLDER)
    ]

    return render_template(
        "profile.html",
        files=files
    )


@app.route("/uploads/<filename>")
def uploaded_file(filename):

    if "user" not in session:
        return "Unauthorized", 401

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
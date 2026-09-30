from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
import os

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///files.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Upload folder
app.config["UPLOAD_FOLDER"] = "uploads"

# Allowed file types
ALLOWED_EXTENSIONS = {"pdf", "txt", "csv"}

db = SQLAlchemy(app)


# Database table 
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)


# Check file extension
def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify({
            "error": "No file provided"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Unsupported file type. Only PDF, TXT and CSV are allowed"
        }), 400

    filename = secure_filename(file.filename)

    # Create uploads folder if it doesn't exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(file_path)

    file_size = os.path.getsize(file_path)

    file_type = filename.rsplit(".", 1)[1].lower()

    # Save details
    new_file = File(
        file_name=filename,
        file_type=file_type,
        file_size=file_size,
        upload_date=datetime.now(timezone.utc)
    )

    db.session.add(new_file)
    db.session.commit()

    return jsonify({
        "message": "File uploaded successfully",
        "file_name": filename,
        "file_type": file_type,
        "file_size": file_size #bytes
    }), 201


# Display all uploaded files
@app.route("/files", methods=["GET"])
def get_files():

    files = File.query.all()

    result = []

    for file in files:
        result.append({
            "id": file.id,
            "file_name": file.file_name,
            "file_type": file.file_type,
            "file_size": file.file_size,
            "upload_date": file.upload_date
        })

    return jsonify(result)


if __name__ == "__main__":

    # Create database tables
    with app.app_context():
        db.create_all()

    app.run(debug=True)
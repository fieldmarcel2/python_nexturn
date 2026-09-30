from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employees.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Employee(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    department = db.Column(db.String(100), nullable=False)

    salary = db.Column(db.Float, nullable=False)


# Convert employee object into dictionary
def employee_to_dict(employee):

    return {
        "id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "department": employee.department,
        "salary": employee.salary
    }


#add emp

@app.route("/employees", methods=["POST"])
def add_employee():

    data = request.get_json()

    # Check JSON data
    if not data:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    # Check required fields
    if not all(
        key in data
        for key in ["name", "email", "department", "salary"]
    ):
        return jsonify({
            "error": "Name, email, department and salary are required"
        }), 400

    # Check salary
    try:
        salary = float(data["salary"])
    except (ValueError, TypeError):
        return jsonify({
            "error": "Salary must be a number"
        }), 400

    if salary <= 0:
        return jsonify({
            "error": "Salary must be greater than zero"
        }), 400

    # Check duplicate email
    existing_employee = Employee.query.filter_by(
        email=data["email"]
    ).first()

    if existing_employee:
        return jsonify({
            "error": "Email already exists"
        }), 409

    # Create employee
    employee = Employee(
        name=data["name"],
        email=data["email"],
        department=data["department"],
        salary=salary
    )

    db.session.add(employee)
    db.session.commit()

    return jsonify({
        "message": "Employee added successfully",
        "employee": employee_to_dict(employee)
    }), 201


#  view emp

@app.route("/employees", methods=["GET"])
def get_employees():

    employees = Employee.query.all()

    result = []

    for employee in employees:
        result.append(employee_to_dict(employee))

    return jsonify(result), 200


#  UPDATE EMPLOYEE

@app.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):

    employee = Employee.query.get(employee_id)

    if not employee:
        return jsonify({
            "error": "Employee not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON data is required"
        }), 400

    # Update name
    if "name" in data:
        employee.name = data["name"]

    # Update email
    if "email" in data:

        # Check whether another employee has this email
        existing_employee = Employee.query.filter_by(
            email=data["email"]
        ).first()

        if existing_employee and existing_employee.id != employee.id:
            return jsonify({
                "error": "Email already exists"
            }), 409

        employee.email = data["email"]

    # Update department
    if "department" in data:
        employee.department = data["department"]

    # Update salary
    if "salary" in data:

        try:
            salary = float(data["salary"])
        except (ValueError, TypeError):
            return jsonify({
                "error": "Salary must be a number"
            }), 400

        if salary <= 0:
            return jsonify({
                "error": "Salary must be greater than zero"
            }), 400

        employee.salary = salary

    db.session.commit()

    return jsonify({
        "message": "Employee updated successfully",
        "employee": employee_to_dict(employee)
    }), 200


#  DELETE EMPLOYEE

@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):

    employee = Employee.query.get(employee_id)

    if not employee:
        return jsonify({
            "error": "Employee not found"
        }), 404

    db.session.delete(employee)
    db.session.commit()

    return jsonify({
        "message": "Employee deleted successfully"
    }), 200


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)


    {
    "name": "Shiva Kumar",
    "email": "shiva@gmail.com",
    "department": "IT",
    "salary": 50000
}
    {
    "name": "Rahul Sharma",
    "email": "rahul@gmail.com",
    "department": "HR",
    "salary": 45000
}
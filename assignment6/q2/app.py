
from flask import Flask, request, jsonify
from pymongo.errors import DuplicateKeyError
from database import employees_collection

app = Flask(__name__)


def validate_employee(data, is_update=False):
    errors = []

    if not is_update or "name" in data:
        if not isinstance(data.get("name"), str) or not data.get("name").strip():
            errors.append("Employee name cannot be empty.")

    if not is_update or "department" in data:
        if not isinstance(data.get("department"), str) or not data.get("department").strip():
            errors.append("Department cannot be empty.")

    if not is_update or "salary" in data:
        salary = data.get("salary")

        if isinstance(salary, bool) or not isinstance(salary, (int, float)):
            errors.append("Salary must be a number.")
        elif salary <= 0:
            errors.append("Salary must be greater than 0.")

    if not is_update or "status" in data:
        status = data.get("status")

        if status not in ["Active", "Inactive"]:
            errors.append("Status must be Active or Inactive.")

    return errors


@app.route("/employees", methods=["POST"])
def add_employee():

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Valid JSON request body is required."
        }), 400

    required_fields = [
        "employee_id",
        "name",
        "department",
        "salary",
        "status"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields.",
            "fields": missing_fields
        }), 400

    employee_id = data.get("employee_id")

    if not isinstance(employee_id, str) or not employee_id.strip():
        return jsonify({
            "error": "Employee ID cannot be empty."
        }), 400

    errors = validate_employee(data)

    if errors:
        return jsonify({
            "errors": errors
        }), 400

    employee = {
        "employee_id": employee_id.strip(),
        "name": data["name"].strip(),
        "department": data["department"].strip(),
        "salary": data["salary"],
        "status": data["status"]
    }

    try:
        employees_collection.insert_one(employee)

    except DuplicateKeyError:
        return jsonify({
            "error": "Employee ID already exists."
        }), 409

    return jsonify({
        "message": "Employee added successfully.",
        "employee": employee
    }), 201


@app.route("/employees", methods=["GET"])
def get_all_employees():

    employees = list(
        employees_collection.find({}, {"_id": 0})
    )

    return jsonify({
        "count": len(employees),
        "employees": employees
    }), 200


@app.route("/employees/<employee_id>", methods=["GET"])
def get_employee(employee_id):

    employee_id = employee_id.strip()

    if not employee_id:
        return jsonify({
            "error": "Employee ID cannot be empty."
        }), 400

    employee = employees_collection.find_one(
        {"employee_id": employee_id},
        {"_id": 0}
    )

    if not employee:
        return jsonify({
            "error": "Employee not found."
        }), 404

    return jsonify({
        "employee": employee
    }), 200


@app.route("/employees/<employee_id>", methods=["PUT"])
def update_employee(employee_id):

    employee_id = employee_id.strip()

    if not employee_id:
        return jsonify({
            "error": "Employee ID cannot be empty."
        }), 400

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Valid JSON request body is required."
        }), 400

    if "employee_id" in data:
        return jsonify({
            "error": "Employee ID cannot be changed."
        }), 400

    employee = employees_collection.find_one({
        "employee_id": employee_id
    })

    if not employee:
        return jsonify({
            "error": "Employee not found."
        }), 404

    errors = validate_employee(data, is_update=True)

    if errors:
        return jsonify({
            "errors": errors
        }), 400

    allowed_fields = [
        "name",
        "department",
        "salary",
        "status"
    ]

    update_data = {
        field: data[field].strip()
        if isinstance(data[field], str)
        else data[field]
        for field in allowed_fields
        if field in data
    }

    if not update_data:
        return jsonify({
            "error": "At least one valid field is required."
        }), 400

    employees_collection.update_one(
        {"employee_id": employee_id},
        {"$set": update_data}
    )

    updated_employee = employees_collection.find_one(
        {"employee_id": employee_id},
        {"_id": 0}
    )

    return jsonify({
        "message": "Employee updated successfully.",
        "employee": updated_employee
    }), 200


@app.route("/employees/<employee_id>", methods=["DELETE"])
def delete_employee(employee_id):

    employee_id = employee_id.strip()

    if not employee_id:
        return jsonify({
            "error": "Employee ID cannot be empty."
        }), 400

    result = employees_collection.delete_one({
        "employee_id": employee_id
    })

    if result.deleted_count == 0:
        return jsonify({
            "error": "Employee not found."
        }), 404

    return jsonify({
        "message": "Employee deleted successfully."
    }), 200


@app.route("/employees/department/<department>", methods=["GET"])
def employees_by_department(department):

    department = department.strip()

    if not department:
        return jsonify({
            "error": "Department cannot be empty."
        }), 400

    employees = list(
        employees_collection.find(
            {
                "department": {
                    "$regex": f"^{department}$",
                    "$options": "i"
                }
            },
            {"_id": 0}
        )
    )

    if not employees:
        return jsonify({
            "message": "No employees found in this department."
        }), 404

    return jsonify({
        "department": department,
        "count": len(employees),
        "employees": employees
    }), 200


@app.route("/employees/salary", methods=["GET"])
def employees_by_salary():

    salary = request.args.get("greater_than")

    if salary is None or not salary.strip():
        return jsonify({
            "error": "Salary amount is required."
        }), 400

    try:
        salary = float(salary)
    except ValueError:
        return jsonify({
            "error": "Salary must be a valid number."
        }), 400

    if salary < 0:
        return jsonify({
            "error": "Salary amount cannot be negative."
        }), 400

    employees = list(
        employees_collection.find(
            {
                "salary": {
                    "$gt": salary
                }
            },
            {"_id": 0}
        )
    )

    if not employees:
        return jsonify({
            "message": "No employees found with salary greater than the given amount."
        }), 404

    return jsonify({
        "salary_greater_than": salary,
        "count": len(employees),
        "employees": employees
    }), 200


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Employee API is running."
    }), 200


@app.errorhandler(404)
def page_not_found(error):

    return jsonify({
        "error": "Endpoint not found."
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):

    return jsonify({
        "error": "HTTP method not allowed."
    }), 405


@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({
        "error": "Internal server error."
    }), 500


if __name__ == "__main__":
    app.run(debug=True)

{
    "employee_id": "E101",
    "name": "Rahul",
    "department": "IT",
    "salary": 60000,
    "status": "Active"
}

{
    "salary": 90000,
    "status": "Inactive"
}
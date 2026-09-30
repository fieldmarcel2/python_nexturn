
from flask import Flask, request, jsonify
from datetime import datetime
from pymongo.errors import DuplicateKeyError

from database import employees, leaves

app = Flask(__name__)


def get_date(date_string):
    try:
        return datetime.strptime(
            date_string,
            "%Y-%m-%d"
        ).date()
    except (ValueError, TypeError):
        return None


def calculate_days(start_date, end_date):
    return (end_date - start_date).days + 1


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Employee Leave API is running."
    })


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
        "available_leave_days"
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
    name = data.get("name")
    department = data.get("department")
    leave_days = data.get("available_leave_days")

    if not isinstance(employee_id, str) or not employee_id.strip():
        return jsonify({
            "error": "Employee ID cannot be empty."
        }), 400

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            "error": "Employee name cannot be empty."
        }), 400

    if not isinstance(department, str) or not department.strip():
        return jsonify({
            "error": "Department cannot be empty."
        }), 400

    if isinstance(leave_days, bool) or not isinstance(leave_days, int):
        return jsonify({
            "error": "Available leave days must be an integer."
        }), 400

    if leave_days < 0:
        return jsonify({
            "error": "Available leave days cannot be negative."
        }), 400

    employee = {
        "employee_id": employee_id.strip(),
        "name": name.strip(),
        "department": department.strip(),
        "available_leave_days": leave_days
    }

    try:
        employees.insert_one(employee)

    except DuplicateKeyError:
        return jsonify({
            "error": "Employee ID already exists."
        }), 409

    return jsonify({
        "message": "Employee added successfully.",
        "employee": employee
    }), 201


@app.route("/leaves", methods=["POST"])
def apply_leave():

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Valid JSON request body is required."
        }), 400

    required_fields = [
        "leave_id",
        "employee_id",
        "start_date",
        "end_date",
        "reason"
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

    leave_id = data.get("leave_id")
    employee_id = data.get("employee_id")
    start_date = get_date(data.get("start_date"))
    end_date = get_date(data.get("end_date"))
    reason = data.get("reason")

    if not isinstance(leave_id, str) or not leave_id.strip():
        return jsonify({
            "error": "Leave ID cannot be empty."
        }), 400

    if not isinstance(employee_id, str) or not employee_id.strip():
        return jsonify({
            "error": "Employee ID cannot be empty."
        }), 400

    if not start_date or not end_date:
        return jsonify({
            "error": "Date must be in YYYY-MM-DD format."
        }), 400

    if start_date > end_date:
        return jsonify({
            "error": "Start date cannot be after end date."
        }), 400

    if not isinstance(reason, str) or not reason.strip():
        return jsonify({
            "error": "Reason cannot be empty."
        }), 400

    employee = employees.find_one({
        "employee_id": employee_id.strip()
    })

    if not employee:
        return jsonify({
            "error": "Employee not found."
        }), 404

    days = calculate_days(start_date, end_date)

    if days > employee["available_leave_days"]:
        return jsonify({
            "error": "Requested leave exceeds available leave days.",
            "available_days": employee["available_leave_days"],
            "requested_days": days
        }), 400

    leave = {
        "leave_id": leave_id.strip(),
        "employee_id": employee_id.strip(),
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "reason": reason.strip(),
        "status": "Pending",
        "days": days
    }

    try:
        leaves.insert_one(leave)

    except DuplicateKeyError:
        return jsonify({
            "error": "Leave ID already exists."
        }), 409

    return jsonify({
        "message": "Leave applied successfully.",
        "leave": leave
    }), 201


@app.route("/leaves", methods=["GET"])
def get_all_leaves():

    all_leaves = list(
        leaves.find({}, {"_id": 0})
    )

    return jsonify({
        "count": len(all_leaves),
        "leaves": all_leaves
    }), 200


@app.route("/employees/<employee_id>/leaves", methods=["GET"])
def get_employee_leaves(employee_id):

    if not employee_id.strip():
        return jsonify({
            "error": "Employee ID cannot be empty."
        }), 400

    employee = employees.find_one({
        "employee_id": employee_id
    })

    if not employee:
        return jsonify({
            "error": "Employee not found."
        }), 404

    employee_leaves = list(
        leaves.find(
            {"employee_id": employee_id},
            {"_id": 0}
        )
    )

    return jsonify({
        "employee_id": employee_id,
        "count": len(employee_leaves),
        "leaves": employee_leaves
    }), 200


@app.route("/leaves/<leave_id>/approve", methods=["PUT"])
def approve_leave(leave_id):

    leave = leaves.find_one({
        "leave_id": leave_id
    })

    if not leave:
        return jsonify({
            "error": "Leave not found."
        }), 404

    if leave["status"] != "Pending":
        return jsonify({
            "error": "Only Pending leave can be approved."
        }), 400

    employee = employees.find_one({
        "employee_id": leave["employee_id"]
    })

    if not employee:
        return jsonify({
            "error": "Employee not found."
        }), 404

    if employee["available_leave_days"] < leave["days"]:
        return jsonify({
            "error": "Employee does not have enough leave balance."
        }), 400

    employees.update_one(
        {"employee_id": leave["employee_id"]},
        {
            "$inc": {
                "available_leave_days": -leave["days"]
            }
        }
    )

    leaves.update_one(
        {"leave_id": leave_id},
        {
            "$set": {
                "status": "Approved"
            }
        }
    )

    return jsonify({
        "message": "Leave approved successfully."
    }), 200


@app.route("/leaves/<leave_id>/reject", methods=["PUT"])
def reject_leave(leave_id):

    leave = leaves.find_one({
        "leave_id": leave_id
    })

    if not leave:
        return jsonify({
            "error": "Leave not found."
        }), 404

    if leave["status"] != "Pending":
        return jsonify({
            "error": "Only Pending leave can be rejected."
        }), 400

    leaves.update_one(
        {"leave_id": leave_id},
        {
            "$set": {
                "status": "Rejected"
            }
        }
    )

    return jsonify({
        "message": "Leave rejected successfully."
    }), 200


@app.route("/leaves/<leave_id>/cancel", methods=["PUT"])
def cancel_leave(leave_id):

    leave = leaves.find_one({
        "leave_id": leave_id
    })

    if not leave:
        return jsonify({
            "error": "Leave not found."
        }), 404

    if leave["status"] != "Pending":
        return jsonify({
            "error": "Only Pending leave can be cancelled."
        }), 400

    leaves.update_one(
        {"leave_id": leave_id},
        {
            "$set": {
                "status": "Cancelled"
            }
        }
    )

    return jsonify({
        "message": "Leave cancelled successfully."
    }), 200


@app.route("/employees/<employee_id>/leave-balance", methods=["GET"])
def get_leave_balance(employee_id):

    employee = employees.find_one(
        {"employee_id": employee_id},
        {"_id": 0}
    )

    if not employee:
        return jsonify({
            "error": "Employee not found."
        }), 404

    return jsonify({
        "employee_id": employee_id,
        "available_leave_days": employee["available_leave_days"]
    }), 200


@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "Endpoint not found."
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):

    return jsonify({
        "error": "HTTP method not allowed."
    }), 405


if __name__ == "__main__":
    app.run(debug=True)

{
    "leave_id": "L101",
    "employee_id": "E101",
    "start_date": "2026-10-05",
    "end_date": "2026-10-07",
    "reason": "Family function",
    "status": "Pending",
    "days": 3
}
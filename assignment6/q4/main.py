
from datetime import date
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from pymongo.errors import DuplicateKeyError

from database import tasks_collection


app = FastAPI(
    title="Task Management API",
    version="1.0.0"
)


class Task(BaseModel):
    task_id: str = Field(min_length=1)
    task_name: str = Field(min_length=1)
    employee_name: str = Field(min_length=1)
    priority: str
    status: str
    due_date: date


class TaskUpdate(BaseModel):
    task_name: str | None = Field(default=None, min_length=1)
    employee_name: str | None = Field(default=None, min_length=1)
    priority: str | None = None
    status: str | None = None
    due_date: date | None = None


@app.get("/")
def home():
    return {
        "message": "Task Management API is running."
    }


@app.post("/tasks", status_code=201)
def add_task(task: Task):

    if task.priority not in ["Low", "Medium", "High"]:
        raise HTTPException(
            status_code=400,
            detail="Priority must be Low, Medium or High."
        )

    if task.status not in ["Pending", "In Progress", "Completed"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Pending, In Progress or Completed."
        )

    data = task.model_dump()

    data["due_date"] = task.due_date.isoformat()

    try:
        tasks_collection.insert_one(data)

    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="Task ID already exists."
        )

    return {
        "message": "Task added successfully.",
        "task": data
    }


@app.get("/tasks")
def get_all_tasks():

    tasks = list(
        tasks_collection.find(
            {},
            {"_id": 0}
        )
    )

    return {
        "count": len(tasks),
        "tasks": tasks
    }


@app.get("/tasks/{task_id}")
def get_task(task_id: str):

    task = tasks_collection.find_one(
        {"task_id": task_id},
        {"_id": 0}
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found."
        )

    return {
        "task": task
    }


@app.put("/tasks/{task_id}")
def update_task(
    task_id: str,
    task: TaskUpdate
):

    existing_task = tasks_collection.find_one({
        "task_id": task_id
    })

    if not existing_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found."
        )

    update_data = {
        key: value
        for key, value in task.model_dump().items()
        if value is not None
    }

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="At least one field is required for update."
        )

    if "priority" in update_data:
        if update_data["priority"] not in [
            "Low",
            "Medium",
            "High"
        ]:
            raise HTTPException(
                status_code=400,
                detail="Priority must be Low, Medium or High."
            )

    if "status" in update_data:
        if update_data["status"] not in [
            "Pending",
            "In Progress",
            "Completed"
        ]:
            raise HTTPException(
                status_code=400,
                detail="Status must be Pending, In Progress or Completed."
            )

    if (
        existing_task["status"] == "Completed"
        and update_data.get("status") == "Pending"
    ):
        raise HTTPException(
            status_code=400,
            detail="Completed task cannot be changed back to Pending."
        )

    if "due_date" in update_data:
        update_data["due_date"] = update_data["due_date"].isoformat()

    tasks_collection.update_one(
        {"task_id": task_id},
        {"$set": update_data}
    )

    updated_task = tasks_collection.find_one(
        {"task_id": task_id},
        {"_id": 0}
    )

    return {
        "message": "Task updated successfully.",
        "task": updated_task
    }


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):

    result = tasks_collection.delete_one({
        "task_id": task_id
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Task not found."
        )

    return {
        "message": "Task deleted successfully."
    }


@app.get("/tasks/employee/{employee_name}")
def tasks_by_employee(employee_name: str):

    employee_name = employee_name.strip()

    if not employee_name:
        raise HTTPException(
            status_code=400,
            detail="Employee name cannot be empty."
        )

    tasks = list(
        tasks_collection.find(
            {
                "employee_name": {
                    "$regex": f"^{employee_name}$",
                    "$options": "i"
                }
            },
            {"_id": 0}
        )
    )

    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="No tasks found for this employee."
        )

    return {
        "employee": employee_name,
        "count": len(tasks),
        "tasks": tasks
    }


@app.get("/tasks/status/{status}")
def tasks_by_status(status: str):

    valid_statuses = [
        "Pending",
        "In Progress",
        "Completed"
    ]

    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail="Status must be Pending, In Progress or Completed."
        )

    tasks = list(
        tasks_collection.find(
            {
                "status": status
            },
            {"_id": 0}
        )
    )

    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="No tasks found with this status."
        )

    return {
        "status": status,
        "count": len(tasks),
        "tasks": tasks
    }


@app.get("/tasks/high-priority")
def high_priority_tasks():

    tasks = list(
        tasks_collection.find(
            {
                "priority": "High"
            },
            {"_id": 0}
        )
    )

    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="No high-priority tasks found."
        )

    return {
        "count": len(tasks),
        "tasks": tasks
    }


@app.get("/tasks/overdue")
def overdue_tasks():

    today = date.today().isoformat()

    tasks = list(
        tasks_collection.find(
            {
                "due_date": {
                    "$lt": today
                },
                "status": {
                    "$ne": "Completed"
                }
            },
            {"_id": 0}
        )
    )

    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="No overdue tasks found."
        )

    return {
        "count": len(tasks),
        "tasks": tasks
    }

{
    "task_id": "T101",
    "task_name": "Complete API",
    "employee_name": "Rahul",
    "priority": "High",
    "status": "In Progress",
    "due_date": "2026-10-05"
}

{
    "priority": "High",
    "status": "Completed"
}
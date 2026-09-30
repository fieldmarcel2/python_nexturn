from flask import Flask, request, jsonify
import asyncio
import threading
import uuid


app = Flask(__name__)

class Task:
    def __init__(self, name, processing_time):
        self.id = str(uuid.uuid4())
        self.name = name
        self.processing_time = processing_time
        self.status = "pending"


    def to_dict(self):
        return {
            "task_id": self.id,
            "task_name": self.name,
            "processing_time": self.processing_time,
            "status": self.status
        }



# Task Manager

class TaskManager:

    def __init__(self):
        # task_id -> Task object
        self.tasks = {}

        self.loop = asyncio.new_event_loop()

        # Lock for shared data
        self.lock = asyncio.Lock()

        # Start event loop in background thread
        self.thread = threading.Thread(
            target=self._start_loop,
            daemon=True
        )
        self.thread.start()

    def _start_loop(self):
        """
        Runinng the asyncio event loop continuously
        in a background thread.
        """
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    # -----------------------------------------------------

    async def process_task(self, task):
        """
        Process one task asynchronously.
        """

        async with self.lock:
            task.status = "processing"

        print(
            f"Started: {task.name} "
            f"({task.processing_time}s)"
        )

        try:
            # Simulate time-consuming work
            await asyncio.sleep(task.processing_time)

            async with self.lock:
                task.status = "completed"

            print(f"Completed: {task.name}")

        except asyncio.CancelledError:

            async with self.lock:
                task.status = "cancelled"

            raise

        except Exception:

            async with self.lock:
                task.status = "failed"

    

    def add_tasks(self, tasks):
        """
        Add multiple tasks and start them concurrently.
        """

        for task in tasks:
            self.tasks[task.id] = task

            asyncio.run_coroutine_threadsafe(
                self.process_task(task),
                self.loop
            )


    def get_task(self, task_id):
        return self.tasks.get(task_id)

    

    def get_all_tasks(self):
        return list(
            map(
                lambda task: task.to_dict(),
                self.tasks.values()
            )
        )


# Create Task Manager

task_manager = TaskManager()


# Validation

def validate_task(data):
    """
    Validate a single task.
    Returns:
        (True, None) if valid
        (False, error_message) if invalid
    """

    if not isinstance(data, dict):
        return False, "Each task must be a JSON object."

    required_fields = {"name", "processing_time"}

    missing_fields = required_fields - data.keys()

    if missing_fields:
        return False, (
            f"Missing fields: {', '.join(missing_fields)}"
        )

    name = data["name"]
    processing_time = data["processing_time"]

    # Validate name
    if not isinstance(name, str):
        return False, "Task name must be a string."

    name = name.strip()

    if not name:
        return False, "Task name cannot be empty."

    # Validate processing time
    if isinstance(processing_time, bool):
        return False, "Processing time must be a number."

    if not isinstance(processing_time, (int, float)):
        return False, "Processing time must be a number."

    if processing_time < 0:
        return False, "Processing time cannot be negative."

    # Optional upper limit
    if processing_time > 3600:
        return False, "Processing time cannot exceed 3600 seconds."

    return True, None


# Routes
# 

@app.get("/")
def home():
    return jsonify({
        "message": "Asynchronous Task Processing API",
        "endpoints": {
            "POST /tasks": "Submit multiple tasks",
            "GET /tasks": "Get all tasks",
            "GET /tasks/<task_id>": "Get task status"
        }
    })


# Submit Multiple Tasks

@app.post("/tasks")
def create_tasks():

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Request body must contain valid JSON."
        }), 400

    # We expect:
    #
    # {
    #     "tasks": [
    #         {
    #             "name": "Task A",
    #             "processing_time": 5
    #         }
    #     ]
    # }

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object."
        }), 400

    tasks_data = data.get("tasks")

    if tasks_data is None:
        return jsonify({
            "error": "'tasks' field is required."
        }), 400

    if not isinstance(tasks_data, list):
        return jsonify({
            "error": "'tasks' must be a list."
        }), 400

    if not tasks_data:
        return jsonify({
            "error": "Task list cannot be empty."
        }), 400

    # Validate all tasks first

    errors = [
        {
            "index": index,
            "error": validate_task(task)[1]
        }
        for index, task in enumerate(tasks_data)
        if not validate_task(task)[0]
    ]

    if errors:
        return jsonify({
            "error": "Invalid task data.",
            "details": errors
        }), 400

    # Create Task objects using list comprehension
    tasks = [
        Task(
            name=task["name"].strip(),
            processing_time=task["processing_time"]
        )
        for task in tasks_data
    ]

    # Add and start processing
    task_manager.add_tasks(tasks)

    return jsonify({
        "message": "Tasks submitted successfully.",
        "tasks": [
            task.to_dict()
            for task in tasks
        ]
    }), 202


# Get All Tasks

@app.get("/tasks")
def get_all_tasks():

    return jsonify({
        "count": len(task_manager.tasks),
        "tasks": task_manager.get_all_tasks()
    })


# Get Individual Task


@app.get("/tasks/<task_id>")
def get_task_status(task_id):

    task = task_manager.get_task(task_id)

    if task is None:
        return jsonify({
            "error": "Task not found."
        }), 404

    return jsonify(task.to_dict())



if __name__ == "__main__":
    app.run(
        debug=False,
        threaded=True
    )
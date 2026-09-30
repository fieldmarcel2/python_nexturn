from flask import Flask, request, jsonify, render_template
import asyncio
import threading
import time
import uuid


app = Flask(__name__)



class Task:

    def __init__(self, task_id):
        self.task_id = task_id
        self.status = "Pending"
        self.result = None
        self.error = None


# Store all tasks
tasks = {}


# Long Running Task

async def process_task(task):

    try:

        task.status = "Running"

        # Simulate long-running work
        await asyncio.sleep(5)

        task.result = "Task completed successfully"
        task.status = "Completed"

    except Exception as e:

        task.status = "Failed"
        task.error = str(e)


# 
# Run Async Task
# 

def run_task(task):

    asyncio.run(process_task(task))


# 
# Home Page
# 

@app.route("/")
def home():

    return render_template("index.html")


# Submit Task
# 

@app.route("/tasks", methods=["POST"])
def create_task():

    task_id = str(uuid.uuid4())

    task = Task(task_id)

    tasks[task_id] = task

    # running  task in bg thread
    thread = threading.Thread(
        target=run_task,
        args=(task,)
    )

    thread.start()

    return jsonify({
        "message": "Task submitted successfully",
        "task_id": task_id,
        "status": task.status
    }), 202




@app.route("/tasks", methods=["GET"])
def get_tasks():

    # List comprehension
    result = [
        {
            "task_id": task.task_id,
            "status": task.status,
            "result": task.result,
            "error": task.error
        }
        for task in tasks.values()
    ]

    return jsonify(result), 200



@app.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):

    task = tasks.get(task_id)

    if not task:

        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify({
        "task_id": task.task_id,
        "status": task.status,
        "result": task.result,
        "error": task.error
    }), 200



if __name__ == "__main__":

    app.run(
        debug=True,
        threaded=True
    )
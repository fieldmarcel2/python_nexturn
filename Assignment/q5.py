from flask import Flask, request, jsonify, g
import time


app = Flask(__name__)


API_KEY = "abc123"
APP_VERSION = "1.0.0"

@app.before_request
def before_request():

    g.start_time = time.time()

    # Get API key from request header
    api_key = request.headers.get("X-API-KEY")

    # Check API key
    if api_key != API_KEY:
        return jsonify({
            "error": "Invalid or missing API key"
        }), 401

@app.after_request
def after_request(response):

    # Calculate response time
    end_time = time.time()

    response_time = (end_time - g.start_time) * 1000

    # Add information to response headers
    response.headers["X-App-Version"] = APP_VERSION
    response.headers["X-Response-Time"] = f"{response_time:.2f} ms"

    return response

# 3. CUSTOM MIDDLEWARE

class RequestLoggingMiddleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        method = environ.get("REQUEST_METHOD")

        # Get request URL
        path = environ.get("PATH_INFO")

        start_time = time.time()

        response = self.app(environ, start_response)

        end_time = time.time()
        response_time = (end_time - start_time) * 1000

        print(
            f"Method: {method} | "
            f"URL: {path} | "
            f"Time: {response_time:.2f} ms"
        )

        return response


# Attach custom middleware to Flask
app.wsgi_app = RequestLoggingMiddleware(app.wsgi_app)

@app.route("/")
def home():

    return jsonify({
        "message": "Welcome to Flask Middleware API"})


@app.route("/users")
def users():

    return jsonify({
        "users": ["Shiva", "Rahul", "Amit"]
    })
if __name__ == "__main__":
    app.run(debug=True)


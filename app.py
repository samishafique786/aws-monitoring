from flask import Flask
from prometheus_client import Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# Create a histogram metric to track request duration
REQUEST_TIME = Histogram(
    'hello_world_request_seconds',
    'Time spent serving hello world requests'
)

@app.route("/")
def hello():
    start = time.time()
    response = "hello world"
    REQUEST_TIME.observe(time.time() - start)
    return response

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

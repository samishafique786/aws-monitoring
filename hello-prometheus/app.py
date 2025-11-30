from flask import Flask, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# Prometheus metrics
REQUEST_LATENCY = Histogram(
    'hello_world_request_latency_seconds', 
    'Time spent processing hello world request'
)
REQUEST_COUNT = Counter(
    'hello_world_requests_total', 
    'Total number of hello world requests'
)

@app.route('/')
def hello_world():
    start_time = time.time()
    REQUEST_COUNT.inc()
    
    # Simulate processing (optional)
    response_text = "hello world version 2"
    
    elapsed = time.time() - start_time
    REQUEST_LATENCY.observe(elapsed)
    
    return response_text

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

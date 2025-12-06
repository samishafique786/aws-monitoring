from flask import Flask, Response, request, g
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
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

# New Standard Metrics
HTTP_REQUESTS_TOTAL = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'active_requests',
    'Number of active requests'
)

APP_INFO = Gauge(
    'app_info',
    'Application information',
    ['version']
)
APP_INFO.labels(version='1.0.0').set(1)

@app.before_request
def before_request():
    ACTIVE_REQUESTS.inc()
    g.start_time = time.time()

@app.after_request
def after_request(response):
    ACTIVE_REQUESTS.dec()
    if hasattr(g, 'start_time'):
        elapsed = time.time() - g.start_time
        # Use request.path as endpoint, but be careful with high cardinality if you have dynamic paths
        # For this simple app, request.path is fine.
        HTTP_REQUEST_DURATION_SECONDS.labels(method=request.method, endpoint=request.path).observe(elapsed)
        HTTP_REQUESTS_TOTAL.labels(method=request.method, endpoint=request.path, status=response.status_code).inc()
    return response

@app.route('/')
def hello_world():
    start_time = time.time()
    REQUEST_COUNT.inc()
    
    # Simulate processing (optional)
    response_text = "hello world"
    
    elapsed = time.time() - start_time
    REQUEST_LATENCY.observe(elapsed)
    
    return response_text

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

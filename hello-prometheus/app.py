from flask import Flask, Response, request, g
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

SERVER_START_TIME = time.time()


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

HTTP_REQUEST_SIZE_BYTES = Histogram(
    'http_request_size_bytes',
    'HTTP request content length in bytes',
    ['method', 'endpoint']
)

HTTP_RESPONSE_SIZE_BYTES = Histogram(
    'http_response_size_bytes',
    'HTTP response content length in bytes',
    ['method', 'endpoint']
)

SERVER_UPTIME_SECONDS = Gauge(
    'server_uptime_seconds',
    'Server uptime in seconds'
)

@app.before_request
def before_request():
    ACTIVE_REQUESTS.inc()
    g.start_time = time.time()
    
    # Record request size
    length = request.content_length or 0
    HTTP_REQUEST_SIZE_BYTES.labels(method=request.method, endpoint=request.path).observe(length)

@app.after_request
def after_request(response):
    ACTIVE_REQUESTS.dec()
    if hasattr(g, 'start_time'):
        elapsed = time.time() - g.start_time
        HTTP_REQUEST_DURATION_SECONDS.labels(method=request.method, endpoint=request.path).observe(elapsed)
        HTTP_REQUESTS_TOTAL.labels(method=request.method, endpoint=request.path, status=response.status_code).inc()
    
    # Record response size
    length = response.content_length or 0
    # If content_length is not set, try to get it from data
    if length == 0 and response.data:
        length = len(response.data)
        
    HTTP_RESPONSE_SIZE_BYTES.labels(method=request.method, endpoint=request.path).observe(length)
    
    return response

@app.route('/')
def hello_world():
    start_time = time.time()
    REQUEST_COUNT.inc()
    
    response_text = "hello world"
    
    elapsed = time.time() - start_time
    REQUEST_LATENCY.observe(elapsed)
    
    return response_text

@app.route('/metrics')
def metrics():
    SERVER_UPTIME_SECONDS.set(time.time() - SERVER_START_TIME)
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

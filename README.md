# GitLab to EKS: CI/CD Workflow for NordHealth

This is a project repository that shows the detailed process of creating a End-to-End CI/CD workflow.

The workflow starts when a developer pushed code to a version control system, in this case GitLab, and then, the code is then built into a container image to be pushed to a container registry. 

This project uses GitLab as the version control system, and the container registry is also the GitLab container registry.

Once the container image and built and pushed, the image is then pulled into an EKS Kubernetes cluster, and then deployed to a pod. 

All the process is automated using GitLab CI/CD pipelines. 


## 1. Hello World Flask App with Prometheus Metrics

A simple Flask web application that prints "hello world sami" and exposes Prometheus metrics to monitor request counts and latency.

---

## Features

- **Endpoint `/`**: Returns `"hello world sami"`.
- **Prometheus Metrics `/metrics`**:
  - `hello_world_requests_total` – Total number of requests to `/`.
  - `hello_world_request_latency_seconds` – Histogram measuring request processing time. (later visualized by Grafana)

  
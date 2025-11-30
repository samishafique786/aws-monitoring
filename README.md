# GitLab to EKS: CI/CD Workflow for NordHealth

This is a project repository that shows the detailed process of creating a End-to-End CI/CD workflow.

The workflow starts when a developer pushed code to a version control system, in this case GitLab, and then, the code is then built into a container image to be pushed to a container registry. 

This project uses GitLab as the version control system, and the container registry is also the GitLab container registry.

Once the container image and built and pushed, the image is then pulled into an EKS Kubernetes cluster, and then deployed to a pod. 

All the process is automated using GitLab CI/CD pipelines. 

## Architecture Diagram

https://gitlab.com/samishafique786/aws-ci-cd/-/blob/main/nordhealth1.0.jpg?ref_type=heads

## Project Structure

- **`eks-terraform/`**: Terraform configuration to provision the AWS EKS cluster.
- **`monitoring-terraform/`**: Terraform configuration to provision the EC2 instance (including cloud-init file for installing prometheus and Grafana)
- **`hello-prometheus/`**: Source code for the Python Flask application (Dockerfile, .py, and tests)
- **`.gitlab-ci.yml`**: CI/CD pipeline definition for building testing and deploying the application to EKS

---


### 1. Hello World Flask App with Prometheus Metrics

A simple Flask web application that prints "hello world sami" and exposes Prometheus metrics to monitor request counts and latency.

---

## Features

- **Endpoint `/`**: Returns `"hello world sami"`.
- **Prometheus Metrics `/metrics`**:
  - `hello_world_requests_total` – Total number of requests to `/`.
  - `hello_world_request_latency_seconds` – Histogram measuring request processing time. (later visualized by Grafana)

## Cloud Infrastructure on AWS Managed by Terraform

### 1. EKS Cluster (`/eks-terraform`)
Provisions a Kubernetes cluster on AWS using the `terraform-aws-modules/eks/aws` module.
- **Resources**: VPC, Subnets, EKS Cluster, Managed Node Groups, also an Elastic IP that is used later by the Python app to expose the app on a static IP.
- **Region**: `eu-north-1`.

### 2. Monitoring Server (`monitoring-terraform`)
Provisions a standalone EC2 instance (`t3.small`) to monitor the infrastructure.
- **Components Installed via Cloud-Init**:
    - **Prometheus**: Scrapes metrics from itself and Node Exporter.
    - **Grafana**: Visualization dashboard.
    - **Node Exporter**: Exposes hardware and OS metrics.
- **Access**:
    - **Prometheus**: `http://<Public-IP>:9090`
    - **Grafana**: `http://<Public-IP>:3000` default login was 'admin' for both username and pass. 
    - **Node Exporter**: Port 9100 (Internal only).

---

## CI/CD Pipeline (`.gitlab-ci.yml`)

The pipeline automates the software delivery lifecycle:

1. **Test**: Runs unit tests (`test_app.py`).
2.  **Build**: Creates a Docker image from `hello-prometheus/`.
3.  **Push**: Pushes the Docker image to the GitLab Container Registry. (it is public for now, but if it was private, I would have created an Access token in GitLab with the registry read permission, and stored it in my EKS Cluster as a "Secret" for my namespace. I have done that in previous projects)
4.  **Deploy**: Deploys the application to the EKS cluster using `kubectl`. 


## My Workflow (In what sequence I built everything)

### Prerequisites
- Created AWS Account & Credentials configured (new IAM user with Admin permission, and then created secret access key)
- Terraform installed. (wrote code for EKS first, then the server.)
- GitLab Account. (already had one)

### Step 1: Deploy Infrastructure
```bash

# Deploy EKS Cluster
cd ../eks-terraform
terraform init
terraform apply
```

```bash
# Deploy Monitoring Server
cd monitoring-terraform
terraform init
terraform apply
```

### Step 2: Configure Kubernetes Access
Update your local `kubeconfig` to interact with the cluster: (Assuming that you have aws cli installed and configured already with "aws configure")
```bash
aws eks update-kubeconfig --region eu-north-1 --name <cluster-name>
kubectl get nodes
```
It should authenticate with the cluster and then, should give you worker nodes. 



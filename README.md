# GitLab to EKS: CI/CD Workflow for NordHealth

This is a project repository that shows the detailed process of creating a End-to-End CI/CD workflow.

The workflow starts when a developer pushed code to a version control system, in this case GitLab, and then, the code is then built into a container image to be pushed to a container registry. 

This project uses GitLab as the version control system, and the container registry is also the GitLab container registry.

Once the container image and built and pushed, the image is then pulled into an EKS Kubernetes cluster, and then deployed to a pod. 

All the process is automated using GitLab CI/CD pipelines. 

## The Flast Application, Exlplained

The application is written in python using the web framework Flask. 

It has two routes. 

1. "/" takes you to the "hello world" output.

2. The other route "/metrics" takes you to an Endpoint that gives prometheus metrices, inlcluding the metric that shows how much time was taken to serve the request on the first route. 


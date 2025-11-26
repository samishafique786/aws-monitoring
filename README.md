This is a project repository that shows the detailed process of creating a End-to-End CI/CD workflow.

The workflow starts when a developer pushed code to a version control system, in this case GitLab, and then, the code is then built into a container image to be pushed to a container registry. 

This project uses GitLab as the version control system, and the container registry is also the GitLab container registry.

Once the container image and built and pushed, the image is then pulled into an EKS Kubernetes cluster, and then deployed to a pod. 

All the process is automated using GitLab CI/CD pipelines. 
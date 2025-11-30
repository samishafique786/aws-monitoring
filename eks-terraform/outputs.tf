# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "cluster_security_group_id" {
  description = "Security group ids attached to the cluster control plane"
  value       = module.eks.cluster_security_group_id
}

output "region" {
  description = "AWS region"
  value       = var.region
}

output "cluster_name" {
  description = "Kubernetes Cluster Name"
  value       = module.eks.cluster_name
}

output "load_balancer_ip" {
  description = "Public IP of the load balancer"
  value       = aws_eip.nord_app_ip.public_ip
}

output "load_balancer_allocation_id" {
  description = "Allocation ID to be used in Kubernetes Service annotations"
  value       = aws_eip.nord_app_ip.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_eip.lb.public_ip
}

output "ssh_command" {
  description = "Command to SSH into the instance"
  value       = "ssh -i /Users/sami/.ssh/id_rsa ubuntu@${aws_eip.lb.public_ip}"
}



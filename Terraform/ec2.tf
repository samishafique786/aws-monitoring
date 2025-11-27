resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.small"
  key_name      = aws_key_pair.deployer.key_name

  vpc_security_group_ids = [aws_security_group.allow_ssh_prometheus.id]

  user_data = templatefile("cloud-init.yaml", {
    prometheus_config = file("prometheus.yml")
  })

  tags = {
    Name = "Prometheus-Instance"
  }
}

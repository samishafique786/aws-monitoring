resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = file("/Users/sami/.ssh/id_rsa.pub")
}

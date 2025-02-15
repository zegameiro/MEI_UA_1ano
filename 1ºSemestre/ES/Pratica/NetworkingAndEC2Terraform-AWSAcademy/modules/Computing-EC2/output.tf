# EC2 Security Group
output "ec2_security_group" {
  value = {
    id          = aws_security_group.ec2_security_group.id
    name        = aws_security_group.ec2_security_group.name
    description = aws_security_group.ec2_security_group.description
    ingress     = aws_security_group.ec2_security_group.ingress
    egress      = aws_security_group.ec2_security_group.egress
  }
  description = "Details of the EC2 Security Group"
}

# EC2 Public Instance
output "ec2_public_instance" {
  value = {
    id              = aws_instance.public_vm.id
    name            = aws_instance.public_vm.tags["Name"]
    key_name        = aws_instance.public_vm.key_name
    private_ip      = aws_instance.public_vm.private_ip
    public_ip       = aws_instance.public_vm.public_ip
    security_groups = aws_instance.public_vm.vpc_security_group_ids
    user_data       = aws_instance.public_vm.user_data

  }
  description = "Details of the EC2 Public Instance"
}

# EC2 Private Instance
output "ec2_private_instance" {
  value = {
    id              = aws_instance.private_vm.id
    name            = aws_instance.private_vm.tags["Name"]
    key_name        = aws_instance.private_vm.key_name
    private_ip      = aws_instance.private_vm.private_ip
    public_ip       = aws_instance.private_vm.public_ip
    security_groups = aws_instance.private_vm.vpc_security_group_ids
    user_data       = aws_instance.private_vm.user_data

  }
  description = "Details of the EC2 Private Instance"
}

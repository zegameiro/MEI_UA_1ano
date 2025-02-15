module "Networking" {
  source                   = "./modules/Networking"
  aws_region               = var.aws_region
  aws_az                   = var.aws_az
  vpc_name                 = var.vpc_name
  vpc_cidr                 = var.vpc_cidr
  private_subnet_name      = var.private_subnet_name
  private_subnet_cidr      = var.private_subnet_cidr
  public_subnet_name       = var.public_subnet_name
  public_subnet_cidr       = var.public_subnet_cidr
  ec2_endpoint_name        = var.ec2_endpoint_name
  internet_gateway_name    = var.internet_gateway_name
  nat_gateway_name         = var.nat_gateway_name
  public_route_table_name  = var.public_route_table_name
  private_route_table_name = var.private_route_table_name
  environment              = var.environment
}

module "Computing-EC2" {
  source                  = "./modules/Computing-EC2"
  depends_on              = [module.Networking]
  vpc_id                  = module.Networking.vpc_info.id
  public_subnet_id        = module.Networking.public_subnet_info.id
  private_subnet_id       = module.Networking.private_subnet_info.id
  ec2_security_group_name = var.ec2_security_group_name
  ssh_key_pub_location    = var.ssh_key_pub_location
  ssh_key_ec2_name        = var.ssh_key_ec2_name
  public_vm_name          = var.public_vm_name
  private_vm_name         = var.private_vm_name
  environment             = var.environment

}

################################
#           Outputs            #
################################

# VPC
output "vpc_info" {
  value = module.Networking.vpc_info
}

# Subnets
output "public_subnet_info" {
  value = module.Networking.public_subnet_info
}
output "private_subnet_info" {
  value = module.Networking.private_subnet_info
}

# Route Tables
output "public_route_table_info" {
  value = module.Networking.public_route_table_info
}
output "private_route_table_info" {
  value = module.Networking.private_route_table_info
}

# Internet Gateway
output "internet_gw_info" {
  value = module.Networking.internet_gw_info
}

# NAT Gateway
output "nat_gw_info" {
  value = module.Networking.nat_gw_info
}

# EC2 Security Group
output "ec2_security_group" {
  value = module.Computing-EC2.ec2_security_group
}

# EC2 Public Instance
output "ec2_public_instance" {
  value = module.Computing-EC2.ec2_public_instance
}

# EC2 Private Instance
output "ec2_private_instance" {
  value = module.Computing-EC2.ec2_private_instance
}

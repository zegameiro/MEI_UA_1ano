output "vpc_id" {
  value = aws_vpc.vpc.id
}

output "public_subnet_id" {
  value = aws_subnet.public_subnet.id
}

output "private_subnet_id" {
  value = aws_subnet.private_subnet.id
}

output "public_subnet_cidr_block" {
  value = aws_subnet.public_subnet.cidr_block
}

output "private_subnet_cidr_block" {
  value = aws_subnet.private_subnet.cidr_block
}

output "default_sg_id" {
  value = data.aws_security_group.default_sg.id
}

output "public_route_table" {
  value = aws_route_table.public.id
}

output "private_route_table" {
  value = aws_route_table.private.id
}

# For information showcasing

# VPC
output "vpc_info" {
  value = {
    id                   = aws_vpc.vpc.id
    name                 = aws_vpc.vpc.tags["Name"]
    enable_dns_hostnames = aws_vpc.vpc.enable_dns_hostnames
    enable_dns_support   = aws_vpc.vpc.enable_dns_support
    cidr_block           = aws_vpc.vpc.cidr_block

  }
  description = "Details of the VPC"
}

# Subnets
output "public_subnet_info" {
  value = {
    id                      = aws_subnet.public_subnet.id
    name                    = aws_subnet.public_subnet.tags["Name"]
    tier                    = aws_subnet.public_subnet.tags["Tier"]
    availability_zone       = aws_subnet.public_subnet.availability_zone
    cidr_block              = aws_subnet.public_subnet.cidr_block
    map_public_ip_on_launch = aws_subnet.public_subnet.map_public_ip_on_launch

  }
  description = "Details of the Public Subnet"
}
output "private_subnet_info" {
  value = {
    id                      = aws_subnet.private_subnet.id
    name                    = aws_subnet.private_subnet.tags["Name"]
    tier                    = aws_subnet.private_subnet.tags["Tier"]
    availability_zone       = aws_subnet.private_subnet.availability_zone
    cidr_block              = aws_subnet.private_subnet.cidr_block
    map_public_ip_on_launch = aws_subnet.private_subnet.map_public_ip_on_launch

  }
  description = "Details of the Public Subnet"
}

# Route Tables
output "public_route_table_info" {
  value = {
    id   = aws_route_table.public.id
    name = aws_route_table.public.tags["Name"]
    routes = [
      aws_route.public_internet_gateway
    ]
    subnets = [
      aws_route_table_association.public.subnet_id,
    ]
  }
  description = "Details of the Public Route Table"
}
output "private_route_table_info" {
  value = {
    id   = aws_route_table.private.id
    name = aws_route_table.private.tags["Name"]
    routes = [
      aws_route.private_nat_gateway
    ]
    subnets = [
      aws_route_table_association.private.subnet_id,
    ]
  }
  description = "Details of the Private Route Table"
}

# Internet Gateway
output "internet_gw_info" {
  value = {
    id   = aws_internet_gateway.internet_gw.id
    name = aws_internet_gateway.internet_gw.tags["Name"]

  }
  description = "Details of the Internet Gateway"
}

# NAT Gateway
output "nat_gw_info" {
  value = {
    id         = aws_nat_gateway.nat_gateway.id
    name       = aws_nat_gateway.nat_gateway.tags["Name"]
    subnet     = aws_subnet.public_subnet
    private_ip = aws_eip.nat_eip.private_ip
    public_ip  = aws_eip.nat_eip.public_ip
  }
  description = "Details of the NAT Gateway"
}

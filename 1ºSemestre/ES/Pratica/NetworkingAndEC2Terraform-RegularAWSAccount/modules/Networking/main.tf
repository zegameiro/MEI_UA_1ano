# 1 - Create Your VPC
resource "aws_vpc" "vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = var.vpc_name
    Environment = var.environment
  }
}


# 2 - Create a Private Subnet
# Private Subnets
resource "aws_subnet" "private_subnet" {
  vpc_id                  = aws_vpc.vpc.id
  availability_zone       = var.aws_az
  cidr_block              = var.private_subnet_cidr
  map_public_ip_on_launch = false

  tags = {
    Name        = var.private_subnet_name
    Environment = var.environment
    Tier        = "Private"
  }
}

# 3 and 4 - Create a Public Network
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.vpc.id
  availability_zone       = var.aws_az
  cidr_block              = var.public_subnet_cidr
  map_public_ip_on_launch = true

  tags = {
    Name        = var.public_subnet_name
    Environment = var.environment
    Tier        = "Public"
  }
}

# 5 - Create a VPC Endpoint
# Data source to get the default security group of the VPC
data "aws_security_group" "default_sg" {
  filter {
    name   = "group-name"
    values = ["default"]
  }

  vpc_id = aws_vpc.vpc.id
}

# EC2 Enpoint -> Takes Ages to be created!
#resource "aws_ec2_instance_connect_endpoint" "ec2_connect_endpoint" {
#  security_group_ids = [data.aws_security_group.default_sg.id]
#  subnet_id          = aws_subnet.public_subnet.id
#
#  tags = {
#    Name = var.ec2_endpoint_name
#  }
#}


# 6 - Create an Internet Gateway
resource "aws_internet_gateway" "internet_gw" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name        = var.internet_gateway_name
    Environment = var.environment
  }
}

# 7 - Create a Route Table for the Public Subnet
# Create a Route Table for the Public Subnet
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name        = var.public_route_table_name
    Environment = var.environment
  }
}

# Route table associations for the Public Subnet
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public.id
}

# Route for Internet Gateway
resource "aws_route" "public_internet_gateway" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.internet_gw.id
  depends_on             = [aws_internet_gateway.internet_gw]
}

# 8 - Create NAT Gateway for the Private Subnet
# Elastic-IP (eip) for NAT
resource "aws_eip" "nat_eip" {
  depends_on = [aws_internet_gateway.internet_gw]
}

# Create the NAT
resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnet.id
  depends_on    = [aws_eip.nat_eip]

  tags = {
    Name        = var.nat_gateway_name
    Environment = var.environment
  }
}

# 9 - Create a Route Table for the Private Subnet
# Create a Route Table for the Private Subnet
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name        = var.private_route_table_name
    Environment = var.environment
  }
}

# Route table associations for the Public Subnet
resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private_subnet.id
  route_table_id = aws_route_table.private.id
}

# Route for NAT Gateway
resource "aws_route" "private_nat_gateway" {
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat_gateway.id
  depends_on             = [aws_nat_gateway.nat_gateway]
}

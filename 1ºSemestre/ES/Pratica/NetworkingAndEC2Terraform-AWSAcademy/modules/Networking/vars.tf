# Region and AZ
variable "aws_region" {
  description = "AWS Region"
}
variable "aws_az" {
  description = "AWS Availability Zone"
}

# VPC 
variable "vpc_name" {
  description = "VPC Name"
}
variable "vpc_cidr" {
  type        = string
  description = "CIDR block of the vpc"
}

# Subnets
variable "private_subnet_name" {
  type        = string
  description = "Name for the Private Subnet"
}
variable "private_subnet_cidr" {
  type        = string
  description = "CIDR block for the Private Subnet"
}
variable "public_subnet_name" {
  type        = string
  description = "Name for the Public Subnet"
}
variable "public_subnet_cidr" {
  type        = string
  description = "CIDR block for the Public Subnet"
}

# Internet Gateway
variable "ec2_endpoint_name" {
  type        = string
  description = "EC2 Connection Endpoint Name"
}

# Internet Gateway
variable "internet_gateway_name" {
  type        = string
  description = "Internet Gateway Name"
}

# NAT Gateways
variable "nat_gateway_name" {
  type        = string
  description = "NAT Gateway Name"
}

# Route Tables
variable "public_route_table_name" {
  type        = string
  description = "Public Route Table Name"
}
variable "private_route_table_name" {
  type        = string
  description = "Private Route Table Name"
}

# Environment
variable "environment" {
  type        = string
  description = "Environment"
}

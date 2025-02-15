variable "aws_access_key_id" {}
# export TF_VAR_aws_access_key_id=""
variable "aws_access_key_secret" {}
# export TF_VAR_aws_access_key_secret=""
variable "aws_session_token" {}
# export TF_VAR_aws_session_token=""

# Region and AZ
variable "aws_region" {
  description = "AWS Region"
  default     = "us-east-1"
}
variable "aws_az" {
  description = "AWS Availability Zone"
  default     = "us-east-1a"
}

# VPC 
variable "vpc_name" {
  description = "VPC Name"
  default     = "networking-tutorial"
}
variable "vpc_cidr" {
  type        = string
  description = "CIDR block of the vpc"
  default     = "10.10.0.0/16"
}

# Subnets
variable "private_subnet_name" {
  type        = string
  description = "Name for the Private Subnet"
  default     = "private-subnet-us-east-1a"
}
variable "private_subnet_cidr" {
  type        = string
  description = "CIDR block for the Private Subnet"
  default     = "10.10.11.0/24"
}
variable "public_subnet_name" {
  type        = string
  description = "Name for the Public Subnet"
  default     = "public-subnet-us-east-1a"
}
variable "public_subnet_cidr" {
  type        = string
  description = "CIDR block for the Public Subnet"
  default     = "10.10.1.0/24"
}

# Internet Gateway
variable "ec2_endpoint_name" {
  type        = string
  description = "EC2 Connection Endpoint Name"
  default     = "ec2-endpoint"
}


# Internet Gateway
variable "internet_gateway_name" {
  type        = string
  description = "Internet Gateway Name"
  default     = "internet-gw"
}

# NAT Gateways
variable "nat_gateway_name" {
  type        = string
  description = "NAT Gateway Name"
  default     = "nat-gw"
}

# Route Tables
variable "public_route_table_name" {
  type        = string
  description = "Public Route Table Name"
  default     = "public-route-table"
}
variable "private_route_table_name" {
  type        = string
  description = "Private Route Table Name"
  default     = "private-route-table"
}

# Security Groups
variable "ec2_security_group_name" {
  type        = string
  description = "Security Group Name to be used in EC2"
  default     = "all_open"
}

# SSH Keys
variable "ssh_key_pub_location" {
  type        = string
  description = "SSH Key to be used in AWS EC2"
}
variable "ssh_key_ec2_name" {
  type        = string
  description = "Name of SSH Key to be used in AWS EC2"
  default     = "ec2-key"
}

# EC2
variable "public_vm_name" {
  type        = string
  description = "Name of the Public AWS EC2 Instance"
  default     = "public-ec2-1"
}
variable "private_vm_name" {
  type        = string
  description = "Name of the Private AWS EC2 Instance"
  default     = "private-ec2-1"
}






# Environment
variable "environment" {
  type        = string
  description = "Environment"
  default     = "testing"
}

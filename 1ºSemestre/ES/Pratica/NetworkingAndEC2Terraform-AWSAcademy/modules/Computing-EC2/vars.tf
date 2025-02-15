# VPC 
variable "vpc_id" {
  description = "ID of the vpc"
}

# Subnets
variable "public_subnet_id" {
  type        = string
  description = "Public Subnet ID"
}
variable "private_subnet_id" {
  type        = string
  description = "Private Subnet ID"
}

# Security Groups
variable "ec2_security_group_name" {
  type        = string
  description = "Security Group Name to be used in EC2"
}

# SSH Keys
variable "ssh_key_pub_location" {
  type        = string
  description = "SSH Key to be used in AWS EC2"
}
variable "ssh_key_ec2_name" {
  type        = string
  description = "Name of SSH Key to be used in AWS EC2"
}

# EC2
variable "public_vm_name" {
  type        = string
  description = "Name of the Public AWS EC2 Instance"
}
variable "private_vm_name" {
  type        = string
  description = "Name of the Private AWS EC2 Instance"
}

# Environment
variable "environment" {
  type        = string
  description = "Environment"
}

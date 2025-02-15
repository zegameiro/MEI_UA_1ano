# PubN - T1  -  Create a Security Group for EC2 Instance
resource "aws_security_group" "ec2_security_group" {
  name        = var.ec2_security_group_name
  description = "This Security Group is VERY INSECURE"
  vpc_id      = var.vpc_id

  # Inbound rule: Allow all traffic from any IPv4 source
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # -1 stands for all protocols
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Outbound rules: Leave as is (default is to allow all outbound traffic)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = var.ec2_security_group_name
  }
}

# PubN – T2  -  Create a SSH Key To Access EC2 Instances
resource "aws_key_pair" "my_key_pair" {
  key_name   = var.ssh_key_ec2_name
  public_key = file("${var.ssh_key_pub_location}")
}

# PubN – T3  -  Create a Public EC2 Instance
resource "aws_instance" "public_vm" {
  ami           = "ami-007855ac798b5175e" # AMI = Ubuntu 22.04 AMD64
  instance_type = "t2.micro"
  subnet_id     = var.public_subnet_id
  # This Key was previously created
  key_name                    = var.ssh_key_ec2_name
  associate_public_ip_address = true

  # Root Disk
  root_block_device {
    volume_size           = "8"
    volume_type           = "standard"
    delete_on_termination = true
  }

  # Security Groups
  vpc_security_group_ids = [
    aws_security_group.ec2_security_group.id,
  ]

  # User data for initializing the instance
  user_data = <<-EOF
    #!/bin/bash
    # Update the package list
    sudo apt update -y

    # Install Apache
    sudo apt install -y apache2

    # Start Apache and enable it to start on boot
    sudo systemctl start apache2
    sudo systemctl enable apache2

    # Custom message in the default HTML page
    echo "<h1>Welcome to my Terraform-provisioned instance!</h1>" | sudo tee /var/www/html/index.html
  EOF

  tags = {
    Name        = var.public_vm_name
    Terraform   = "true"
    Environment = var.environment
  }
}

# PrivN – T1  -  Create a Public EC2 Instance
resource "aws_instance" "private_vm" {
  ami           = "ami-007855ac798b5175e" # AMI = Ubuntu 22.04 AMD64
  instance_type = "t2.micro"
  subnet_id     = var.private_subnet_id
  # This Key was previously created
  key_name = var.ssh_key_ec2_name
  # For AWS Academy Only
  iam_instance_profile = "LabInstanceProfile"

  # Root Disk
  root_block_device {
    volume_size           = "8"
    volume_type           = "standard"
    delete_on_termination = true
  }

  # Security Groups
  vpc_security_group_ids = [
    aws_security_group.ec2_security_group.id,
  ]

  tags = {
    Name        = var.private_vm_name
    Terraform   = "true"
    Environment = var.environment
  }
}

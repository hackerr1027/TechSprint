# Terraform Infrastructure as Code
# Generated from Infrastructure Model
# Model ID: model-v1
# Last Edit Source: initial
#
# METADATA NOTES:
#   infra_id: <id>  - Maps resource to model (DO NOT MODIFY)
#   editable: <prop> - Safe to edit this property

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# infra_id: vpc-main
resource "aws_vpc" "vpc_main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "main-vpc"
  }
}

# Internet Gateway for vpc-main
resource "aws_internet_gateway" "vpc_main_igw" {
  vpc_id = aws_vpc.vpc_main.id

  tags = {
    Name = "main-vpc-igw"
  }
}

# infra_id: subnet-public-1
resource "aws_subnet" "subnet_public_1" {
  vpc_id            = aws_vpc.vpc_main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-1"
    Type = "public"
  }
}

# Route Table for subnet-public-1
resource "aws_route_table" "subnet_public_1_rt" {
  vpc_id = aws_vpc.vpc_main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.vpc_main_igw.id
  }

  tags = {
    Name = "public-subnet-1-rt"
  }
}

resource "aws_route_table_association" "subnet_public_1_rta" {
  subnet_id      = aws_subnet.subnet_public_1.id
  route_table_id = aws_route_table.subnet_public_1_rt.id
}

# infra_id: subnet-private-1
resource "aws_subnet" "subnet_private_1" {
  vpc_id            = aws_vpc.vpc_main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "private-subnet-1"
    Type = "private"
  }
}

# infra_id: subnet-private-2
resource "aws_subnet" "subnet_private_2" {
  vpc_id            = aws_vpc.vpc_main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "private-subnet-2"
    Type = "private"
  }
}

# Security Group for EC2 instances
resource "aws_security_group" "ec2_sg" {
  name        = "ec2-security-group"
  description = "Security group for EC2 instances"
  vpc_id      = aws_vpc.vpc_main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# infra_id: ec2-web-1
resource "aws_instance" "ec2_web_1" {
  ami           = "ami-0c55b159cbfafe1f0"
  # editable: instance_type
  instance_type = "t2.micro"
  # editable: subnet_id
  subnet_id     = aws_subnet.subnet_private_1.id
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  tags = {
    Name = "web-server-1"
  }
}

# DB Subnet Group for rds-main
resource "aws_db_subnet_group" "rds_main_subnet_group" {
  name       = "main-database-subnet-group"
  subnet_ids = [aws_subnet.subnet_private_1.id, aws_subnet.subnet_private_2.id]

  tags = {
    Name = "main-database-subnet-group"
  }
}

# infra_id: rds-main
resource "aws_db_instance" "rds_main" {
  identifier           = "main-database"
  engine               = "postgres"
  # editable: instance_class
  instance_class       = "db.t3.micro"
  # editable: allocated_storage
  allocated_storage    = 20
  db_subnet_group_name = aws_db_subnet_group.rds_main_subnet_group.name
  skip_final_snapshot  = true

  # Credentials should be managed via AWS Secrets Manager in production
  username = "admin"
  password = "change-me-in-production"

  tags = {
    Name = "main-database"
  }
}

# infra_id: lb-main
resource "aws_lb" "lb_main" {
  name               = "main-load-balancer"
  internal           = false
  load_balancer_type = "application"
  subnets            = [aws_subnet.subnet_public_1.id]

  tags = {
    Name = "main-load-balancer"
  }
}

# Target Group for lb-main
resource "aws_lb_target_group" "lb_main_tg" {
  name     = "main-load-balancer-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.vpc_main.id
}

resource "aws_lb_target_group_attachment" "lb_main_ec2_web_1" {
  target_group_arn = aws_lb_target_group.lb_main_tg.arn
  target_id        = aws_instance.ec2_web_1.id
  port             = 80
}

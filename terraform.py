"""
Model-to-Terraform Generator
Converts InfrastructureModel to Terraform IaC code.
This reads from the model, never directly from text or diagrams.
"""

from .model import InfrastructureModel, SubnetType


def generate_terraform_code(model: InfrastructureModel) -> str:
    """
    Generate Terraform code from the infrastructure model.
    
    Model → Terraform (never Text → Terraform directly)
    
    Embeds stable resource IDs in comments for reverse-parsing.
    This allows us to parse Terraform back into edit operations.
    
    Metadata Format:
        # infra_id: resource-id  <- Maps back to model resource
        # editable: property     <- Marks safe-to-edit fields
    """
    lines = [
        "# Terraform Infrastructure as Code",
        "# Generated from Infrastructure Model",
        f"# Model ID: {model.model_id}",
        f"# Last Edit Source: {model.last_edit_source.value}",
        "#",
        "# METADATA NOTES:",
        "#   infra_id: <id>  - Maps resource to model (DO NOT MODIFY)",
        "#   editable: <prop> - Safe to edit this property",
        "",
        "terraform {",
        "  required_providers {",
        "    aws = {",
        "      source  = \"hashicorp/aws\"",
        "      version = \"~> 5.0\"",
        "    }",
        "  }",
        "}",
        "",
        "provider \"aws\" {",
        "  region = \"us-east-1\"",
        "}",
        ""
    ]
    
    # Generate VPCs
    for vpc in model.vpcs:
        lines.append(f"# infra_id: {vpc.id}")
        lines.append(f"resource \"aws_vpc\" \"{vpc.id.replace('-', '_')}\" {{")
        lines.append(f"  cidr_block           = \"{vpc.cidr}\"")
        lines.append(f"  enable_dns_hostnames = true")
        lines.append(f"  enable_dns_support   = true")
        lines.append(f"")
        lines.append(f"  tags = {{")
        lines.append(f"    Name = \"{vpc.name}\"")
        lines.append(f"  }}")
        lines.append(f"}}")
        lines.append("")
        
        # Generate Internet Gateway for VPCs with public subnets
        has_public = any(s.subnet_type == SubnetType.PUBLIC for s in vpc.subnets)
        if has_public:
            lines.append(f"# Internet Gateway for {vpc.id}")
            lines.append(f"resource \"aws_internet_gateway\" \"{vpc.id.replace('-', '_')}_igw\" {{")
            lines.append(f"  vpc_id = aws_vpc.{vpc.id.replace('-', '_')}.id")
            lines.append(f"")
            lines.append(f"  tags = {{")
            lines.append(f"    Name = \"{vpc.name}-igw\"")
            lines.append(f"  }}")
            lines.append(f"}}")
            lines.append("")
        
        # Generate Subnets
        for subnet in vpc.subnets:
            lines.append(f"# infra_id: {subnet.id}")
            lines.append(f"resource \"aws_subnet\" \"{subnet.id.replace('-', '_')}\" {{")
            lines.append(f"  vpc_id            = aws_vpc.{vpc.id.replace('-', '_')}.id")
            lines.append(f"  cidr_block        = \"{subnet.cidr}\"")
            lines.append(f"  availability_zone = \"{subnet.availability_zone}\"")
            
            if subnet.subnet_type == SubnetType.PUBLIC:
                lines.append(f"  map_public_ip_on_launch = true")
            
            lines.append(f"")
            lines.append(f"  tags = {{")
            lines.append(f"    Name = \"{subnet.name}\"")
            lines.append(f"    Type = \"{subnet.subnet_type.value}\"")
            lines.append(f"  }}")
            lines.append(f"}}")
            lines.append("")
            
            # Generate Route Table for public subnets
            if subnet.subnet_type == SubnetType.PUBLIC:
                lines.append(f"# Route Table for {subnet.id}")
                lines.append(f"resource \"aws_route_table\" \"{subnet.id.replace('-', '_')}_rt\" {{")
                lines.append(f"  vpc_id = aws_vpc.{vpc.id.replace('-', '_')}.id")
                lines.append(f"")
                lines.append(f"  route {{")
                lines.append(f"    cidr_block = \"0.0.0.0/0\"")
                lines.append(f"    gateway_id = aws_internet_gateway.{vpc.id.replace('-', '_')}_igw.id")
                lines.append(f"  }}")
                lines.append(f"")
                lines.append(f"  tags = {{")
                lines.append(f"    Name = \"{subnet.name}-rt\"")
                lines.append(f"  }}")
                lines.append(f"}}")
                lines.append("")
                
                lines.append(f"resource \"aws_route_table_association\" \"{subnet.id.replace('-', '_')}_rta\" {{")
                lines.append(f"  subnet_id      = aws_subnet.{subnet.id.replace('-', '_')}.id")
                lines.append(f"  route_table_id = aws_route_table.{subnet.id.replace('-', '_')}_rt.id")
                lines.append(f"}}")
                lines.append("")
    
    # Generate Security Groups
    if model.ec2_instances or model.rds_databases:
        lines.append("# Security Group for EC2 instances")
        lines.append(f"resource \"aws_security_group\" \"ec2_sg\" {{")
        lines.append(f"  name        = \"ec2-security-group\"")
        lines.append(f"  description = \"Security group for EC2 instances\"")
        if model.vpcs:
            lines.append(f"  vpc_id      = aws_vpc.{model.vpcs[0].id.replace('-', '_')}.id")
        lines.append(f"")
        lines.append(f"  ingress {{")
        lines.append(f"    from_port   = 80")
        lines.append(f"    to_port     = 80")
        lines.append(f"    protocol    = \"tcp\"")
        lines.append(f"    cidr_blocks = [\"0.0.0.0/0\"]")
        lines.append(f"  }}")
        lines.append(f"")
        lines.append(f"  ingress {{")
        lines.append(f"    from_port   = 443")
        lines.append(f"    to_port     = 443")
        lines.append(f"    protocol    = \"tcp\"")
        lines.append(f"    cidr_blocks = [\"0.0.0.0/0\"]")
        lines.append(f"  }}")
        lines.append(f"")
        lines.append(f"  egress {{")
        lines.append(f"    from_port   = 0")
        lines.append(f"    to_port     = 0")
        lines.append(f"    protocol    = \"-1\"")
        lines.append(f"    cidr_blocks = [\"0.0.0.0/0\"]")
        lines.append(f"  }}")
        lines.append(f"}}")
        lines.append("")
    
    # Generate EC2 Instances
    for ec2 in model.ec2_instances:
        lines.append(f"# infra_id: {ec2.id}")
        lines.append(f"resource \"aws_instance\" \"{ec2.id.replace('-', '_')}\" {{")
        lines.append(f"  ami           = \"{ec2.ami}\"")
        lines.append(f"  # editable: instance_type")
        lines.append(f"  instance_type = \"{ec2.instance_type.value}\"")
        lines.append(f"  # editable: subnet_id")
        lines.append(f"  subnet_id     = aws_subnet.{ec2.subnet_id.replace('-', '_')}.id")
        lines.append(f"  vpc_security_group_ids = [aws_security_group.ec2_sg.id]")
        lines.append(f"")
        lines.append(f"  tags = {{")
        lines.append(f"    Name = \"{ec2.name}\"")
        lines.append(f"  }}")
        lines.append(f"}}")
        lines.append("")
    
    # Generate RDS Databases
    for rds in model.rds_databases:
        # Create DB Subnet Group
        lines.append(f"# DB Subnet Group for {rds.id}")
        lines.append(f"resource \"aws_db_subnet_group\" \"{rds.id.replace('-', '_')}_subnet_group\" {{")
        lines.append(f"  name       = \"{rds.name}-subnet-group\"")
        subnet_refs = [f"aws_subnet.{sid.replace('-', '_')}.id" for sid in rds.subnet_ids]
        lines.append(f"  subnet_ids = [{', '.join(subnet_refs)}]")
        lines.append(f"")
        lines.append(f"  tags = {{")
        lines.append(f"    Name = \"{rds.name}-subnet-group\"")
        lines.append(f"  }}")
        lines.append(f"}}")
        lines.append("")
        
        # Create RDS instance
        lines.append(f"# infra_id: {rds.id}")
        lines.append(f"resource \"aws_db_instance\" \"{rds.id.replace('-', '_')}\" {{")
        lines.append(f"  identifier           = \"{rds.name}\"")
        lines.append(f"  engine               = \"{rds.engine.value}\"")
        lines.append(f"  # editable: instance_class")
        lines.append(f"  instance_class       = \"{rds.instance_class}\"")
        lines.append(f"  # editable: allocated_storage")
        lines.append(f"  allocated_storage    = {rds.allocated_storage}")
        lines.append(f"  db_subnet_group_name = aws_db_subnet_group.{rds.id.replace('-', '_')}_subnet_group.name")
        lines.append(f"  skip_final_snapshot  = true")
        lines.append(f"")
        lines.append(f"  # Credentials should be managed via AWS Secrets Manager in production")
        lines.append(f"  username = \"admin\"")
        lines.append(f"  password = \"change-me-in-production\"")
        lines.append(f"")
        lines.append(f"  tags = {{")
        lines.append(f"    Name = \"{rds.name}\"")
        lines.append(f"  }}")
        lines.append(f"}}")
        lines.append("")
    
    # Generate Load Balancers
    for lb in model.load_balancers:
        lines.append(f"# infra_id: {lb.id}")
        lines.append(f"resource \"aws_lb\" \"{lb.id.replace('-', '_')}\" {{")
        lines.append(f"  name               = \"{lb.name}\"")
        lines.append(f"  internal           = false")
        lines.append(f"  load_balancer_type = \"application\"")
        subnet_refs = [f"aws_subnet.{sid.replace('-', '_')}.id" for sid in lb.subnet_ids]
        lines.append(f"  subnets            = [{', '.join(subnet_refs)}]")
        lines.append(f"")
        lines.append(f"  tags = {{")
        lines.append(f"    Name = \"{lb.name}\"")
        lines.append(f"  }}")
        lines.append(f"}}")
        lines.append("")
        
        # Create Target Group
        if lb.target_instance_ids:
            lines.append(f"# Target Group for {lb.id}")
            lines.append(f"resource \"aws_lb_target_group\" \"{lb.id.replace('-', '_')}_tg\" {{")
            lines.append(f"  name     = \"{lb.name}-tg\"")
            lines.append(f"  port     = 80")
            lines.append(f"  protocol = \"HTTP\"")
            if model.vpcs:
                lines.append(f"  vpc_id   = aws_vpc.{model.vpcs[0].id.replace('-', '_')}.id")
            lines.append(f"}}")
            lines.append("")
            
            # Attach instances to target group
            for target_id in lb.target_instance_ids:
                lines.append(f"resource \"aws_lb_target_group_attachment\" \"{lb.id.replace('-', '_')}_{target_id.replace('-', '_')}\" {{")
                lines.append(f"  target_group_arn = aws_lb_target_group.{lb.id.replace('-', '_')}_tg.arn")
                lines.append(f"  target_id        = aws_instance.{target_id.replace('-', '_')}.id")
                lines.append(f"  port             = 80")
                lines.append(f"}}")
                lines.append("")
    
    return "\n".join(lines)

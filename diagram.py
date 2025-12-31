"""
Model-to-Diagram Generator
Converts InfrastructureModel to Mermaid diagram format.
This reads from the model, never directly from text or Terraform.
"""

from .model import InfrastructureModel, SubnetType


def generate_mermaid_diagram(model: InfrastructureModel) -> str:
    """
    Generate a Mermaid diagram from the infrastructure model.
    
    Model → Diagram (never Text → Diagram directly)
    
    The diagram shows:
    - VPCs as subgraphs
    - Subnets as nested subgraphs
    - EC2, RDS, and Load Balancers as nodes
    - Relationships between components
    """
    lines = ["graph TB"]
    lines.append("    %% Infrastructure Diagram Generated from Model")
    lines.append("")
    
    # Track all components for relationship mapping
    all_subnets = {}
    
    # Generate VPCs and Subnets
    for vpc in model.vpcs:
        lines.append(f"    subgraph {vpc.id}[\"{vpc.name}<br/>{vpc.cidr}\"]")
        lines.append(f"        direction TB")
        
        # Generate subnets within VPC
        for subnet in vpc.subnets:
            all_subnets[subnet.id] = subnet
            subnet_style = "fill:#e1f5e1" if subnet.subnet_type == SubnetType.PUBLIC else "fill:#ffe1e1"
            subnet_label = f"{subnet.name}<br/>{subnet.cidr}<br/>({subnet.subnet_type.value})"
            
            lines.append(f"        subgraph {subnet.id}[\"{subnet_label}\"]")
            lines.append(f"            direction TB")
            
            # Add EC2 instances in this subnet
            for ec2 in model.ec2_instances:
                if ec2.subnet_id == subnet.id:
                    lines.append(f"            {ec2.id}[\"🖥️ {ec2.name}<br/>{ec2.instance_type.value}\"]")
            
            # Add RDS databases in this subnet (if primary subnet)
            for rds in model.rds_databases:
                if subnet.id in rds.subnet_ids and subnet.id == rds.subnet_ids[0]:
                    lines.append(f"            {rds.id}[\"🗄️ {rds.name}<br/>{rds.engine.value}<br/>{rds.instance_class}\"]")
            
            lines.append(f"        end")
            lines.append(f"        style {subnet.id} {subnet_style}")
        
        lines.append(f"    end")
        lines.append(f"    style {vpc.id} fill:#e1e8f5,stroke:#333,stroke-width:2px")
        lines.append("")
    
    # Add Load Balancers (outside VPC subgraph for clarity)
    for lb in model.load_balancers:
        lines.append(f"    {lb.id}[\"⚖️ {lb.name}<br/>Application Load Balancer\"]")
        lines.append(f"    style {lb.id} fill:#fff4e1,stroke:#333,stroke-width:2px")
    
    lines.append("")
    lines.append("    %% Relationships")
    
    # Add relationships: Load Balancer → EC2 instances
    for lb in model.load_balancers:
        for target_id in lb.target_instance_ids:
            lines.append(f"    {lb.id} --> {target_id}")
    
    # Add relationships: EC2 → RDS (if EC2 is in private subnet and RDS exists)
    for ec2 in model.ec2_instances:
        subnet = model.get_subnet_by_id(ec2.subnet_id)
        if subnet and subnet.subnet_type == SubnetType.PRIVATE:
            for rds in model.rds_databases:
                lines.append(f"    {ec2.id} -.-> {rds.id}")
    
    return "\n".join(lines)


def generate_diagram_description(model: InfrastructureModel) -> str:
    """
    Generate a human-readable description of the infrastructure.
    Useful for documentation or API responses.
    """
    parts = []
    
    # VPC summary
    for vpc in model.vpcs:
        parts.append(f"VPC '{vpc.name}' ({vpc.cidr}) with {len(vpc.subnets)} subnet(s)")
    
    # EC2 summary
    if model.ec2_instances:
        parts.append(f"{len(model.ec2_instances)} EC2 instance(s)")
    
    # RDS summary
    if model.rds_databases:
        parts.append(f"{len(model.rds_databases)} RDS database(s)")
    
    # Load Balancer summary
    if model.load_balancers:
        parts.append(f"{len(model.load_balancers)} load balancer(s)")
    
    return ", ".join(parts)

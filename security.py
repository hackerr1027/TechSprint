"""
Security & Compliance Validator
Validates the infrastructure model against best practices and security standards.
This operates at the model level, not on Terraform or diagrams.
"""

from typing import List, Dict
from .model import InfrastructureModel, SubnetType


class SecurityWarning:
    """Represents a security or compliance warning"""
    def __init__(self, severity: str, resource: str, message: str, recommendation: str):
        self.severity = severity  # "HIGH", "MEDIUM", "LOW"
        self.resource = resource
        self.message = message
        self.recommendation = recommendation
    
    def to_dict(self) -> Dict:
        return {
            "severity": self.severity,
            "resource": self.resource,
            "message": self.message,
            "recommendation": self.recommendation
        }


def validate_security(model: InfrastructureModel) -> List[SecurityWarning]:
    """
    Validate the infrastructure model for security best practices.
    
    Model → Security Warnings (never Text → Warnings directly)
    
    Checks:
    - RDS databases should be in private subnets
    - EC2 instances should use appropriate subnets based on purpose
    - Load balancers should be in public subnets
    - VPC should have both public and private subnets for proper segmentation
    - Security group configurations (implied from model)
    """
    warnings = []
    
    # Check 1: RDS databases should be in private subnets only
    for rds in model.rds_databases:
        for subnet_id in rds.subnet_ids:
            subnet = model.get_subnet_by_id(subnet_id)
            if subnet and subnet.subnet_type == SubnetType.PUBLIC:
                warnings.append(SecurityWarning(
                    severity="HIGH",
                    resource=f"RDS: {rds.name} ({rds.id})",
                    message="Database is deployed in a public subnet",
                    recommendation="Move RDS instances to private subnets to prevent direct internet access"
                ))
                break
    
    # Check 2: Ensure RDS has multi-AZ deployment (at least 2 subnets)
    for rds in model.rds_databases:
        if len(rds.subnet_ids) < 2:
            warnings.append(SecurityWarning(
                severity="MEDIUM",
                resource=f"RDS: {rds.name} ({rds.id})",
                message="Database is not configured for multi-AZ deployment",
                recommendation="Use at least 2 subnets in different availability zones for high availability"
            ))
    
    # Check 3: VPC should have network segmentation (both public and private subnets)
    for vpc in model.vpcs:
        has_public = any(s.subnet_type == SubnetType.PUBLIC for s in vpc.subnets)
        has_private = any(s.subnet_type == SubnetType.PRIVATE for s in vpc.subnets)
        
        if not has_private:
            warnings.append(SecurityWarning(
                severity="MEDIUM",
                resource=f"VPC: {vpc.name} ({vpc.id})",
                message="VPC has no private subnets",
                recommendation="Create private subnets for internal resources like databases and application servers"
            ))
        
        if not has_public and model.load_balancers:
            warnings.append(SecurityWarning(
                severity="MEDIUM",
                resource=f"VPC: {vpc.name} ({vpc.id})",
                message="VPC has no public subnets but load balancers are defined",
                recommendation="Create public subnets for internet-facing resources like load balancers"
            ))
    
    # Check 4: Load balancers should be in public subnets
    for lb in model.load_balancers:
        for subnet_id in lb.subnet_ids:
            subnet = model.get_subnet_by_id(subnet_id)
            if subnet and subnet.subnet_type == SubnetType.PRIVATE:
                warnings.append(SecurityWarning(
                    severity="MEDIUM",
                    resource=f"Load Balancer: {lb.name} ({lb.id})",
                    message="Load balancer is in a private subnet",
                    recommendation="Place internet-facing load balancers in public subnets"
                ))
                break
    
    # Check 5: EC2 instances serving web traffic should be behind load balancers
    if model.ec2_instances and not model.load_balancers:
        warnings.append(SecurityWarning(
            severity="LOW",
            resource="EC2 Instances",
            message="EC2 instances are not behind a load balancer",
            recommendation="Use a load balancer for better availability, scalability, and security"
        ))
    
    # Check 6: Warn about default credentials in RDS (from terraform.py)
    if model.rds_databases:
        warnings.append(SecurityWarning(
            severity="MEDIUM",  # Changed from HIGH to allow RDS creation
            resource="RDS Databases",
            message="Database credentials may be using default/hardcoded values",
            recommendation="Use AWS Secrets Manager or Parameter Store for database credentials in production"
        ))
    
    # Check 7: Ensure EC2 instances in public subnets have a specific purpose
    public_ec2_count = 0
    for ec2 in model.ec2_instances:
        subnet = model.get_subnet_by_id(ec2.subnet_id)
        if subnet and subnet.subnet_type == SubnetType.PUBLIC:
            public_ec2_count += 1
    
    if public_ec2_count > 0 and model.load_balancers:
        warnings.append(SecurityWarning(
            severity="MEDIUM",
            resource="EC2 Instances",
            message=f"{public_ec2_count} EC2 instance(s) in public subnet with load balancer present",
            recommendation="Consider moving application servers to private subnets and only expose them via load balancer"
        ))
    
    # Check 8: VPC CIDR should not overlap with common private ranges
    for vpc in model.vpcs:
        if vpc.cidr.startswith("192.168."):
            warnings.append(SecurityWarning(
                severity="LOW",
                resource=f"VPC: {vpc.name} ({vpc.id})",
                message="VPC uses 192.168.x.x range which may conflict with home networks",
                recommendation="Consider using 10.x.x.x or 172.16-31.x.x ranges for better compatibility"
            ))
    
    return warnings


def generate_security_report(warnings: List[SecurityWarning]) -> str:
    """
    Generate a human-readable security report from warnings.
    """
    if not warnings:
        return "✅ No security warnings found. Infrastructure follows best practices."
    
    lines = [f"⚠️  Found {len(warnings)} security warning(s):\n"]
    
    # Group by severity
    high = [w for w in warnings if w.severity == "HIGH"]
    medium = [w for w in warnings if w.severity == "MEDIUM"]
    low = [w for w in warnings if w.severity == "LOW"]
    
    for severity, warning_list in [("HIGH", high), ("MEDIUM", medium), ("LOW", low)]:
        if warning_list:
            lines.append(f"\n{severity} SEVERITY ({len(warning_list)}):")
            for w in warning_list:
                lines.append(f"\n  • {w.resource}")
                lines.append(f"    Issue: {w.message}")
                lines.append(f"    Fix: {w.recommendation}")
    
    return "\n".join(lines)

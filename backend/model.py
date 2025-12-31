"""
Infrastructure Model - Single Source of Truth
This module defines the core infrastructure graph model.
All transformations (text->model, model->diagram, model->terraform) go through this.

Edit Tracking: Models track their edit source to prevent infinite loops
when synchronizing between diagram and Terraform views.
"""

from typing import List, Optional, Dict
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class EditSource(Enum):
    """Source of the last edit to prevent infinite loops"""
    TEXT = "text"          # From natural language input
    DIAGRAM = "diagram"    # From diagram edit events
    TERRAFORM = "terraform" # From Terraform code edits
    INITIAL = "initial"    # Initial creation


class SubnetType(Enum):
    """Subnet visibility type"""
    PUBLIC = "public"
    PRIVATE = "private"


class InstanceType(Enum):
    """EC2 instance types"""
    T2_MICRO = "t2.micro"
    T2_SMALL = "t2.small"
    T2_MEDIUM = "t2.medium"
    T3_MICRO = "t3.micro"
    T3_SMALL = "t3.small"


class DatabaseEngine(Enum):
    """RDS database engines"""
    POSTGRES = "postgres"
    MYSQL = "mysql"
    MARIADB = "mariadb"


@dataclass
class Subnet:
    """Represents a subnet within a VPC"""
    id: str
    name: str
    cidr: str
    subnet_type: SubnetType
    availability_zone: str = "us-east-1a"
    
    def __post_init__(self):
        """Ensure subnet_type is an Enum"""
        if isinstance(self.subnet_type, str):
            self.subnet_type = SubnetType(self.subnet_type)


@dataclass
class EC2Instance:
    """Represents an EC2 instance"""
    id: str
    name: str
    instance_type: InstanceType
    subnet_id: str
    ami: str = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI
    
    def __post_init__(self):
        """Ensure instance_type is an Enum"""
        if isinstance(self.instance_type, str):
            self.instance_type = InstanceType(self.instance_type)


@dataclass
class RDSDatabase:
    """Represents an RDS database instance"""
    id: str
    name: str
    engine: DatabaseEngine
    instance_class: str
    subnet_ids: List[str]
    allocated_storage: int = 20
    
    def __post_init__(self):
        """Ensure engine is an Enum"""
        if isinstance(self.engine, str):
            self.engine = DatabaseEngine(self.engine)


@dataclass
class LoadBalancer:
    """Represents an Application Load Balancer"""
    id: str
    name: str
    subnet_ids: List[str]
    target_instance_ids: List[str] = field(default_factory=list)


@dataclass
class S3Bucket:
    """Represents an S3 storage bucket"""
    id: str
    name: str
    versioning_enabled: bool = False
    encryption_enabled: bool = True


@dataclass
class SecurityGroup:
    """Represents a security group (firewall rules)"""
    id: str
    name: str
    vpc_id: str
    description: str = "Security group"
    ingress_rules: List[Dict] = field(default_factory=list)
    egress_rules: List[Dict] = field(default_factory=list)



@dataclass
class VPC:
    """Represents a Virtual Private Cloud"""
    id: str
    name: str
    cidr: str
    subnets: List[Subnet] = field(default_factory=list)
    
    def add_subnet(self, subnet: Subnet):
        """Add a subnet to this VPC"""
        self.subnets.append(subnet)


@dataclass
class InfrastructureModel:
    """
    The central infrastructure model - single source of truth.
    This is the graph that connects all infrastructure components.
    
    Edit Tracking:
    - last_edit_source: Prevents infinite loops during sync
    - last_edit_timestamp: For version control and debugging
    - model_id: Unique identifier for this model state
    """
    vpcs: List[VPC] = field(default_factory=list)
    ec2_instances: List[EC2Instance] = field(default_factory=list)
    rds_databases: List[RDSDatabase] = field(default_factory=list)
    load_balancers: List[LoadBalancer] = field(default_factory=list)
    s3_buckets: List[S3Bucket] = field(default_factory=list)
    security_groups: List[SecurityGroup] = field(default_factory=list)
    
    # Edit tracking fields
    last_edit_source: EditSource = EditSource.INITIAL
    last_edit_timestamp: Optional[datetime] = None
    model_id: str = "model-v1"  # Incremented on edits for conflict detection
    
    def add_vpc(self, vpc: VPC):
        """Add a VPC to the model"""
        self.vpcs.append(vpc)
    
    def add_ec2(self, instance: EC2Instance):
        """Add an EC2 instance to the model"""
        self.ec2_instances.append(instance)
    
    def add_rds(self, database: RDSDatabase):
        """Add an RDS database to the model"""
        self.rds_databases.append(database)
    
    def add_load_balancer(self, lb: LoadBalancer):
        """Add a load balancer to the model"""
        self.load_balancers.append(lb)
    
    def add_s3_bucket(self, bucket: S3Bucket):
        """Add an S3 bucket to the model"""
        self.s3_buckets.append(bucket)
    
    def add_security_group(self, sg: SecurityGroup):
        """Add a security group to the model"""
        self.security_groups.append(sg)
    
    def get_subnet_by_id(self, subnet_id: str) -> Optional[Subnet]:
        """Find a subnet by ID across all VPCs"""
        for vpc in self.vpcs:
            for subnet in vpc.subnets:
                if subnet.id == subnet_id:
                    return subnet
        return None
    
    def get_vpc_for_subnet(self, subnet_id: str) -> Optional[VPC]:
        """Find which VPC contains a given subnet"""
        for vpc in self.vpcs:
            for subnet in vpc.subnets:
                if subnet.id == subnet_id:
                    return vpc
        return None
    
    def update_edit_tracking(self, source: EditSource):
        """Update edit tracking when model is modified"""
        self.last_edit_source = source
        self.last_edit_timestamp = datetime.now()
        # Update model ID for version tracking
        version = int(self.model_id.split('-v')[-1]) + 1
        self.model_id = f"model-v{version}"
    
    def to_dict(self) -> Dict:
        """Convert model to dictionary for debugging/logging"""
        return {
            "vpcs": [
                {
                    "id": vpc.id,
                    "name": vpc.name,
                    "cidr": vpc.cidr,
                    "subnets": [
                        {
                            "id": s.id,
                            "name": s.name,
                            "cidr": s.cidr,
                            "type": s.subnet_type.value
                        } for s in vpc.subnets
                    ]
                } for vpc in self.vpcs
            ],
            "ec2_instances": [
                {
                    "id": ec2.id,
                    "name": ec2.name,
                    "type": ec2.instance_type.value,
                    "subnet": ec2.subnet_id
                } for ec2 in self.ec2_instances
            ],
            "rds_databases": [
                {
                    "id": rds.id,
                    "name": rds.name,
                    "engine": rds.engine.value,
                    "subnets": rds.subnet_ids
                } for rds in self.rds_databases
            ],
            "load_balancers": [
                {
                    "id": lb.id,
                    "name": lb.name,
                    "subnets": lb.subnet_ids,
                    "targets": lb.target_instance_ids
                } for lb in self.load_balancers
            ]
        }

# AI-Driven Infrastructure Backend - README

## Overview

A complete FastAPI backend that generates infrastructure diagrams and Terraform IaC code from natural language descriptions using a **model-centric architecture**.

## Quick Start

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run the server
uvicorn backend.main:app --reload
```

Server runs at `http://localhost:8000`

## API Usage

### Generate Infrastructure

```bash
POST /text
Content-Type: application/json

{
  "text": "Create a VPC with public and private subnets. Deploy an EC2 instance in the public subnet and a PostgreSQL RDS database in the private subnet. Add a load balancer."
}
```

**Response includes**:
- Mermaid diagram
- Terraform code
- Security warnings
- Infrastructure model summary

### Health Check

```bash
GET /health
```

## Architecture

```
Text Input → Parser (Mock LLM) → Infrastructure Model → [Diagram, Terraform, Security]
```

**Key Principle**: The Infrastructure Model is the single source of truth. All outputs derive from it.

## Project Structure

```
backend/
├── main.py          # FastAPI app
├── model.py         # Infrastructure graph model
├── parser.py        # Text → Model (mock LLM)
├── diagram.py       # Model → Mermaid
├── terraform.py     # Model → Terraform
├── security.py      # Security validation
└── requirements.txt # Dependencies
```

## Supported Resources

- **VPC**: Virtual Private Cloud with CIDR blocks
- **Subnets**: Public and private subnets with availability zones
- **EC2**: Instances with configurable types (t2.micro, t2.small, etc.)
- **RDS**: PostgreSQL, MySQL, MariaDB databases
- **Load Balancers**: Application Load Balancers with target groups

## Security Features

Validates infrastructure against best practices:
- RDS databases in private subnets
- Multi-AZ deployment for databases
- Network segmentation
- Credential management warnings
- Load balancer placement

## Testing

Run the test script:

```bash
python test_backend.py
```

Outputs saved to:
- `output_diagram.mmd` - Mermaid diagram
- `output_terraform.tf` - Terraform code
- `output_security.txt` - Security report

## API Documentation

Interactive API docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Future Enhancements

1. Replace mock LLM with real AI (OpenAI, Anthropic)
2. Add more AWS resources (S3, Lambda, API Gateway)
3. Implement Terraform → Model reverse parsing
4. Build frontend UI for visualization
5. Add Terraform syntax validation

## Requirements

- Python 3.11+
- FastAPI 0.109.0
- Uvicorn 0.27.0
- Pydantic 2.5.3

## License

MIT

"""
Test script for the AI-Driven Infrastructure Generator backend
"""

import requests
import json
import sys
import io

# Set UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# API endpoint
BASE_URL = "http://localhost:8000"

def test_text_endpoint():
    """Test the /text endpoint with a sample infrastructure description"""
    
    # Sample infrastructure request
    payload = {
        "text": "Create a VPC with public and private subnets. Deploy an EC2 instance in the public subnet and a PostgreSQL RDS database in the private subnet. Add a load balancer."
    }
    
    print("=" * 80)
    print("Testing /text endpoint")
    print("=" * 80)
    print(f"\nInput: {payload['text']}\n")
    
    # Make request
    response = requests.post(f"{BASE_URL}/text", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        
        print("[SUCCESS]!\n")
        print(f"Description: {data['description']}\n")
        
        print("-" * 80)
        print("MERMAID DIAGRAM:")
        print("-" * 80)
        print(data['mermaid_diagram'])
        print()
        
        print("-" * 80)
        print("TERRAFORM CODE:")
        print("-" * 80)
        print(data['terraform_code'][:500] + "...")  # First 500 chars
        print()
        
        print("-" * 80)
        print("SECURITY REPORT:")
        print("-" * 80)
        print(data['security_report'])
        print()
        
        # Save outputs to files
        with open("output_diagram.mmd", "w", encoding="utf-8") as f:
            f.write(data['mermaid_diagram'])
        print("[OK] Saved Mermaid diagram to output_diagram.mmd")
        
        with open("output_terraform.tf", "w", encoding="utf-8") as f:
            f.write(data['terraform_code'])
        print("[OK] Saved Terraform code to output_terraform.tf")
        
        with open("output_security.txt", "w", encoding="utf-8") as f:
            f.write(data['security_report'])
        print("[OK] Saved security report to output_security.txt")
        
    else:
        print(f"[FAILED]: {response.status_code}")
        print(response.text)

def test_health_endpoint():
    """Test the /health endpoint"""
    print("\n" + "=" * 80)
    print("Testing /health endpoint")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("[OK] Health check passed")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"[FAILED] Health check failed: {response.status_code}")

if __name__ == "__main__":
    test_health_endpoint()
    test_text_endpoint()

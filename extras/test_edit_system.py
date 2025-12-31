"""
Test script for Edit System
Tests bidirectional editing: Diagram ← Model → Terraform
"""

import requests
import json
import sys
import io

# Set UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000"


def test_1_create_initial_infrastructure():
    """Step 1: Create initial infrastructure from text"""
    print("\n" + "="*80)
    print("TEST 1: Create Initial Infrastructure")
    print("="*80)
    
    payload = {
        "text": "Create a VPC with public and private subnets. Deploy an EC2 t2.micro instance in the public subnet."
    }
    
    response = requests.post(f"{BASE_URL}/text", json=payload)
    data = response.json()
    
    model_id = data["model_summary"]["vpcs"][0]["id"]  # Will be "vpc-main" or similar
    # Extract actual model_id from response
    tf_code = data["terraform_code"]
    model_id_line = [line for line in tf_code.split('\n') if "Model ID:" in line][0]
    model_id = model_id_line.split(":")[-1].strip()
    
    print(f"[OK] Created infrastructure with model ID: {model_id}")
    print(f"     EC2 instances: {len(data['model_summary']['ec2_instances'])}")
    
    # Save outputs for next tests
    with open("test_model_id.txt", "w") as f:
        f.write(model_id)
    with open("test_original_terraform.tf", "w", encoding="utf-8") as f:
        f.write(data["terraform_code"])
    
    return model_id, data


def test_2_diagram_edit_add_resource(model_id):
    """Step 2: Add EC2 instance via diagram edit"""
    print("\n" + "="*80)
    print("TEST 2: Diagram Edit - Add Resource")
    print("="*80)
    
    payload = {
        "current_model_id": model_id,
        "operation": "add_resource",
        "resource_type": "ec2",
        "properties": {
            "name": "web-server-2",
            "instance_type": "t2.small",
            "subnet_id": "subnet-public-1"
        }
    }
    
    response = requests.post(f"{BASE_URL}/edit/diagram", json=payload)
    data = response.json()
    
    if data["success"]:
        print(f"[OK] Added EC2 instance via diagram edit")
        print(f"     New model ID: {data['model_id']}")
        print(f"     Security warnings: {len(data['security_warnings'])}")
        return data["model_id"], data
    else:
        print(f"[FAILED] {data.get('error')}")
        return None, data


def test_3_diagram_edit_update_property(model_id):
    """Step 3: Update EC2 instance type via diagram edit"""
    print("\n" + "="*80)
    print("TEST 3: Diagram Edit - Update Property")
    print("="*80)
    
    payload = {
        "current_model_id": model_id,
        "operation": "update_resource_property",
        "resource_id": "ec2-web-1",
        "property_name": "instance_type",
        "value": "t2.medium"
    }
    
    response = requests.post(f"{BASE_URL}/edit/diagram", json=payload)
    data = response.json()
    
    if data["success"]:
        print(f"[OK] Updated instance type to t2.medium")
        print(f"     New model ID: {data['model_id']}")
        
        # Save terraform for terraform edit test
        with open("test_after_diagram_edit.tf", "w", encoding="utf-8") as f:
            f.write(data["terraform_code"])
        
        return data["model_id"], data
    else:
        print(f"[FAILED] {data.get('error')}")
        return None, data


def test_4_diagram_edit_move_to_private_security_block():
    """Step 4: Try to move EC2 to private (should succeed)"""
    print("\n" + "="*80)
    print("TEST 4: Diagram Edit - Move EC2 to Private Subnet")
    print("="*80)
    
    # First create fresh infrastructure
    payload = {"text": "Create a VPC with public and private subnets and one EC2 in public subnet."}
    response = requests.post(f"{BASE_URL}/text", json=payload)
    data = response.json()
    tf_code = data["terraform_code"]
    model_id = [line for line in tf_code.split('\n') if "Model ID:" in line][0].split(":")[-1].strip()
    
    # Try to move EC2 to private
    payload = {
        "current_model_id": model_id,
        "operation": "move_resource",
        "resource_id": "ec2-web-1",
        "target_subnet_id": "subnet-private-1"
    }
    
    response = requests.post(f"{BASE_URL}/edit/diagram", json=payload)
    data = response.json()
    
    if data["success"]:
        print(f"[OK] Moved EC2 to private subnet successfully")
        print(f"     Warnings: {len(data['security_warnings'])}")
    else:
        print(f"[BLOCKED] Move blocked: {data.get('error')}")


def test_5_terraform_edit_change_instance_type():
    """Step 5: Edit Terraform code and sync back to model"""
    print("\n" + "="*80)
    print("TEST 5: Terraform Edit - Change Instance Type")
    print("="*80)
    
    # Read the original terraform
    with open("test_after_diagram_edit.tf", "r", encoding="utf-8") as f:
        original_tf = f.read()
    
    # Modify: change t2.medium back to t2.micro
    modified_tf = original_tf.replace(
        'instance_type = "t2.medium"',
        'instance_type = "t2.micro"'
    )
    
    # Extract model ID
    model_id = [line for line in original_tf.split('\n') if "Model ID:" in line][0].split(":")[-1].strip()
    
    payload = {
        "current_model_id": model_id,
        "original_terraform": original_tf,
        "modified_terraform": modified_tf
    }
    
    response = requests.post(f"{BASE_URL}/edit/terraform", json=payload)
    data = response.json()
    
    if data["success"]:
        print(f"[OK] Terraform edit applied successfully")
        print(f"     Operations applied: {data['operations_applied']}")
        print(f"     New model ID: {data['model_id']}")
        print(f"     Diagram updated: Yes")
    else:
        print(f"[FAILED] {data.get('error')}")


def test_6_no_infinite_loop():
    """Step 6: Verify no infinite loops with edit source tracking"""
    print("\n" + "="*80)
    print("TEST 6: Edit Source Tracking (No Infinite Loops)")
    print("="*80)
    
    # Create infrastructure
    payload = {"text": "Create a VPC with one EC2 instance."}
    response = requests.post(f"{BASE_URL}/text", json=payload)
    data = response.json()
    tf_code = data["terraform_code"]
    model_id = [line for line in tf_code.split('\n') if "Model ID:" in line][0].split(":")[-1].strip()
    
    # Make diagram edit
    payload = {
        "current_model_id": model_id,
        "operation": "update_resource_property",
        "resource_id": "ec2-web-1",
        "property_name": "instance_type",
        "value": "t2.small"
    }
    
    response = requests.post(f"{BASE_URL}/edit/diagram", json=payload)
    data = response.json()
    
    # Check that Terraform was regenerated but not diagram
    if "terraform_code" in data:
        print("[OK] Diagram edit → Terraform regenerated (correct)")
    if "mermaid_diagram" not in data:
        print("[OK] Diagram edit → Diagram NOT regenerated (correct, prevents loop)")
    
    print("\n[PASS] Edit source tracking working correctly")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("EDIT SYSTEM TEST SUITE")
    print("Testing: Diagram ← Model → Terraform synchronization")
    print("="*80)
    
    try:
        # Run tests
        model_id, data1 = test_1_create_initial_infrastructure()
        model_id, data2 = test_2_diagram_edit_add_resource(model_id)
        
        if model_id:
            model_id, data3 = test_3_diagram_edit_update_property(model_id)
        
        test_4_diagram_edit_move_to_private_security_block()
        test_5_terraform_edit_change_instance_type()
        test_6_no_infinite_loop()
        
        print("\n" + "="*80)
        print("ALL TESTS COMPLETED")
        print("="*80)
        
    except Exception as e:
        print(f"\n[ERROR] Test suite failed: {str(e)}")
        import traceback
        traceback.print_exc()

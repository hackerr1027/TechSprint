// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// Global state
let currentModelId = null;

// Initialize Mermaid
mermaid.initialize({
    startOnLoad: false,
    theme: 'default',
    securityLevel: 'loose'
});

/**
 * Generate infrastructure from text input
 */
async function generateInfrastructure() {
    const userInput = document.getElementById('user-input').value.trim();

    if (!userInput) {
        alert('Please enter an infrastructure description');
        return;
    }

    // Show loading state
    const generateBtn = document.getElementById('generate-btn');
    const loading = document.getElementById('loading');
    generateBtn.disabled = true;
    loading.classList.remove('hidden');

    try {
        const response = await fetch(`${API_BASE_URL}/text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: userInput })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Store model ID
        currentModelId = data.model_summary.model_id;

        // Display results
        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to generate infrastructure. Make sure the backend is running at ' + API_BASE_URL);
    } finally {
        generateBtn.disabled = false;
        loading.classList.add('hidden');
    }
}

/**
 * Display generated infrastructure results
 */
function displayResults(data) {
    // Show results section
    document.getElementById('results').style.display = 'grid';

    // Display model ID
    document.getElementById('model-id').textContent = `Model: ${data.model_summary.model_id}`;

    // Render Mermaid diagram
    renderDiagram(data.mermaid_diagram);

    // Display Terraform code
    document.getElementById('terraform-code').textContent = data.terraform_code;

    // Display security warnings
    displaySecurityWarnings(data.security_warnings);

    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Render Mermaid diagram
 */
function renderDiagram(mermaidCode) {
    const container = document.getElementById('diagram-container');

    // Clear previous diagram
    container.innerHTML = mermaidCode;

    // Render new diagram
    mermaid.init(undefined, container);
}

/**
 * Display security warnings
 */
function displaySecurityWarnings(warnings) {
    const container = document.getElementById('security-warnings');

    if (!warnings || warnings.length === 0) {
        container.innerHTML = '<div class="no-warnings">✅ No security warnings - Infrastructure looks good!</div>';
        return;
    }

    container.innerHTML = warnings.map(warning => `
        <div class="warning warning-${warning.severity}">
            <span class="warning-severity">${warning.severity}:</span>
            ${warning.message}
        </div>
    `).join('');
}

/**
 * Copy Terraform code to clipboard
 */
function copyTerraform() {
    const terraformCode = document.getElementById('terraform-code').textContent;

    navigator.clipboard.writeText(terraformCode).then(() => {
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = '✅ Copied!';
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy to clipboard');
    });
}

/**
 * Add a new resource via diagram edit
 */
async function addResource() {
    if (!currentModelId) {
        alert('Please generate infrastructure first');
        return;
    }

    const resourceType = document.getElementById('resource-type').value;
    const resourceName = document.getElementById('resource-name').value.trim();

    if (!resourceName) {
        alert('Please enter a resource name');
        return;
    }

    // Build properties based on resource type
    const properties = {
        name: resourceName
    };

    // Add type-specific properties
    if (resourceType === 'ec2') {
        properties.instance_type = 't2.micro';
        properties.subnet_id = 'subnet-public-1'; // Default, should be dynamic in production
    } else if (resourceType === 'rds') {
        properties.engine = 'postgres';
        properties.instance_class = 'db.t3.micro';
        properties.subnet_ids = ['subnet-private-1', 'subnet-private-2'];
    } else if (resourceType === 'load_balancer') {
        properties.subnet_ids = ['subnet-public-1'];
        properties.target_instance_ids = [];
    }

    try {
        const response = await fetch(`${API_BASE_URL}/edit/diagram`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                current_model_id: currentModelId,
                operation: 'add_resource',
                resource_type: resourceType,
                properties: properties
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            alert(`✅ ${resourceType.toUpperCase()} "${resourceName}" added successfully!`);

            // Update Terraform code
            document.getElementById('terraform-code').textContent = data.terraform_code;

            // Update security warnings
            displaySecurityWarnings(data.security_warnings);

            // Clear input
            document.getElementById('resource-name').value = '';
        } else {
            alert('❌ Failed to add resource: ' + (data.error || 'Unknown error'));
        }

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to add resource. Check console for details.');
    }
}

/**
 * Handle Enter key in textarea
 */
document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.getElementById('user-input');

    textarea.addEventListener('keydown', function (e) {
        // Ctrl/Cmd + Enter to generate
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            generateInfrastructure();
        }
    });

    // Add example text on load
    if (!textarea.value) {
        textarea.value = 'Create a VPC with public and private subnets. Deploy an EC2 instance in the public subnet and a PostgreSQL RDS database in the private subnet. Add a load balancer.';
    }
});

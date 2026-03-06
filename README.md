# Cloud Scanner Sentinel (AWS/LocalStack)

Cloud Scanner Sentinel is a cloud infrastructure security auditing tool designed to identify misconfigurations in AWS environments. The tool leverages the Boto3 library to interface with AWS APIs and automate the detection of common security vulnerabilities.

## Technical Capabilities
* **Network Analysis (EC2):** Detection of Security Groups with overly permissive ingress rules (0.0.0.0/0) on critical ports such as SSH (22).
* **Storage Analysis (S3):** Identification of S3 buckets with Access Control Lists (ACLs) configured for public read access.
* **Report Generation:** Automatic export of findings into a structured JSON format for integration with SOC workflows or visualization tools.

## System Requirements
* Docker and LocalStack (for cost-free AWS service simulation).
* Python 3.x.
* Python Virtual Environment (venv).

## Installation and Setup

1. Navigate to the project directory:
   ```bash
   cd ~/Escritorio/cloud-scanner



2. Configure the virtual environment and install dependencies:

python3 -m venv venv
source venv/bin/activate
pip install boto3 localstack

3. Start the LocalStack service in detached mode:

localstack start -d


<img width="842" height="389" alt="image" src="https://github.com/user-attachments/assets/0634e356-819b-4720-81bc-24f8aca71f87" />

<img width="479" height="130" alt="Captura desde 2026-03-06 14-17-10" src="https://github.com/user-attachments/assets/669d139a-a790-40bc-bee1-e272f7d61497" />


## Workflow

To properly test the security scanner, follow this two-step execution process:

### 1. Insecure Infrastructure Provisioning (Seed)
Before running the audit, you must populate the LocalStack environment with vulnerable resources. The `seed.py` script automates this by creating an open Security Group and a public S3 bucket:
```bash
python seed.py





Security Scan Execution
Once the "vulnerable seeds" are planted, execute the primary scanning engine. It will perform the audit, display alerts in the terminal, and generate the final report:

python Proyecto-scanner.py

##Report Structure
After execution, the tool generates a reporte_seguridad.json file. This allows for easy integration with other security tools (SIEM/SOAR). The structure is as follows:
<img width="871" height="186" alt="Captura desde 2026-03-06 14-13-44" src="https://github.com/user-attachments/assets/41890f51-2c49-41c9-b814-1fa2ef2ea209" />

Metadata: Scan timestamp and total findings count.

Findings: A detailed list of each security risk, including:

tipo: Resource category (Network/EC2 or Data/S3).

recurso: Name of the affected resource.

detalle/puerto: Technical specifics of the exposure.

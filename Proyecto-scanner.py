import boto3
import json
from datetime import datetime

def run_security_scan():
    print(f"\n\033[1;34m" + "="*50)
    print(f"   CLOUD SCANNER SENTINEL - {datetime.now().strftime('%H:%M:%S')}")
    print("="*50 + "\033[0m")
    
    # Sesión común para ambos servicios
    session_params = {
        'endpoint_url': 'http://localhost:4566',
        'region_name': 'us-east-1',
        'aws_access_key_id': 'test',
        'aws_secret_access_key': 'test'
    }

    findings = []

    # --- BLOQUE 1: ESCANEO DE RED (EC2) ---
    print("[*] Analyzing Firewalls (Security Groups)...")
    ec2 = boto3.client('ec2', **session_params)
    sgs = ec2.describe_security_groups()['SecurityGroups']
    for sg in sgs:
        for rule in sg.get('IpPermissions', []):
            for ip_range in rule.get('IpRanges', []):
                if ip_range.get('CidrIp') == '0.0.0.0/0':
                    print(f"\033[1;31m[!] RISK OF GRID: SG {sg['GroupName']} abierto al mundo.\033[0m")
                    findings.append({"tipo": "RED", "recurso": sg['GroupName'], "puerto": rule.get('FromPort')})

    # --- BLOQUE 2: ESCANEO DE DATOS (S3) ---
    print("[*] Analyzing storage (S3 Buckets)...")
    s3 = boto3.client('s3', **session_params)
    buckets = s3.list_buckets()['Buckets']
    for b in buckets:
        name = b['Name']
        acl = s3.get_bucket_acl(Bucket=name)
        for grant in acl['Grants']:
            if 'AllUsers' in str(grant['Grantee']):
                print(f"\033[1;31m[!] RISK OF DATA : Bucket '{name}' es PÚBLICO.\033[0m")
                findings.append({"tipo": "DATOS", "recurso": name, "detalle": "Acceso Público (ACL)"})

    # --- GENERACIÓN DEL REPORTE ---
    with open('reporte_seguridad.json', 'w') as f:
        json.dump({"metadata": {"fecha": str(datetime.now()), "total": len(findings)}, "hallazgos": findings}, f, indent=4)
    
    print(f"\n\033[1;32m[+] Escaneo completo. {len(findings)} fallos guardados en reporte_seguridad.json\033[0m")

if __name__ == "__main__":
    run_security_scan()
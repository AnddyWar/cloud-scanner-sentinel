import boto3

# Configuración para conectar con tu LocalStack
ENDPOINT_URL = "http://localhost:4566"

def create_insecure_infrastructure():
    # 1. PRIMERO: Creamos el cliente para poder hablar con AWS
    ec2 = boto3.client(
        'ec2', 
        endpoint_url=ENDPOINT_URL, 
        region_name='us-east-1',
        aws_access_key_id='testing',
        aws_secret_access_key='testing'
    )

    print("[*] Limpiando entorno previo...")
    try:
        # 2. SEGUNDO: Ahora sí podemos borrar porque 'ec2' ya existe
        ec2.delete_security_group(GroupName='SG-PELIGROSO-SOC')
        print("[+] Grupo antiguo eliminado.")
    except Exception:
        # Si no existe, no pasa nada, seguimos adelante
        pass

    print("[*] Creando Security Group vulnerable...")
    sg = ec2.create_security_group(
        GroupName='SG-PELIGROSO-SOC',
        Description='Este grupo tiene el puerto 22 abierto al mundo'
    )
    sg_id = sg['GroupId']

    # Abrir el puerto 22 (SSH) a TODO el internet (0.0.0.0/0)
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpProtocol='tcp',
        FromPort=22,
        ToPort=22,
        CidrIp='0.0.0.0/0'
    )
    
    print(f"[+ OK] Infraestructura creada. ID: {sg_id}")
    print("[!] El puerto 22 está abierto en 0.0.0.0/0. ¡Listo para ser escaneado!")

    # --- NUEVO: Módulo de S3 (Almacenamiento) ---
    s3 = boto3.client(
        's3', 
        endpoint_url=ENDPOINT_URL, 
        region_name='us-east-1',
        aws_access_key_id='testing',
        aws_secret_access_key='testing'
    )

    bucket_name = "datos-confidenciales-soc"
    
    # Limpieza de bucket si ya existe
    try:
        s3.delete_bucket(Bucket=bucket_name)
    except:
        pass

    print(f"[*] Creando Bucket de S3: {bucket_name}...")
    s3.create_bucket(Bucket=bucket_name)
    s3.put_bucket_acl(Bucket=bucket_name, ACL='public-read')
    print(f"[+ OK] Bucket {bucket_name} expuesto al público.")

if __name__ == "__main__":
    create_insecure_infrastructure()
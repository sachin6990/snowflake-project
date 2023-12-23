import sys
sys.path.append(r'D:\snowflake_project\retail-project\src\jobs\utils')

from vaultutil import VaultClient
from awsutil import AWSConnector

VAULT_URL = "http://127.0.0.1:8200"
ROLE_ID = "c306d891-f5e2-a3e7-24f6-e97bd019e48d"
SECRET_ID = "3a9da866-a3fd-308f-e7c8-3d1b15c32065"
SECRET_PATH = "secret/data/aws"

vault_client = VaultClient(VAULT_URL, ROLE_ID, SECRET_ID, SECRET_PATH)
token = vault_client.authenticate_with_approle()

if token:
    secret_data = vault_client.get_secret(token)
    if secret_data:
        aws_access_key = secret_data['data']['bw-aws-accesskey']
        aws_secret_key = secret_data['data']['bw-aws-secretkey']
        print("Secret data:", secret_data)
    else:
        print("Failed to retrieve secret.")
else:
    print("Failed to authenticate with AppRole.")

region = 'us-east-1'  # Replace with your preferred AWS region
aws_connector = AWSConnector(aws_access_key, aws_secret_key, 'iam', region)

# Access the IAM client through the instance
iam_client = aws_connector.aws_client_conn

# Now you can use iam_client to perform IAM operations
response = iam_client.list_groups()

print("IAM groups:", response)
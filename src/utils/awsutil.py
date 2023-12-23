import boto3
from vaultutil import VaultClient

VAULT_URL = "http://127.0.0.1:8200"
ROLE_ID = "c306d891-f5e2-a3e7-24f6-e97bd019e48d"
SECRET_ID = "3a9da866-a3fd-308f-e7c8-3d1b15c32065"
SECRET_PATH = "secret/data/snow"

vault_client = VaultClient(VAULT_URL, ROLE_ID, SECRET_ID, "secret/data/aws")  # Update the secret path
token = vault_client.authenticate_with_approle()

if token:
    secret_data = vault_client.get_secret(token)
    if secret_data:
        print("Secret data:", secret_data)

        # Ensure that the key is present in the secret_data dictionary
        aws_access_key = secret_data['data'].get('bw-aws-accesskey')
        aws_secret_key = secret_data['data'].get('bw-aws-secretkey')

        if aws_access_key and aws_secret_key:
            region = 'us-east-1'  # Replace with your preferred AWS region

            class AWSConnector:
                def __init__(self, aws_access_key, aws_secret_key, client='s3', region='us-east-1'):
                    self.aws_access_key = aws_access_key
                    self.aws_secret_key = aws_secret_key
                    self.region = region
                    self.aws_client = client
                    self.session = self.create_session()
                    self.aws_client_conn = self.create_aws_client()

                def create_session(self):
                    """
                    Create an AWS session using the provided credentials and region.
                    """
                    session = boto3.Session(
                        aws_access_key_id=self.aws_access_key,
                        aws_secret_access_key=self.aws_secret_key,
                        region_name=self.region
                    )
                    return session

                def create_aws_client(self):
                    """
                    Create an AWS client using the AWS session.
                    """
                    aws_client_conn = self.session.client(self.aws_client)
                    return aws_client_conn

            # Create an instance of the AWSConnector class
            aws_connector = AWSConnector(aws_access_key, aws_secret_key, client='s3', region=region)

            # Access the S3 client through the instance
            s3_client = aws_connector.aws_client_conn

            # Now you can use s3_client to perform S3 operations
            response = s3_client.list_buckets()
            print("S3 Buckets:")
            for bucket in response['Buckets']:
                print(f"  {bucket['Name']}")
        else:
            print("AWS credentials not found in secret data.")
    else:
        print("Failed to retrieve secret.")
else:
    print("Failed to authenticate with AppRole.")
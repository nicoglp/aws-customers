import os

LOCAL_DYNAMO = 'http://docker.for.mac.localhost:8000' if 'AWS_SAM_LOCAL' in os.environ else 'http://localhost:8000'
DYNAMODB_URL = os.getenv('DYNAMODB_URL', LOCAL_DYNAMO)
USER_TABLENAME = os.getenv('TABLE', 'Users')
REGION = os.getenv('REGION', 'us-east-2')
DEBUG_LEVEL = os.getenv('DEBUG_LEVEL', 10)  # 10 = DEBUG

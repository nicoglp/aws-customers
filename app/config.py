import os

LOCAL_DYNAMODB_URL = 'http://docker.for.mac.localhost:8000' if 'AWS_SAM_LOCAL' in os.environ else 'http://localhost:8000'

ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')
REGION = os.getenv('REGION', 'us-east-2')
TABLENAME = os.getenv('TABLE', 'Users')
LOGLEVEL = os.getenv('LOGLEVEL', 'DEBUG')  # 10 = DEBUG




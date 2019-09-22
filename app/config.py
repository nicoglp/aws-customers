import os

LOCAL_DYNAMODB_URL = 'http://docker.for.mac.localhost:8000' if 'AWS_SAM_LOCAL' in os.environ else 'http://localhost:8000'
#SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:@172.17.0.2:5432/postgres'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@database-2.ci7oifiiqx7r.us-east-2.rds.amazonaws.com:5432/gentem'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')
REGION = os.getenv('REGION', 'us-east-2')
USERTABLENAME = os.getenv('USERTABLE', 'Users')
LOGLEVEL = os.getenv('LOGLEVEL', 'DEBUG')  # 10 = DEBUG

INGEST_DATE_FORMAT = os.getenv('INGEST_DATE_FORMAT', '%m/%d/%y')
INGEST_CSV_DELIMITER = os.getenv('INGEST_CSV_DELIMITER', ';')

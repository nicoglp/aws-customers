import csv
import json
import urllib.parse

import boto3
from marshmallow import ValidationError, fields

from app import logger, config
from app.users import UserSchema, dao


class IngestSchema(UserSchema):
    "Custom User schema ingestion"

    # Custom date format for Date of Birth
    dob = fields.Date(format=config.INGEST_DATE_FORMAT)


ingestion_schema = IngestSchema()
s3 = boto3.client('s3')


def ingest_users(event, context):
    # TODO : Validate event structure

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    logger.info(f'Ingesting Users from file {key}')

    s3_object = _get_s3_object(bucket, key)

    if s3_object:
        lines = s3_object['Body'].read().splitlines(True)
        users, errors = _create_users(lines)
        _persist_users(users)

        logger.info(f'Ingestion process finished. User created = {len(users)} - With Errors = {len(errors)}')


def _get_s3_object(bucket, key):
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return response
    except Exception as e:
        logger.error(
            f'Error getting object {key} from bucket {bucket}. '
            f'Make sure they exist and your bucket is in the same region as this function.')
        return None


def _persist_users(users):
    dao.save_all(users)


def _create_users(iterable):
    users = []
    with_errors = []

    dialect = csv.Sniffer().sniff(iterable.read(1024))
    iterable.seek(0)

    fieldnames = ["firstName", "lastName", "email", "dob", "address"]

    csv_reader = csv.DictReader(iterable, dialect=dialect, fieldnames=fieldnames)
    csv_reader.__next__()  # Omit headers

    for row in csv_reader:
        try:
            users.append(ingestion_schema.load(row))
        except ValidationError as validation:
            with_errors.append(row)
            logger.error(f"Error ingesting user with data {json.dumps(row)}")
            logger.error(f'Field errors: {json.dumps(validation.messages)}')

    return users, with_errors

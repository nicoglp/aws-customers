from . import logger

from .base import exception
from .users import service


def post(event, context):
    logger.info('HTTP POST Method execution')

    if not (event.get("httpMethod") == 'POST' and event['body']):
        raise exception.ServiceException("Bad request")
    else:
        result_json, result_status = service.create(event['body'])

    return dict(
        statusCode=result_status,
        body=result_json
    )


def get(event, context):
    logger.info('HTTP GET Method execution')

    if not (event.get("httpMethod") == 'GET' and event.get('pathParameters', {}).get('id')):
        result_json, result_status = dict(message="Bad request"), 500
    else:
        result_json, result_status = service.retrieve(event['pathParameters']['id'])

    return dict(
        statusCode=result_status,
        body=result_json
    )


def put(event, context):
    logger.info('HTTP PUT Method execution')

    if not (event.get("httpMethod") == 'PUT' and event.get('pathParameters', {}).get('id')):
        result_json, result_status = dict(message="Bad request"), 500
    else:
        result_json, result_status = "{'message' : 'Not implemented yet !'}", 500

    return dict(
        statusCode=result_status,
        body=result_json
    )


def delete(event, context):
    logger.info('HTTP DELETE Method execution')

    if not (event.get("httpMethod") == 'DELETE' and event.get('pathParameters', {}).get('id')):
        result_json, result_status = dict(message="Bad request"), 500
    else:
        result_json, result_status = service.delete(event['pathParameters']['id'])

    return dict(
        statusCode=result_status,
        body=result_json
    )

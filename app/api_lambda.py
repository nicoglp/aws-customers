from . import logger

from .base import exception
from .users import service as user_service
from .claims import service as claims_service
from .provider import service as provider_service
from .profile import service as profile_service
from .service_line import service as service_line_service


def post(event, context, service):
    logger.info('HTTP POST Method execution')

    if not (event.get("httpMethod") == 'POST' and event['body']):
        raise exception.ServiceException("Bad request")
    else:
        result_json, result_status = service.create(event['body']), 201

    return dict(
        statusCode=result_status,
        body=result_json
    )


def get(event, context, service):
    logger.info('HTTP GET Method execution')

    if not (event.get("httpMethod") == 'GET' and event.get('pathParameters', {}).get('id')):
        result_json, result_status = dict(message="Bad request"), 500
    else:
        result_json, result_status = service.retrieve(event['pathParameters']['id']), 200

    return dict(
        statusCode=result_status,
        body=result_json
    )


def delete(event, context, service):
    logger.info('HTTP DELETE Method execution')

    if not (event.get("httpMethod") == 'DELETE' and event.get('pathParameters', {}).get('id')):
        result_json, result_status = dict(message="Bad request"), 500
    else:
        result_json, result_status = service.delete(event['pathParameters']['id']), 200

    return dict(
        statusCode=result_status,
        body=result_json
    )


def put(event, context, service):
    logger.info('HTTP PUT Method execution')

    if not (event.get("httpMethod") == 'PUT' and event.get('pathParameters', {}).get('id')):
        result_json, result_status = dict(message="Bad request"), 500
    else:
        result_json, result_status = "{'message' : 'Not implemented yet !'}", 500

    return dict(
        statusCode=result_status,
        body=result_json
    )


def list(event, context, service):
    logger.info('HTTP GET Method execution')

    if not event.get("httpMethod") == 'GET':
        result_json, result_status = dict(message="Bad request"), 500
    else:
        result_json, result_status = service.list(), 200

    return dict(
        statusCode=result_status,
        body=result_json
    )


def post_user(event, context):
    return post(event, context, user_service)


def get_user(event, context):
    return get(event, context, user_service)


def delete_user(event, context):
    return delete(event, context, user_service)


def put_user(event, context):
    return put(event, context, user_service)


def list_user(event, context):
    return list(event, context, user_service)


def post_claim(event, context):
    return post(event, context, claims_service)


def get_claim(event, context):
    return get(event, context, claims_service)


def list_claim(event, context):
    return list(event, context, claims_service)


def post_provider(event, context):
    return post(event, context, provider_service)


def get_provider(event, context):
    return get(event, context, provider_service)


def list_provider(event, context):
    return list(event, context, provider_service)


def post_profile(event, context):
    return post(event, context, profile_service)


def get_profile(event, context):
    return get(event, context, profile_service)


def list_profile(event, context):
    return list(event, context, profile_service)


def get_service_line(event, context):
    return get(event, context, service_line_service)


def list_service_line(event, context):
    return list(event, context, service_line_service)

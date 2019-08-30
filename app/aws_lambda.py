from . import logger
from .users import service


def handler(event, context):
    method = event['httpMethod']
    logger.debug('HTTP Method {}'.format(method))

    result_json, result_status = None, None
    if method == 'POST':
        json_body = event['body']
        logger.debug('Creating entity with with values {}'.format(json_body))
        result_json, result_status = service.create(json_body)
    elif method == 'GET':
        entity_id = event['pathParameters']['id']
        logger.debug('Retrieving entity with id {}'.format(entity_id))
        result_json, result_status = service.retrieve(entity_id)

    return dict(
        statusCode=result_status,
        body=result_json
    )

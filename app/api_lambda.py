from . import logger

from .base import exception


class AWSLambda():

    def __init__(self, service):
        self.service = service

    def post(self, event, context):
        logger.info('HTTP POST Method execution')

        if not (event.get("httpMethod") == 'POST' and event['body']):
            raise exception.ServiceException("Bad request")
        else:
            result_json, result_status = self.service.create(event['body']), 201

        return dict(
            statusCode=result_status,
            body=result_json
        )


    def get(self, event, context):
        logger.info('HTTP GET Method execution')

        if not (event.get("httpMethod") == 'GET' and event.get('pathParameters', {}).get('id')):
            result_json, result_status = dict(message="Bad request"), 500
        else:
            result_json, result_status = self.service.retrieve(event['pathParameters']['id']), 200

        return dict(
            statusCode=result_status,
            body=result_json
        )


    def delete(self, event, context):
        logger.info('HTTP DELETE Method execution')

        if not (event.get("httpMethod") == 'DELETE' and event.get('pathParameters', {}).get('id')):
            result_json, result_status = dict(message="Bad request"), 500
        else:
            result_json, result_status = self.service.delete(event['pathParameters']['id']), 200

        return dict(
            statusCode=result_status,
            body=result_json
        )


    def put(self, event, context):
        logger.info('HTTP PUT Method execution')

        if not (event.get("httpMethod") == 'PUT' and event.get('pathParameters', {}).get('id')):
            result_json, result_status = dict(message="Bad request"), 500
        else:
            result_json, result_status = "{'message' : 'Not implemented yet !'}", 500

        return dict(
            statusCode=result_status,
            body=result_json
        )


    def list(self, event, context):
        logger.info('HTTP GET Method execution')

        if not event.get("httpMethod") == 'GET':
            result_json, result_status = dict(message="Bad request"), 500
        else:
            result_json, result_status = self.service.list(), 200

        return dict(
            statusCode=result_status,
            body=result_json
        )

"""
"""

import logging
import uuid
from datetime import datetime

import boto3

from .. import config
from ..base import model

log = logging.getLogger('DynamoDAO')


class DynamoDAO:
    """
    DynamoDB Data Access Object (aka Repository) used to manage the persistence of a Domain Model Entities using a
    unified interface that defines the basics CRUD operations (create, retrieve, update).

    This implementation use `Boto 3<https://boto3.amazonaws.com/v1/documentation/api/latest/index.html>`_, the  (AWS)
    SDK for Python ot access DynamoDB resources.
    """

    def __init__(self, table_name, storage_schema, key_name='id'):
        '''
        Create a Repository to manage persistence using the specified Table, schema and key attribute that make up the
         primary key for the table.
        :param table_name: Name of the DynamoDB table
        :param storage_schema: Storage schema
        :param key_name:
        '''
        super(DynamoDAO, self).__init__()
        self.schema = storage_schema
        if 'dev' == config.ENVIRONMENT:
            self.db = boto3.resource('dynamodb', endpoint_url=config.LOCAL_DYNAMODN_URL)
        else:
            self.db = boto3.resource('dynamodb')
        self.table_name = table_name
        self.table = self.db.Table(table_name)
        self.key_name = key_name

    def retrieve(self, key_value):
        retrieve_params = {
            self.key_name: str(key_value)
        }
        log.debug('get_item params %s', retrieve_params)
        result = self.table.get_item(Key=retrieve_params)

        return self.schema.load(result['Item'])

    def create(self, entity):
        entity.id = uuid.uuid1()

        timestamp = datetime.utcnow().timestamp()
        entity.created_at = timestamp
        entity.updated_at = timestamp

        document = self.schema.dump(entity)
        result = self.table.put_item(Item=document)

        return entity

    def delete(self, key_value):
        delete_params = {
            self.key_name: str(key_value)
        }
        log.debug('delete_item params %s', delete_params)

        self.table.delete_item(Key=delete_params)

    def find_all(self):
        result = self.table.scan()

        entities = self.schema.load(result['Items'], many=True)

        return model.Pagination(1, result['ScannedCount'], result['ScannedCount'], entities)

    def update(self, entity):

        entity.updated_at = datetime.utcnow().timestamp()

        document = self.schema.dump(entity)
        update_params = self._update_params(document, [self.key_name])
        log.debug('update_item params %s', update_params)

        result = self.table.update_item(**update_params)

        return entity

    def _update_params(self, attrs, ignore=None):
        '''
        Generate the upgrade sentence based on the properties sent as parameters
        :param attrs - dic with all the attributes to update
        :param ignore - collection of attributes to ignore
        '''

        ignore = ignore or []
        updates = []
        params = dict(
            Key={
                self.key_name: str(attrs[self.key_name])
            },
            ExpressionAttributeNames={},
            ExpressionAttributeValues={},
            UpdateExpression="SET ",
            ReturnValues='ALL_NEW',
        )
        for attr, value in attrs.items():
            if attr not in ignore:
                name_key = "#{}".format(attr)
                value_key = ":{}".format(attr)
                params['ExpressionAttributeNames'][name_key] = attr
                params['ExpressionAttributeValues'][value_key] = value
                updates.append("{} = {}".format(name_key, value_key))
        params['UpdateExpression'] += ','.join(updates)

        return params

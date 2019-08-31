import boto3

from app import users_ingestion
from test import UserTestCase


class UserIngestionTestCase(UserTestCase):

    def setUp(self):
        super(UserIngestionTestCase, self).setUp()

    def test_create_users(self):

        with open('sample-csv-file.csv', newline='') as csvfile:
            users, errors = users_ingestion._create_users(csvfile)
            self.assertEqual(len(users), 2)

    def test_read_from_s3(self):
        boto3.resource('s3')

        response = users_ingestion._get_s3_object('gentem-bucket', 'csvs/sample-csv-file.csv')
        self.assertIsNotNone(response)

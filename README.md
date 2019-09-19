# Gentem Customer's Admin
Serverless web application to store an Organization’s customer information. 

The application will accept a list of customers in a CSV file, parse the CSV file, and save the data in the database. Then all customer's uploaded will be listed allowing the user to update the customer's information.

**Requirements**
* Ingest CSV file with the format |first_name| , |last_name|, |email|, , |date_of_birth|, |Address|
* Static files of UI will be hosted on the cloud (Deployment could be done using Elastic beanstalk or Heroku)
* Lambda functions will be written in Python


## Backend implementation

### RESTFull API - Lambda functions written in Python

The backend API was implemented as an AWS Lambda function, which manages a resource called *Users* following the REST specification.

In order to give a basic structure to facilitate the system maintainability, the Lambda function was designed following this basic concept linked to the Domain-Driven Design patterns.

* _Repositories_ ( aka _Data Access Object_ or _DAOs_ ): Repository abstraction for the underlying storage systems. A specific _DynamoDB_ DAO was implemented for this project.
* _Domain Model_: A *User* domain model was introduced to implement all the domain logic needed in this context.
* _Services (or Business Object)_ * : This layer is where all the business rules should be implemented, and also architectural concepts like transaction management.

*Note* :  [Marshmallow](https://marshmallow.readthedocs.io/en/stable/index.html) is used for schema definitions and validation.

### CSV Ingestion

TODO

## Development Environment

### Requirements
To start working with AWS Lambdas, next tools al required: 

* AWS CLI already configured with Administrator permission
* [AWS SAM CLI](https://docs.aws.amazon.com/en_pv/serverless-application-model/latest/developerguide/serverless-sam-cli-install-mac.html) 
* [Python 3 installed](https://www.python.org/downloads/)
* [Docker installed](https://www.docker.com/community-edition)
* [AWS Toolkit for JetBrains](https://docs.aws.amazon.com/en_pv/toolkit-for-jetbrains/latest/userguide/key-tasks.html)

### Set Up Project 

Then, in order to set up a development environment and work with the project,  we should follow the next steps.

* Clone the sourcecode from GitHub  
```shell script
$ git clone https://github.com/nicoglp/gentem-customers.git    
$ cd gentem-customers
```

* Create Virtual Environment
```shell script
$ python3 -m venv venv
$ . venv/bin/activate
```
* Install dependencies
```shell script
$ pip install -r requirements.txt
```
* Setup Local DynamoDB (using Docker)
```shell script
$ docker run -p 8000:8000 amazon/dynamodb-local`
```

* Create DynamoDB `Users` Table
```shell script
$ aws dynamodb create-table \
    --table-name Users \
    --attribute-definitions \
        AttributeName=email,AttributeType=S \
    --key-schema \
        AttributeName=email,KeyType=HASH \
    --provisioned-throughput \
        ReadCapacityUnits=1,WriteCapacityUnits=1 \
    --endpoint-url http://localhost:8000
```

### Build and test

Once the python project and the DynamoDB are configured, we can test the API using the next approaches:

**Invoking function locally using a local sample payload**
```shell script
$ sam local invoke UsersFunction --event events/get_event.json
```

**Invoking function locally through local API Gateway**

```shell script
$ sam local start-api
```
If the previous command ran successfully you should now be able to hit the following local endpoints

_Create a new User_
```shell script
$ curl -X POST \
  http://127.0.0.1:3000/users \
  -H 'content-type: application/json' \
  -d '{
	"firstName" : "Jon",
	"lastName":"Doe",
	"email":"jon.doe@gmail.com",
	"dob":"1980-10-14",
	"address":"1 glove drive , san francisco 94103, CA"
}'
```

_Get previous user_
```shell script
$ curl -X GET http://127.0.0.1:3000/users/jon.doe@gmail.com
```

## Packaging and deployment

AWS Lambda Python runtime requires a flat folder with all dependencies including the application. SAM will use `CodeUri`
 property to know where to look up for both application and dependencies:

```yaml
...
    HelloWorldFunction:
        Type: AWS::Serverless::Function
        Properties:
            CodeUri: .
            ...
```

We need a `S3 bucket` where we can upload our Lambda functions packaged as ZIP before we deploy anything.
If you don't have a S3 bucket to store code artifacts then this is a good time to create one:

```
# Example regions: us-east-1, ap-east-1, eu-central-1, sa-east-1
aws s3 mb s3://bucketname --region region  
```

I've created one to use for to deploy the current project.

**_nicoglp-artifacts_**


Next, run the following command to package our Lambda function to S3:

```bash
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket nicoglp-artifacts
```

Next, the following command will create a Cloudformation Stack and deploy your SAM resources.

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name users-api \
    --capabilities CAPABILITY_IAM
```

After deployment is complete you can run the following command to retrieve the API Gateway Endpoint URL:

```bash
aws cloudformation describe-stacks \
    --stack-name users-api \
    --query 'Stacks[].Outputs[?OutputKey==`UsersApi`]' \
    --output table
``` 

> **See [Serverless Application Model (SAM) HOWTO Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-quick-start.html) for more details in how to get started.**

## Last Production Endpoints

Last production endpoints !!

 _POST /users : Create new User_
 ```shell script
$ curl -X POST \
  https://f8lkr3u8u5.execute-api.us-east-2.amazonaws.com/Prod/users \
  -H 'content-type: application/json' \
  -d '{
	"firstName" : "Jon",
	"lastName":"Doe",
	"email":"jon.doe@gmail.com",
	"dob":"1980-10-14",
	"address":"1 glove drive , san francisco 94103, CA"
}'
```

_GET /users/{id} : Get user with {id}_
```shell script
$ curl -X GET https://f8lkr3u8u5.execute-api.us-east-2.amazonaws.com/Prod/users/jon.doe@gmail.com
```

_DELETE /users/{id} : Delete user with {id}_
```shell script
$ curl -X  https://f8lkr3u8u5.execute-api.us-east-2.amazonaws.com/Prod/users/jon.doe@gmail.com
```

_GET /users : List of users_
```shell script
$ curl -X GET https://f8lkr3u8u5.execute-api.us-east-2.amazonaws.com/Prod/users
```


## Cleanup

In order to delete our Serverless Application recently deployed you can use the following AWS CLI Command:

```shell script
$ aws cloudformation delete-stack --stack-name users-api
```

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

 _POST /claims : Create new Claim_
 _First we need to create the billing provider, rendering provider, referring provider, patient and insured (if necessary)_

 _POST /providers : Create new Billing Provider_
 ```shell script
$ curl -X POST https://q1il74s1xa.execute-api.us-east-2.amazonaws.com/Prod/providers \
    -H 'content-type: application/json' \
    -d '{ "name":"Gentem",
        "address":"303 YOUNGLOVE AVE, san francisco 94103, CA",
        "npi":"1568412344",
        "type":"billing_provider",
        "phone":"424-248-7725"
}'
```

 _POST /providers : Create new Rendering Provider_
 ```shell script
$ curl -X POST https://q1il74s1xa.execute-api.us-east-2.amazonaws.com/Prod/providers \
    -H 'content-type: application/json' \
    -d '{ "name":"Saint Francis Memorial Hospital",
        "address":"2900 Hyde St Lower Nob Hill, san francisco 94103, CA",
        "npi":"1316061998",
        "type":"rendering_provider"
}'
```

 _POST /providers : Create new Referring Provider_
 ```shell script
$ curl -X POST https://q1il74s1xa.execute-api.us-east-2.amazonaws.com/Prod/providers \
    -H 'content-type: application/json' \
    -d '{"name":"John Lin",
        "npi":"1568412347",
        "type":"referring_provider"
}'
```

 _POST /profiles : Create new Patient_
 ```shell script
$ curl -X POST https://q1il74s1xa.execute-api.us-east-2.amazonaws.com/Prod/profiles \
    -H 'content-type: application/json' \
    -d '{ "email":"susan.doe1@gmail.com",
        "lastName":"Doe",
        "gender":"Female",
        "firstName":"Susan",
        "address":"1 glove drive , san francisco 94103, CA",
        "memberId":"ABC100286987",
        "phone":"415 1234567",
        "dob":"2015-10-19"
}'
```

 _POST /profiles : Create new Insured_
 ```shell script
$ curl -X POST https://q1il74s1xa.execute-api.us-east-2.amazonaws.com/Prod/profiles \
    -H 'content-type: application/json' \
    -d '{ "email":"jon.doe1@gmail.com",
        "lastName":"Doe",
        "gender":"Male",
        "firstName":"Jon",
        "address":"1 glove drive , san francisco 94103, CA",
        "memberId":"ABC100286987",
        "phone":"415 1234567",
        "middleInitial":"P",
        "dob":"1981-06-24"
}'
```
 _To create the claim we need those ids created_
 _Glosary with claim columns: https://docs.google.com/document/d/1q7WokZnkXgHTZsC3V3cR43_eaK6nixqnJQ_mSnXSCW4/edit_
  ```shell script
$ curl -X POST https://q1il74s1xa.execute-api.us-east-2.amazonaws.com/Prod/claims \
    -H 'content-type: application/json' \
    -d '{
        "patientAccountNumber": "1234567",
        "totalCharge": 200.50,
        "amountPaid": 0,
        "insuranceName": "blue_shield_ca",
        "insuredId": "f576dab6-e38d-11e9-9ee5-0addcae3daec",
        "patientId": "fe8e6a88-e38d-11e9-9ee6-0addcae3daec",
        "referringProviderId": "09f16a6a-e38e-11e9-8e5b-0addcae3daec",
        "billingProviderId": "13c3f882-e38e-11e9-8e5c-0addcae3daec",
        "billingProviderTaxId": "HE567W65489A",
        "renderingProviderId": "1beee0e4-e38e-11e9-8e5d-0addcae3daec",
        "insuredPolicyGroup": "Z9364859",
        "insurancePlanName": "IFP ON EXCHANGE",
        "priorAuthorizationNumber": "63B4295825",
        "physicianSupplierSignature": "Signature on File",
        "physicianSupplierSignatureDate": "2019-09-29",
        "illnessDate": "2019-09-26",
        "similarSymptomDate": "2019-08-20",
        "unableToWorkFrom": "2019-09-26",
        "unableToWorkTo": "2019-10-26",
        "hospitalAdmitDate": "2019-09-26",
        "hospitalDischargeDate": "2019-10-15",
        "additionalClaimInformation": "",
        "insuranceType": "OTHER",
        "patientCondition": "Other Accident",
        "patientSignatureDate": "2019-09-29",
        "patientSignature": "Signature on File",
        "insuredSignature": "Signature on File",
        "patientRelation": "CHILD",
        "otherInsuredName": "Mcintire, Ashley L",
        "otherInsuredPolicyGroup": "115",
        "otherInsuredCompanyName": "UHC",
        "anotherHealthBenefitPlan": "true",
        "claimState": {"state": "Created"},
        "serviceLines": [{
                        "procedureCode": 87653,
                        "charges": 100.40,
                        "units": 1,
                        "modifiers": [],
                        "diagnosisCodes": ["N949"],
                        "serviceDateFrom": "2019-09-29",
                        "serviceDateTo": "2019-09-29",
                        "placeOfService": "21",
                        "emergencyIndicator": "false"
                        },
                        {"procedureCode":87798,
                        "charges":20.02,
                        "units":5,
                        "modifiers":["49"],
                        "diagnosisCodes":["Z7251"],
                        "serviceDateFrom":"2019-09-29",
                        "serviceDateTo":"2019-09-29",
                        "placeOfService":"21",
                        "emergencyIndicator":"false"
                        }]
        }'
```

_GET /claims/{id} : Get claim with {id}_
```shell script
$ curl -X GET https://q1il74s1xa.execute-api.us-east-2.amazonaws.com/Prod/claims/80866180-e38e-11e9-929c-0addcae3daec
```

_GET /claims : List of claims_
```shell script
$ curl -X GET https://q1il74s1xa.execute-api.us-east-2.amazonaws.com/Prod/claims
```

_GET /providers/{id} : Get provider with {id}_
```shell script
$ curl -X GET https://q1il74s1xa.execute-api.us-east-2.amazonaws.com/Prod/providers/09f16a6a-e38e-11e9-8e5b-0addcae3daec
```

_GET /providers : List of providers_
```shell script
$ curl -X GET https://q1il74s1xa.execute-api.us-east-2.amazonaws.com/Prod/providers
```

_GET /profiles/{id} : Get profile with {id}_
```shell script
$ curl -X GET https://q1il74s1xa.execute-api.us-east-2.amazonaws.com/Prod/profiles/f576dab6-e38d-11e9-9ee5-0addcae3daec
```

_GET /profiles : List of profiles_
```shell script
$ curl -X GET https://q1il74s1xa.execute-api.us-east-2.amazonaws.com/Prod/profiles
```

## Cleanup

In order to delete our Serverless Application recently deployed you can use the following AWS CLI Command:

```shell script
$ aws cloudformation delete-stack --stack-name users-api
```

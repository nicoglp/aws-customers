#!/bin/bash

# Build
sam build

# Package
sam package --output-template-file packaged.yaml --s3-bucket nicoglp-artifacts

# Deploy
sam deploy --template-file packaged.yaml --stack-name users-api --capabilities CAPABILITY_IAM

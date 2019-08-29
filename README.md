# Gentem Customer's Admin
Serverless web application to store an Organization’s customer information. 

The application will accept a list of customers in a CSV file, parse the CSV file, and save the data in the database. Then all customer's uploaded will be listed allowing the user to update the customer's information.

**Requirements**
* Ingest CSV file with the format |first_name| , |last_name|, |email|, , |date_of_birth|, |Address|
* Static files of UI will be hosted on the cloud (Deployment could be done using Elastic beanstalk or Heroku)
* Lambda functions will be written in Python

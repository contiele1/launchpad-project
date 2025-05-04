# Streaming Data Project

## Description
An application to retrieve articles from the [Guardian API](https://open-platform.theguardian.com/) and publish it to
an instance of AWS SQS queue so that it can be consumed and analysed by other applications.

It accepts a key for the Guardian API, a search term (e.g. "machine learning"), an optional "date_from" field, and the name of an SQS queue. It will use the search terms to search for articles in the Guardian API and will then post details of up to ten hits to the SQS.

For example, given the inputs:
- "test"
- "machine learning" 
- "date_from=2023-01-01"
- "guardian_content"

it will retrieve all content returned by the API (called with the key "test") and send up to the ten most recent items in JSON format to the SQS named "guardian_content". The messages will have the following format:

```json
{
    "webPublicationDate": "2023-11-21T11:11:31Z",
    "webTitle": "Who said what: using machine learning to correctly attribute quotes",
    "webUrl": "https://www.theguardian.com/info/2023/nov/21/who-said-what-using-machine-learning-to-correctly-attribute-quotes"
}
```
This application is intended to be deployed as a component in a data platform on AWS. However, it can also be invoked from the command line (see below).
The terraform folder contains the modules to provision the infrastucture on AWS, including a standard SQS called "guardian_content".

## Prerequisites
1. An AWS account.
2. Terraform (Optional)


## Setup
1. Run `make requirements` to install the modules listed in requirements.txt and create the dependencies for the lambda layer. Alternatively, running `make all` will also run the security checks and the unit tests.
2. Running Terraform on the modules in the terraform folder will deploy the Lambda and and an SQS called 'guardian_content' in your AWS account (the region is set to eu-west-2).
3. To use the app locally, save your Guardian API key in an `.env` file as: 
```.env
API-KEY=<your-guardian-key>
```

## Usage
- To invoke the application from the command line:
```bash
python local.py
```
It will retrieve your api key from the .env file.
- Once deployed, the lambda can be triggered via the AWS CLI or the AWS console with an event with this format:
```json
{
    "content": "your content",
    "api_key": "your api key,
    "date": "your date",
    "sqs_name": "your sqs name"
}
```
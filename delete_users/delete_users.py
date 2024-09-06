import os
import boto3


dynamodb_params = {}
if os.getenv("IS_OFFLINE"):
    dynamodb_params = {
        "region_name": "localhost",
        "endpoint_url": "http://localhost:8000",
    }

dynamodb = boto3.resource("dynamodb", **dynamodb_params)                              
table = dynamodb.Table(os.getenv("TABLE_NAME"))


def handler(event, context):
    # generate and add id
    user_id = event["pathParameters"]["id"]

    table.delete_item(Key={"pk": user_id})

    return {"statusCode": 204}

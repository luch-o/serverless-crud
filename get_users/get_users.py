import os
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb_params = {}
if os.getenv("IS_OFFLINE", False):
    dynamodb_params = {
        "region_name": "localhost",
        "endpoint_url": "http://localhost:8000",
    }

dynamodb = boto3.resource("dynamodb", **dynamodb_params)                              
table = dynamodb.Table("users-table")


def handler(event, context):
    user_id = event["pathParameters"]["id"]
    print(f"{dynamodb_params=}")
    response = table.query(KeyConditionExpression=Key("pk").eq(user_id))
    user = response["Items"][0] if response["Items"] else {}

    return {"statusCode": 200, "body": json.dumps({"user": user})}

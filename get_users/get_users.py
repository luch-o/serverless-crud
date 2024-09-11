import os
import json
import boto3
from utils.utils import decimal_serializer, dynamodb_params
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource("dynamodb", **dynamodb_params)                              
table = dynamodb.Table(os.getenv("TABLE_NAME"))


def handler(event, context):
    user_id = event["pathParameters"]["id"]

    response = table.query(KeyConditionExpression=Key("pk").eq(user_id))
    user = response["Items"][0] if response.get("Items") else {}

    return {
        "statusCode": 200 if user else 404,
        "body": json.dumps({"user": user}, default=decimal_serializer) if user else None
    }

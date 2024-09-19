import os
import json
import boto3
from utils.utils import dynamodb_params

dynamodb = boto3.resource("dynamodb", **dynamodb_params)                              
table = dynamodb.Table(os.getenv("TABLE_NAME"))

def handler(event, context):
    body = json.loads(event["Records"][0]["body"])
    user_id = body["id"]
    print(user_id)

    response = table.update_item(
        Key={
            "pk": user_id
        },
        UpdateExpression="ADD likes :inc",
        ExpressionAttributeValues={
            ":inc": 1
        },
        ReturnValues="ALL_NEW",
    )

    print(response)

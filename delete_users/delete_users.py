import os
import boto3
from utils.utils import dynamodb_params

dynamodb = boto3.resource("dynamodb", **dynamodb_params)                              
table = dynamodb.Table(os.getenv("TABLE_NAME"))


def handler(event, context):
    # generate and add id
    user_id = event["pathParameters"]["id"]

    table.delete_item(Key={"pk": user_id})

    return {"statusCode": 204}

import os
import json
import uuid
import boto3
from utils.utils import  dynamodb_params


dynamodb = boto3.resource("dynamodb", **dynamodb_params)                              
table = dynamodb.Table(os.getenv("TABLE_NAME"))


def handler(event, context):
    # generate and add id
    user_id = uuid.uuid4()
    body = json.loads(event["body"]) if "body" in event else {}
    user = body | {"pk": str(user_id)}

    table.put_item(Item=user)

    return {"statusCode": 201, "body": json.dumps(user)}

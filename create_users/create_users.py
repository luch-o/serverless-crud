import os
import json
import uuid
import boto3


dynamodb_params = {}
if os.getenv("IS_OFFLINE"):
    dynamodb_params = {
        "region_name": "localhost",
        "endpoint_url": "http://0.0.0.0:8000",
        "aws_access_key_id": "DEFAULT_ACCESS_KEY",
        "aws_secret_access_key": "DEFAULT_SECRET", 
    }

dynamodb = boto3.resource("dynamodb", **dynamodb_params)                              
table = dynamodb.Table("users-table")


def handler(event, context):
    # generate and add id
    user_id = uuid.uuid4()
    body = json.loads(event["body"]) if "body" in event else {}
    user = body | {"pk": str(user_id)}

    print(f"{dynamodb_params=}")
    table.put_item(Item=user)

    return {"statusCode": 200, "body": json.dumps(user)}

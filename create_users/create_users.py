import os
import json
import uuid
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
    user_id = uuid.uuid4()
    body = json.loads(event["body"]) if "body" in event else {}
    user = body | {"pk": str(user_id)}

    print(f"{dynamodb_params=}")
    table.put_item(Item=user)

    return {"statusCode": 201, "body": json.dumps(user)}

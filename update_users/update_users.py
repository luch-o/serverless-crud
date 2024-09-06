import os
import json
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
    user_id = user_id = event["pathParameters"]["id"]
    body = json.loads(event["body"]) if "body" in event else {}

    update_params = {
        "Key": {"pk": user_id},
        "UpdateExpression": "SET",
        "ExpressionAttributeNames": {},
        "ExpressionAttributeValues": {},
        "ReturnValues": "ALL_NEW",
    }

    expression_assignments = []
    for field, value in body.items():
        expression_assignments.append(f"#{field} = :{field}")
        update_params["ExpressionAttributeNames"][f"#{field}"] = field
        update_params["ExpressionAttributeValues"][f":{field}"] = value

    update_params["UpdateExpression"] = "SET" + ", ".join(expression_assignments)
    response = table.update_item(**update_params)

    user = response["Attributes"]

    return {"statusCode": 200, "body": json.dumps({"user": user})}

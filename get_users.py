import os
import json
import boto3
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource("dynamodb",
                          region_name="localhost",
                          endpoint_url="http://localhost:8000",
                          aws_access_key_id="default_access_key",
                          aws_secret_access_key="default_secret",  
                          )
table = dynamodb.Table("users-table")

def handler(event, context):
    response = table.query(KeyConditionExpression=Key("pk").eq("1"))

    return {"statusCode": 200, "body": json.dumps(response)}

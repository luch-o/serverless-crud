import os
import json
import boto3

cognito_client = boto3.client("cognito-idp")
CLIENT_ID = os.getenv("CLIENT_ID")
USER_POOL_ID = os.getenv("USER_POOL_ID")


def handler(event, context):
    body = json.loads(event["body"])
    username = body["username"]
    password = body["password"]

    # signup
    cognito_client.sign_up(
        ClientId=CLIENT_ID,
        Username=username,
        Password=password,
    )

    # admin confirm user
    cognito_client.admin_confirm_sign_up(
        UserPoolId=USER_POOL_ID,
        Username=username,
    )

    return {
        "statusCode": 201,
    }

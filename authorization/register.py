import os
import boto3

cognito_client = boto3.client("cognito-idp")
CLIENT_ID = os.getenv("CLIENT_ID")
USER_POOL_ID = os.getenv("USER_POOL_ID")


def handler(event, context):
    username = event["body"]["username"]
    password = event["body"]["password"]

    # signup
    cognito_client.sign_up(
        ClientId=CLIENT_ID,
        Username=username,
        Password=password,
    )

    # admin confirm user
    cognito_client.admin_confirm_user(
        UserPoolId=USER_POOL_ID,
        Username=username,
    )

    return {
        "statusCode": 201,
    }

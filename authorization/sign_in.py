import os
import json
import boto3

cognito_client = boto3.client("cognito-idp")
CLIENT_ID = os.getenv("CLIENT_ID")


def handler(event, context):
    body = json.loads(event["body"])
    username = body["username"]
    password = body["password"]

    response = cognito_client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password,
        },
        ClientId=CLIENT_ID,
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                response["AuthenticationResult"][key]
                for key in ("AccessToken", "RefreshToken", "ExpiresIn")
            }
        )
    }

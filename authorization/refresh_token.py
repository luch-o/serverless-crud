import os
import json
import boto3

cognito_client = boto3.client("cognito-idp")
CLIENT_ID = os.getenv("CLIENT_ID")


def handler(event, context):
    body = json.loads(event["body"])
    refresh_token = body["refresh_token"]

    response = cognito_client.initiate_auth(
        AuthFlow="REFRESH_TOKEN",
        AuthParameters={
            "REFRESH_TOKEN": refresh_token,
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

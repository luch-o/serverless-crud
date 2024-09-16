import os
import json
import boto3
from botocore.config import Config

s3_client = boto3.client("s3", config=Config(signature_version="v4"))
URL_EXPIRATION = 5 * 60 # five minutes

def handler(event, context):
    filename = event["queryStringParameters"]["filename"]
    object_key = f"upload/{filename}"
    signed_url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": os.getenv("BUCKET"),
            "Key": object_key,
        },
        ExpiresIn=URL_EXPIRATION,
        HttpMethod="PUT", 
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps({"signed_url": signed_url})
    }
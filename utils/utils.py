import os
from decimal import Decimal

dynamodb_params = {}
if os.getenv("IS_OFFLINE", False):
    dynamodb_params = {
        "region_name": "localhost",
        "endpoint_url": "http://localhost:8000",
    }

def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    else:
        raise TypeError(f"Object of class {obj.__class__.__name__} is not serializable.")
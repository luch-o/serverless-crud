import boto3
from pathlib import Path
from urllib.parse import unquote_plus
from PIL import Image

SUPPORTED_FORMATS = frozenset((".png", ".jpg"))
s3_client = boto3.client("s3")
local_storage_path = Path("/tmp")

def resize_image(image_path: Path, resized_path: Path, new_width: int):
    """Creates image thumbnail for a specific width, keeping aspect ratio."""
    with Image.open(image_path) as image:
        width, height = image.size
        aspect_ratio = height / width
        new_height = new_width * aspect_ratio
        image.thumbnail((new_width, new_height))
        image.save(resized_path)

def handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = unquote_plus(event["Records"][0]["s3"]["object"]["key"])

    tmpkey = key.replace("/", "")
    download_path = local_storage_path / tmpkey
    
    image_type = download_path.suffix
    if image_type.lower() not in SUPPORTED_FORMATS:
        print(f"only {SUPPORTED_FORMATS} supported, got {image_type}.")
        return

    s3_client.download_file(bucket, key, download_path)

    widths = [50, 100, 200]
    for width in widths:        
        key_path = Path(key)
        resized_name = f"{width}-{key_path.name}"
        resized_path = local_storage_path / resized_name
        
        resize_image(download_path, resized_path, width)

        upload_key = f"resized/{resized_name}"
        s3_client.upload_file(resized_path, bucket, upload_key)


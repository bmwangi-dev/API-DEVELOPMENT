import os
from io import BytesIO
from typing import Optional

import boto3
from botocore.config import Config as BotoConfig

import auth

ALLOWED_CONTENT_TYPES = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/gif": "gif",
    "image/webp": "webp",
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def _get_client():
    return boto3.client(
        "s3",
        endpoint_url=auth.RUSTFS_ENDPOINT,
        aws_access_key_id=auth.RUSTFS_ACCESS_KEY,
        aws_secret_access_key=auth.RUSTFS_SECRET_KEY,
        region_name="us-east-1",
        config=BotoConfig(signature_version="s3v4"),
    )


def _key_for(user_id: str, ext: str) -> str:
    return f"profile_images/{user_id}.{ext}"


def upload_profile_image(file_bytes: bytes, user_id: str, content_type: str) -> str:
    ext = ALLOWED_CONTENT_TYPES.get(content_type)
    if ext is None:
        raise ValueError(f"Unsupported content type: {content_type}")
    key = _key_for(user_id, ext)
    client = _get_client()
    client.upload_fileobj(
        BytesIO(file_bytes),
        auth.RUSTFS_BUCKET,
        key,
        ExtraArgs={"ContentType": content_type},
    )
    return key


def delete_profile_image(key: str) -> None:
    if not key:
        return
    client = _get_client()
    client.delete_object(Bucket=auth.RUSTFS_BUCKET, Key=key)


def get_profile_image_url(key: str) -> Optional[str]:
    if not key:
        return None
    client = _get_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": auth.RUSTFS_BUCKET, "Key": key},
        ExpiresIn=3600,
    )


def extract_ext_from_key(key: str) -> str:
    return key.rsplit(".", 1)[-1] if "." in key else ""

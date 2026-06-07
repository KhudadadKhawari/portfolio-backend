from pathlib import PurePosixPath
from uuid import uuid4

import boto3
from botocore.client import Config
from fastapi import UploadFile

from app.core.config import settings


class StorageService:
    def __init__(self) -> None:
        self.client = boto3.client(
            "s3",
            endpoint_url=f"{'https' if settings.minio_use_ssl else 'http'}://{settings.minio_endpoint}",
            aws_access_key_id=settings.minio_root_user,
            aws_secret_access_key=settings.minio_root_password,
            config=Config(signature_version="s3v4"),
        )

    def ensure_bucket(self) -> None:
        buckets = self.client.list_buckets().get("Buckets", [])
        if not any(bucket["Name"] == settings.minio_bucket for bucket in buckets):
            self.client.create_bucket(Bucket=settings.minio_bucket)

    def upload(self, file: UploadFile, category: str) -> tuple[str, str, int]:
        self.ensure_bucket()
        extension = PurePosixPath(file.filename or "upload").suffix
        object_key = f"{category}/{uuid4().hex}{extension}"
        file.file.seek(0, 2)
        size_bytes = file.file.tell()
        file.file.seek(0)
        self.client.upload_fileobj(
            file.file,
            settings.minio_bucket,
            object_key,
            ExtraArgs={"ContentType": file.content_type or "application/octet-stream"},
        )
        return object_key, self.public_url(object_key), size_bytes

    def public_url(self, object_key: str) -> str:
        endpoint = settings.minio_public_endpoint.rstrip("/")
        return f"{endpoint}/{settings.minio_bucket}/{object_key}"


storage_service = StorageService()

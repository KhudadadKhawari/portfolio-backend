from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.content import Asset
from app.schemas.content import AssetRead
from app.services.storage import storage_service

router = APIRouter(prefix="/uploads", tags=["uploads"])
DbSession = Annotated[Session, Depends(get_db)]
AdminUser = Annotated[str, Depends(require_admin)]


@router.post("", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
def upload_asset(
    db: DbSession,
    _: AdminUser,
    file: Annotated[UploadFile, File()],
    category: Annotated[str, Form()] = "general",
    project_id: Annotated[int | None, Form()] = None,
    certification_id: Annotated[int | None, Form()] = None,
) -> Asset:
    object_key, url, size_bytes = storage_service.upload(file, category)
    asset = Asset(
        object_key=object_key,
        file_name=file.filename or object_key,
        content_type=file.content_type or "application/octet-stream",
        size_bytes=size_bytes,
        category=category,
        url=url,
        project_id=project_id,
        certification_id=certification_id,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

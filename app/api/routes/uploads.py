from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.content import Asset, Certification, Project
from app.schemas.content import AssetRead
from app.services.storage import storage_service

router = APIRouter(prefix="/uploads", tags=["uploads"])
DbSession = Annotated[Session, Depends(get_db)]
AdminUser = Annotated[str, Depends(require_admin)]


def parse_optional_form_id(value: str | None, field_name: str) -> int | None:
    if value is None or value.strip() == "":
        return None
    try:
        parsed_value = int(value)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field_name} must be an integer",
        ) from exc
    if parsed_value < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field_name} must be a positive integer",
        )
    return parsed_value


def ensure_upload_target_exists(
    db: Session,
    project_id: int | None,
    certification_id: int | None,
) -> None:
    if project_id is not None and db.get(Project, project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if certification_id is not None and db.get(Certification, certification_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certification not found")


@router.post("", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
def upload_asset(
    db: DbSession,
    _: AdminUser,
    file: Annotated[UploadFile, File()],
    category: Annotated[str, Form()] = "general",
    project_id: Annotated[str | None, Form()] = None,
    certification_id: Annotated[str | None, Form()] = None,
) -> Asset:
    parsed_project_id = parse_optional_form_id(project_id, "project_id")
    parsed_certification_id = parse_optional_form_id(certification_id, "certification_id")
    ensure_upload_target_exists(db, parsed_project_id, parsed_certification_id)

    object_key, url, size_bytes = storage_service.upload(file, category)
    asset = Asset(
        object_key=object_key,
        file_name=file.filename or object_key,
        content_type=file.content_type or "application/octet-stream",
        size_bytes=size_bytes,
        category=category,
        url=url,
        project_id=parsed_project_id,
        certification_id=parsed_certification_id,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.content import Certification
from app.schemas.content import CertificationCreate, CertificationRead, CertificationUpdate

router = APIRouter(prefix="/certifications", tags=["certifications"])
DbSession = Annotated[Session, Depends(get_db)]
AdminUser = Annotated[str, Depends(require_admin)]
CERTIFICATION_NOT_FOUND = "Certification not found"


@router.get("", response_model=list[CertificationRead])
def list_certifications(db: DbSession) -> list[Certification]:
    return list(
        db.scalars(
            select(Certification)
            .options(selectinload(Certification.assets))
            .order_by(Certification.id.desc())
        )
    )


@router.post("", response_model=CertificationRead, status_code=status.HTTP_201_CREATED)
def create_certification(
    payload: CertificationCreate,
    db: DbSession,
    _: AdminUser,
) -> Certification:
    certification = Certification(**payload.model_dump())
    db.add(certification)
    db.commit()
    db.refresh(certification)
    return certification


@router.put("/{certification_id}", response_model=CertificationRead)
def update_certification(
    certification_id: int,
    payload: CertificationUpdate,
    db: DbSession,
    _: AdminUser,
) -> Certification:
    certification = db.get(Certification, certification_id)
    if certification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=CERTIFICATION_NOT_FOUND)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(certification, key, value)
    db.commit()
    db.refresh(certification)
    return certification


@router.delete("/{certification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_certification(
    certification_id: int,
    db: DbSession,
    _: AdminUser,
) -> None:
    certification = db.get(Certification, certification_id)
    if certification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=CERTIFICATION_NOT_FOUND)
    db.delete(certification)
    db.commit()

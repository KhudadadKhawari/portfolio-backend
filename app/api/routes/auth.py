from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import require_admin
from app.core.security import authenticate_admin, create_access_token
from app.schemas.content import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


AdminUser = Annotated[str, Depends(require_admin)]


@router.post("/login")
def login(payload: LoginRequest) -> TokenResponse:
    if not authenticate_admin(payload.username, payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(payload.username))


@router.get("/me")
def me(username: AdminUser) -> dict[str, str]:
    return {"username": username, "role": "admin"}

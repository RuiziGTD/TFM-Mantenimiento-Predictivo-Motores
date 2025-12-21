import os
from fastapi import APIRouter, HTTPException
from api.app.dto.login_dto import LoginRequestDTO, LoginResponseDTO
from api.app.validators.login_validator import LoginValidator

router = APIRouter(prefix="/login", tags=["Login"])
admin_user = os.getenv("ADMIN_USER")
admin_password = os.getenv("ADMIN_PASSWORD")

@router.post("", response_model=LoginResponseDTO)
def login(data: LoginRequestDTO):

    if not admin_user or not admin_password:
        raise HTTPException(
            status_code=500,
            detail="Variables de entorno no cargadas"
        )

    if data.username == admin_user and data.password == admin_password:
        return LoginResponseDTO(
            success=True,
            message="Login correcto",
            access_token="fake-token"
        )

    raise HTTPException(
        status_code=401,
        detail="Credenciales incorrectas"
    )

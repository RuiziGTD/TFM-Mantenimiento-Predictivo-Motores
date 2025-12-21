import os
from fastapi import APIRouter, HTTPException
from api.app.dto.login_dto import LoginRequestDTO, LoginResponseDTO
from api.logs.logging_config import get_logger

logger = get_logger("login_controller")

router = APIRouter(prefix="/login", tags=["Login"])
admin_user = os.getenv("ADMIN_USER")
admin_password = os.getenv("ADMIN_PASSWORD")

@router.post("", response_model=LoginResponseDTO)
def login(data: LoginRequestDTO):

    logger.info(f"Intento de login usuario={data.username}")

    if not admin_user or not admin_password:
        logger.error("Variables de entorno no cargadas")
        raise HTTPException(
            status_code=500,
            detail="Variables de entorno no cargadas"
        )

    if data.username == admin_user and data.password == admin_password:
        logger.info(f"Login correcto usuario={data.username}")

        return LoginResponseDTO(
            success=True,
            message="Login correcto",
            access_token="fake-token"
        )
    
    logger.warning(f"Credenciales incorrectas: username='{data.username}'")
    raise HTTPException(
        status_code=401,
        detail="Credenciales incorrectas"
    )

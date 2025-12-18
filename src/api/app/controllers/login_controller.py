from fastapi import APIRouter, HTTPException
from api.app.dto.login_dto import LoginRequestDTO, LoginResponseDTO

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("", response_model=LoginResponseDTO)
def login(data: LoginRequestDTO):

    if data.username == "admin" and data.password == "admin":
        return LoginResponseDTO(
            success=True,
            message="Login correcto",
            access_token="fake-token"
        )

    raise HTTPException(status_code=401, detail="Credenciales incorrectas")

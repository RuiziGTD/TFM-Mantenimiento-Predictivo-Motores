from pydantic import BaseModel, Field

class LoginRequestDTO(BaseModel):
    username: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Usuario (1–20 caracteres)"
    )
    password: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Contraseña (1–20 caracteres)"
    )


class LoginResponseDTO(BaseModel):
    success: bool
    message: str
    access_token: str | None = None
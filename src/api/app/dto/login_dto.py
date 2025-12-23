from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException

class LoginRequestDTO(BaseModel):
    username: str = Field(
        ...,
        description="Usuario (1–20 caracteres)"
    )
    password: str = Field(
        ...,
        description="Contraseña (1–20 caracteres)"
    )

    @field_validator("username")
    def username_valido(cls, v):
        if not v or not v.strip():
            raise HTTPException(status_code=400, detail="El usuario no puede estar vacío")
        if len(v) > 20:
            raise HTTPException(status_code=400, detail="El usuario no puede tener más de 20 caracteres")
        return v

    @field_validator("password")
    def password_valida(cls, v):
        if not v or not v.strip():
            raise HTTPException(status_code=400, detail="La contraseña no puede estar vacía")
        if len(v) > 20:
            raise HTTPException(status_code=400, detail="La contraseña no puede tener más de 20 caracteres")
        return v


class LoginResponseDTO(BaseModel):
    success: bool
    message: str
    access_token: str | None = None

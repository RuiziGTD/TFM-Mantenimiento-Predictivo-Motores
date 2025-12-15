from pydantic import BaseModel

class LoginRequestDTO(BaseModel):
    username: str
    password: str


class LoginResponseDTO(BaseModel):
    success: bool
    message: str
    access_token: str | None = None
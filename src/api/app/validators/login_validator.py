from fastapi import HTTPException


class LoginValidator:

    MAX_LENGTH = 20

    @staticmethod
    def validate(username: str, password: str) -> None:
        if username is None or password is None:
            raise HTTPException(status_code=400, detail="Usuario y contraseña obligatorios")

        if username.strip() == "" or password.strip() == "":
            raise HTTPException(status_code=400, detail="Usuario y contraseña no pueden estar vacíos")

        if len(username) > LoginValidator.MAX_LENGTH:
            raise HTTPException(status_code=400, detail="El usuario supera los 20 caracteres")

        if len(password) > LoginValidator.MAX_LENGTH:
            raise HTTPException(status_code=400, detail="La contraseña supera los 20 caracteres")

from dotenv import load_dotenv
load_dotenv()   # ← SIEMPRE arriba del todo

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.app.controllers.login_controller import router as login_router
from api.app.controllers.predict_controller import router as predict_router
from api.logs.logging_config import get_logger

logger = get_logger("main")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)
app.include_router(predict_router)

logger.info("API iniciada correctamente.")
from fastapi import FastAPI
from api.app.controllers.login_controller import router as login_router
from api.app.controllers.predict_controller import router as predict_router
from fastapi.middleware.cors import CORSMiddleware

# 1. IMPORTAR LA LIBRERÍA DE MONITORIZACIÓN
from prometheus_fastapi_instrumentator import Instrumentator

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

# 2. ACTIVAR EL MONITOR
# Esto crea el endpoint /metrics automáticamente para que Prometheus pueda leerlo
Instrumentator().instrument(app).expose(app)
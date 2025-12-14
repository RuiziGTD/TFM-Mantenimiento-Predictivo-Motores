from fastapi import FastAPI

# Inicializa la aplicación de la API
app = FastAPI(
    title="API de Mantenimiento Predictivo",
    description="Sirve predicciones de RUL (Vida Útil Restante) para motores de avión.",
    version="0.1.0",
)


@app.get("/health", tags=["Monitoring"])
def get_health():
    """
    Endpoint de comprobación de salud.
    Verifica que la API está operativa.
    """
    return {"status": "ok"}



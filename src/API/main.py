from fastapi import FastAPI

# Inicializa la aplicación de la API
app = FastAPI(
    title="API de Mantenimiento Predictivo",
    description="Sirve predicciones de RUL (Vida Útil Restante) para motores de avión.",
    version="0.1.0"
)

@app.get("/health", tags=["Monitoring"])
def get_health():
    """
    Endpoint de comprobación de salud.
    Verifica que la API está operativa.
    """
    return {"status": "ok"}

# En el futuro (Fase 3), aquí añadiremos el endpoint de predicción
# @app.post("/predict", tags=["Prediction"])
# def predict_rul(data: ...):
#     # Aquí llamaremos al modelo de Gabriel
#     return {"prediction": 100}
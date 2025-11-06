from fastapi.testclient import TestClient
from src.api.main import app # Importa tu app de FastAPI

# Crea un "cliente" especial para probar la API
client = TestClient(app)

def test_health_check():
    """
    Prueba que el endpoint /health funciona y responde correctamente.
    """
    # 1. Llama al endpoint /health de tu API
    response = client.get("/health")
    
    # 2. Comprueba que el código de estado es 200 (OK)
    assert response.status_code == 200
    
    # 3. Comprueba que la respuesta es exactamente la que esperamos
    assert response.json() == {"status": "ok"}
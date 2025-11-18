from fastapi.testclient import TestClient
from src.api.main import app  # Importa tu app de FastAPI

# TEST 6 - Test del Endpoint de salud de la API
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


# TEST 7 - Test del Endpoint de documentación automática
def test_api_docs_are_available():
    """
    Prueba que la documentación automática (/docs) funciona.
    """
    # 1. Llama al endpoint /docs
    response = client.get("/docs")

    # 2. Comprueba que el código de estado es 200 (OK)
    assert response.status_code == 200


# TEST 8 - Test de "Ruta No Encontrada" (Control de Errores)
def test_invalid_endpoint_returns_404():
    """
    Prueba que una ruta inexistente devuelve un error 404.
    """
    # 1. Llama a una ruta inventada
    response = client.get("/ruta-falsa-que-no-existe")

    # 2. Comprueba que el código de estado es 404 (Not Found)
    assert response.status_code == 404

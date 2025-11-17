# 📂 src/

Este directorio contiene el **código fuente principal** del proyecto **TFM - Mantenimiento Predictivo de Motores de Aviación**.

-Para arrancar MLFlow -> mlflow ui
-Para arrancar la API -> python -m uvicorn main:app --app-dir src/api --reload
-Dentro de la API, para probar que funciona, usar /health al final de la URL, ejemplo: http://127.0.0.1:8000/health
-Para arrancar el Dashboard con Streamlit -> streamlit run src/app/dashboard.py---
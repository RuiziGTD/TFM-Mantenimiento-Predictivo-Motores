import sys
import os

# --- PARCHE UNIVERSAL (WIN/MAC/LINUX) ---
# Obtiene la ruta absoluta del directorio raíz (dos niveles arriba: src -> modelo_ia)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
# ----------------------------------------

import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from src.utils.logger import get_logger
from src.utils.reproducibility import set_seeds

# Configuración
logger = get_logger(__name__)
# Ajustamos la ruta para que coincida con donde 'make pipeline' deja los datos
DATA_PATH = "output/output_csv/train_FD001_filtrado.csv"
MODEL_NAME = "baseline_linear_regression"
RANDOM_SEED = 42

def train_baseline():
    logger.info("Iniciando entrenamiento del modelo base (Regresión Lineal)...")

    # 1. Cargar datos
    if not os.path.exists(DATA_PATH):
        logger.error(f"No se encuentra el archivo de datos: {DATA_PATH}")
        print(f"Error: No existe {DATA_PATH}. Ejecuta 'make pipeline' primero.")
        return

    df = pd.read_csv(DATA_PATH)
    
    # 2. Preprocesamiento simple
    # Quitamos columnas que no son sensores o settings útiles para una regresión simple
    drop_cols = ['RUL', 'unit_number', 'time_in_cycles'] 
    
    X = df.drop(columns=drop_cols, errors='ignore')
    y = df['RUL']
    
    # 3. Split Train/Test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED
    )

    # 4. Iniciar MLflow
    mlflow.set_experiment("Baseline_Experiment")
    
    with mlflow.start_run(run_name="Linear_Regression_Baseline"):
        
        # Entrenar
        model = LinearRegression()
        model.fit(X_train, y_train)
        logger.info("Modelo entrenado correctamente.")

        # Predicciones
        y_pred = model.predict(X_test)

        # Métricas
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"\n📊 Resultados Baseline:")
        print(f"   RMSE: {rmse:.2f}")
        print(f"   MAE:  {mae:.2f}")
        print(f"   R2:   {r2:.4f}")

        # Registrar en MLflow
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.sklearn.log_model(model, "model_baseline")
        
        logger.info("Entrenamiento finalizado y registrado en MLflow.")

if __name__ == "__main__":
    # Semillas para reproducibilidad
    set_seeds(use_tensorflow=False) # Activar reproducibilidad
    train_baseline()
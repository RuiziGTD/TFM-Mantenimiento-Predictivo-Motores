import sys
import os

# --- PARCHE UNIVERSAL (WIN/MAC/LINUX) ---
# Obtiene la ruta absoluta del directorio raíz del proyecto (un nivel arriba de /src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
# ----------------------------------------

import argparse
import pandas as pd
from src.pipeline.pipeline import run_pipeline
from src.config import *
from src.processing.spark import spark_init
from src.utils.reproducibility import set_seeds
import os
from flows_prefect.flujo_retraining import flujo_retraining

# Limpiamos imports de modelos (TensorFlow) para evitar el bloqueo 'mutex' en Mac.
# El entrenamiento ahora se gestiona separadamente vía Makefile.

if __name__ == "__main__":
    # 1. Configuración Inicial
    set_seeds(seed=42, use_tensorflow=False) 
    
    
    # Asegurar carpeta de logs
    os.makedirs("logs", exist_ok=True)
    open("logs/pipeline.log", "w").close()

    # 2. Configuración de Spark (Interacción reducida para automatización)
    # Si quieres que el Makefile no se detenga, podrías forzar 'n' o leer argumentos.
    # De momento mantenemos tu lógica original.
    
    spark_choice = None
    while spark_choice not in ("y", "n"):
        spark_choice = input(
            "¿Quieres usar spark? (y/n): "
        ).lower()
        if spark_choice not in ("y", "n"):
            print("Carácter no reconocido.")
    
    eda_choice = input(
            "¿Quieres crear un EDA? (Y/n): "
        ).lower()

    spark = spark_init() if spark_choice == "y" else None
    eda = "y" if eda_choice != "n" else None

    params = [spark, eda]

    # 3. Ejecutar SOLO el Pipeline de Datos
    print("Iniciando Pipeline de Datos...")
    run_pipeline(params)

    if spark:
        spark.stop()

    print("\tEjecutamos el DAG.")
    flujo_retraining()

    print("Pipeline de datos finalizado. Los archivos están listos en 'output/'.")
    # El entrenamiento (LSTM) se ejecutará en el siguiente paso del Makefile.
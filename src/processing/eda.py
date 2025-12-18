import os
import numpy as np
import matplotlib.pyplot as plt
from config import EDA_OUTPUT

def view_eda(df, df_name):
    df_name = os.path.splitext(df_name)[0]  # Quitar .txt

    out_dir = os.path.join(EDA_OUTPUT, df_name)
    os.makedirs(out_dir, exist_ok=True)

    # Escoger 30 motores aleatorios como máximo
    all_units = df["unit_number"].unique()
    max_motores = 30
    selected_units = np.random.choice(all_units, size=min(max_motores, len(all_units)), replace=False)
    
    # Listado de sensores (a partir de la columna 5 en CMAPSS y excluyendo el RUL)
    sensor_columns = [col for col in df.columns[5:] if col != "RUL"]
    
    # Para cada sensor, generar 2 gráficos
    for sensor in sensor_columns:
        sensor_dir = os.path.join(out_dir, sensor)
        os.makedirs(sensor_dir, exist_ok=True)

        # Evolución por motor: como varían los sensores en cada motor por cada ciclo
        plt.figure(figsize=(10, 6))
        for unit in selected_units:  # solo los seleccionados
            df_unit = df[df["unit_number"] == unit]
            plt.plot(df_unit["time_in_cycles"], df_unit[sensor], alpha=0.4)

        plt.title(f"{sensor} - Evolución por motor")
        plt.xlabel("Ciclo")
        plt.ylabel(sensor)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(sensor_dir, f"{sensor}_evolucion.png"))
        plt.close()

        # Scatter sensor vs RUL: Como varia el valor según el RUL
        if "RUL" in df.columns:  # No es 100% necesario, es una comprobación extra para evitar errores
            plt.figure(figsize=(8, 6))
            plt.scatter(df[sensor], df["RUL"], alpha=0.3)
            plt.title(f"{sensor} vs RUL")
            plt.xlabel(sensor)
            plt.ylabel("RUL")
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(os.path.join(sensor_dir, f"{sensor}_scatter_rul.png"))
            plt.close()

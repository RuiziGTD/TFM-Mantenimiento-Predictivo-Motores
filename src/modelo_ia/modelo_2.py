import sys
import os

# --- PARCHE UNIVERSAL (WIN/MAC/LINUX) ---
# Obtiene la ruta absoluta del directorio raíz (dos niveles arriba: src -> modelo_ia)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"
# ----------------------------------------

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import load_model
import mlflow
import matplotlib.pyplot as plt
from src.utils.reproducibility import set_seeds

def train_lstm_rul2(
    train_path,
    test_path,
    rul_path,
    sequence_length=50,
    epochs=200,
    batch_size=64,
    model_path="lstm_rul2.keras",
):
    """
    Entrena un modelo LSTM para predecir RUL usando secuencias de ciclos.
    Incluye padding automático, dropout, early stopping y métricas completas.
    """

    mlflow.set_experiment("rul_lstm_experiment")

    with mlflow.start_run():
        print("Versión TF:", tf.__version__)
        print("GPUs disponibles:", tf.config.list_physical_devices("GPU"))

        # --- 1. Definir columnas ---
        feature_cols = [
            "op_setting_1",
            "op_setting_2",
            "op_setting_3",
            "T24",
            "T30",
            "T50",
            "P30",
            "Nf",
            "Nc",
            "Ps30",
            "phi",
            "NRf",
            "NRc",
            "BPR",
            "htBleed",
            "W31",
            "W32",
        ]

        # Función para asegurar columnas

        def ensure_columns(df, feature_cols):
            for col in feature_cols:
                if col not in df.columns:
                    df[col] = 0.0  # o valor neutro
            if "RUL" in df.columns:
                return df[feature_cols + ["unit_number", "RUL"]]
            else:
                return df[feature_cols + ["unit_number"]]

        def load_multi(paths):
            if not isinstance(paths, list):
                paths = [paths]
            return pd.concat([pd.read_csv(p) for p in paths], ignore_index=True)

        # --- 2. Cargar datos ---
        df_train = load_multi(train_path)
        df_test = pd.read_csv(test_path)
        y_test = pd.read_csv(rul_path, header=None).values.flatten()

        df_train = ensure_columns(df_train, feature_cols)
        df_test = ensure_columns(df_test, feature_cols)

        # --- 3. Normalizar ---
        scaler = MinMaxScaler()
        df_train[feature_cols] = scaler.fit_transform(df_train[feature_cols])
        df_test[feature_cols] = scaler.transform(df_test[feature_cols])

        # --- Recortar RUL ---

        max_rul_cap = 125
        df_train["RUL"] = df_train["RUL"].clip(upper=max_rul_cap)

        # --- 4. Crear secuencias para train ---
        def create_sequences_with_padding(df, seq_len, feature_cols):
            X, y = [], []
            groups = []  # Para cada secuencia, almacenamos su unidad
            for unit in df["unit_number"].unique():
                unit_data = df[df["unit_number"] == unit]
                feats = unit_data[feature_cols].values
                rul = unit_data["RUL"].values
                L = len(feats)
                # Generar secuencias desde longitud 1 hasta L
                for i in range(1, L + 1):
                    start = max(0, i - seq_len)
                    seq = feats[start:i]
                    if len(seq) < seq_len:
                        pad = np.zeros((seq_len - len(seq), seq.shape[1]))
                        seq = np.vstack([pad, seq])
                    X.append(seq)
                    y.append(rul[i - 1])
                    groups.append(unit)
            return np.array(X), np.array(y), np.array(groups)

        X_train_seq, y_train_seq, groups_train = create_sequences_with_padding(
            df_train, sequence_length, feature_cols
        )

        # Agrupar por unit number, que coga toda la secuencia de un motor

        gss = GroupShuffleSplit(n_splits=1, test_size=0.1, random_state=42)
        train_idx, val_idx = next(gss.split(X_train_seq, y_train_seq, groups_train))

        X_tr, X_val = X_train_seq[train_idx], X_train_seq[val_idx]
        y_tr, y_val = y_train_seq[train_idx], y_train_seq[val_idx]

        # --- 5. Definir modelo LSTM ---
        model = models.Sequential(
            [
                layers.Masking(
                    mask_value=0.0, input_shape=(sequence_length, len(feature_cols))
                ),
                layers.LSTM(128, return_sequences=True),
                layers.BatchNormalization(),
                layers.Dropout(0.2),
                layers.LSTM(64),
                layers.BatchNormalization(),
                layers.Dropout(0.2),
                layers.Dense(32, activation="relu"),
                layers.Dense(1),
            ]
        )
        model.compile(optimizer="adam", loss="mse")

        # --- 6. Entrenar con early stopping ---
        early_stop = EarlyStopping(
            monitor="val_loss", patience=10, restore_best_weights=True
        )
        reduce_lr = ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=5, min_lr=1e-6, verbose=1
        )

        model_path = "lstm_rul.keras"

        mlflow.log_param("epochs", epochs)
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("sequence_length", sequence_length)
        mlflow.log_param("optimizer", "adam")
        mlflow.log_param("loss_function", "mse")

        if os.path.exists(model_path):
            print("Cargando modelo guardado...")
            model = load_model(model_path)
        else:
            model.fit(
                X_tr,
                y_tr,
                validation_data=(X_val, y_val),
                epochs=epochs,
                batch_size=batch_size,
                callbacks=[early_stop, reduce_lr],
                verbose=1,
            )

            print("Entrenamiento terminado, guardando modelo...")
            model.save(model_path)
            print("Modelo guardado, empezando predicción en test...")

        mlflow.tensorflow.log_model(model, "modelo_lstm_RUL_final")

        # --- 7. Predicción en test con padding y alineación ---

        print("Procesando test...")

        # 1) Obtener unidades únicas y ordenarlas
        test_units = np.unique(df_test["unit_number"])
        test_units.sort()  # orden consistente

        # 2) Crear secuencias para cada motor
        X_test_seq = []
        for unit in test_units:
            mask = df_test["unit_number"] == unit
            unit_data = df_test.loc[mask, feature_cols].values
            if len(unit_data) < sequence_length:
                pad = np.zeros((sequence_length - len(unit_data), unit_data.shape[1]))
                unit_data = np.vstack([pad, unit_data])
            # Tomamos la última ventana de tamaño sequence_length
            X_test_seq.append(unit_data[-sequence_length:])

        X_test_seq = np.array(X_test_seq)

        # 3) Alinear y_test con el mismo orden de test_units
        # Asumiendo que rul_path tiene RUL en orden de unit_number ascendente
        y_test_aligned = np.array(
            [y_test[unit - 1] for unit in test_units], dtype=np.float32
        )

        # 4) Predicción
        y_pred = model.predict(X_test_seq, batch_size=64).flatten()

        print("Test procesado.")

        plt.figure(figsize=(8, 5))
        plt.scatter(y_test_aligned, y_pred, s=20)
        max_r = max(y_test_aligned)
        plt.plot([0, max_r], [0, max_r], "--")
        plt.xlabel("RUL Real")
        plt.ylabel("RUL Predicho")
        plt.title("Real vs Predicho - Test")
        plt.grid()
        plt.show()

        # --- 8. Evaluar métricas ---
        mse = mean_squared_error(y_test_aligned, y_pred)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(y_test_aligned - y_pred))
        # MAPE seguro: evita división por 0
        den = np.where(y_test_aligned == 0, 1e-6, y_test_aligned)
        mape = np.mean(np.abs((y_test_aligned - y_pred) / den)) * 100
        r2 = r2_score(y_test_aligned, y_pred)

        # NASA Score (CMAPSS)
        score = 0
        for d in y_pred - y_test_aligned:
            if d < 0:
                score += np.exp(-d / 13) - 1
            else:
                score += np.exp(d / 10) - 1

        # 9. Tabla de resultados
        df_resultados = pd.DataFrame(
            {"Motor": test_units, "RUL_real": y_test_aligned, "RUL_predicho": y_pred}
        )

        resultados = {
            "model": model,
            "metrics": {
                "MSE": mse,
                "RMSE": rmse,
                "MAE": mae,
                "MAPE": mape,
                "R2": r2,
                "NASA_Score": score,
            },
            "predicciones": df_resultados,
        }

        for k, v in resultados["metrics"].items():
            mlflow.log_metric(k, v)

        # Guardar modelo
        mlflow.tensorflow.log_model(resultados["model"], "lstm_model")
        return resultados

if __name__ == "__main__":
    # --- BLOQUE DE EJECUCIÓN DIRECTA (Necesario para Make) ---
    set_seeds()  # Activar reproducibilidad

    print("Iniciando entrenamiento automático de LSTM...")

    # Usamos try/except para capturar errores si no existen los datos
    try:
        # Rutas por defecto para una ejecución estándar
        resultados = train_lstm_rul2(
            train_path=["output/output_csv/train_FD001_filtrado.csv",
                        "output/output_csv/train_FD002_filtrado.csv",
                        "output/output_csv/train_FD003_filtrado.csv",
                        "output/output_csv/train_FD004_filtrado.csv"],
            test_path="output/data_test/test_FD002_filtrado.csv",
            rul_path="data/raw_data/RUL_FD002.txt",
            epochs=50,  # Pocas épocas para probar el pipeline rápido
        )

        m = resultados["metrics"]
        print(f"\n✅ Entrenamiento completado correctamente.")
        print(f"   MSE: {m['MSE']:.2f}")
        print(f"   RMSE: {m['RMSE']:.2f}")
        print(f"   R2: {m['R2']:.2f}")
        print(f"   NASA Score: {m['NASA_Score']:.2f}")

    except FileNotFoundError as e:
        print(f"\n❌ Error: No se encuentran los archivos de datos.")
        print(f"   Detalle: {e}")
        print(
            "   -> Asegúrate de ejecutar 'make pipeline' primero para generar los CSV filtrados."
        )

# RESULTADOS
"""
{'MSE': 816.8579870879265, 'RMSE': np.float64(28.580727546511593), 'MAE': np.float64(21.71330299156513),
 'MAPE': np.float64(37.744045961323934), 'R2': 0.7175611469539649, 'NASA_Score': np.float64(14573.410391026688)}

   Motor  RUL_real  RUL_predicho
0      1        18     12.647554
0      1        18     12.647554
1      2        79    146.435379
2      3       106     85.773888
3      4       110    116.111702
4      5        15     12.081519
"""

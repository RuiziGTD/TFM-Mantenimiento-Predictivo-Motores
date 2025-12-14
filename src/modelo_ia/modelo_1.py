import sys
import os

# --- PARCHE UNIVERSAL (WIN/MAC/LINUX) ---
# Obtiene la ruta absoluta del directorio raíz (dos niveles arriba: src -> modelo_ia)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
# ----------------------------------------

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from src.utils.reproducibility import set_seeds


def train_lstm_rul(
    train_path,
    test_path,
    rul_path,
    sequence_length=50,
    epochs=100,
    batch_size=64,
    model_path="lstm_rul.keras",
):
    # --- IMPORTS DIFERIDOS (Para evitar bloqueo en Mac) ---
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.metrics import mean_squared_error, r2_score
    # ------------------------------------------------------
    """
    Entrena un modelo LSTM para predecir RUL usando secuencias de ciclos.
    Incluye padding automático, dos capas LSTM, dropout y early stopping.
    """

    # --- 1. Definir columnas ---
    feature_cols = [
        "time_in_cycles",
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

    # --- 2. Cargar datos ---
    df_train = pd.read_csv(train_path)
    df_test = pd.read_csv(test_path)
    y_test = pd.read_csv(rul_path, header=None).values.flatten()

    # --- 3. Normalizar ---
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(df_train[feature_cols].values)

    # --- 4. Crear secuencias para train ---
    def create_sequences(df, seq_len):
        X, y = [], []
        for unit in df["unit_number"].unique():
            unit_data = df[df["unit_number"] == unit]
            unit_features = scaler.transform(unit_data[feature_cols].values)
            unit_rul = unit_data["RUL"].values

            for i in range(len(unit_features) - seq_len + 1):
                X.append(unit_features[i : i + seq_len])
                y.append(unit_rul[i + seq_len - 1])
        return np.array(X), np.array(y)

    X_train_seq, y_train_seq = create_sequences(df_train, sequence_length)

    # --- 5. Definir modelo LSTM mejorado ---
    model = models.Sequential(
        [
            layers.LSTM(
                64,
                return_sequences=True,
                input_shape=(sequence_length, len(feature_cols)),
            ),
            layers.Dropout(0.2),
            layers.LSTM(32),
            layers.Dropout(0.2),
            layers.Dense(16, activation="relu"),
            layers.Dense(1),  # salida RUL
        ]
    )
    model.compile(optimizer="adam", loss="mse")

    # --- 6. Entrenar con early stopping ---
    early_stop = EarlyStopping(
        monitor="val_loss", patience=10, restore_best_weights=True
    )
    model.fit(
        X_train_seq,
        y_train_seq,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.1,
        callbacks=[early_stop],
        verbose=1,
    )

    model.save(model_path)

    # --- 7. Predicción en test con padding ---
    y_pred = []
    for unit in df_test["unit_number"].unique():
        unit_data = df_test[df_test["unit_number"] == unit]
        unit_features = scaler.transform(unit_data[feature_cols].values)

        # Padding si el motor tiene menos ciclos que sequence_length
        if len(unit_features) < sequence_length:
            pad = np.zeros(
                (sequence_length - len(unit_features), unit_features.shape[1])
            )
            unit_features = np.vstack([pad, unit_features])

        last_seq = unit_features[-sequence_length:]
        pred = model.predict(last_seq[np.newaxis, :, :])[0, 0]
        y_pred.append(pred)

    # --- 8. Evaluar ---
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # --- 2. Cargar datos ---
    df_train = pd.read_csv(train_path)
    df_test = pd.read_csv(test_path)
    y_test = pd.read_csv(rul_path, header=None).values.flatten()

    # --- 3. Normalizar ---
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(df_train[feature_cols].values)

    # --- 4. Crear secuencias para train ---
    def create_sequences(df, seq_len):
        X, y = [], []
        for unit in df["unit_number"].unique():
            unit_data = df[df["unit_number"] == unit]
            unit_features = scaler.transform(unit_data[feature_cols].values)
            unit_rul = unit_data["RUL"].values

            for i in range(len(unit_features) - seq_len + 1):
                X.append(unit_features[i : i + seq_len])
                y.append(unit_rul[i + seq_len - 1])
        return np.array(X), np.array(y)

    X_train_seq, y_train_seq = create_sequences(df_train, sequence_length)

    # --- 5. Definir modelo LSTM ---
    model = models.Sequential(
        [
            layers.Masking(
                mask_value=0.0, input_shape=(sequence_length, len(feature_cols))
            ),
            layers.LSTM(64, return_sequences=True),
            layers.Dropout(0.2),
            layers.LSTM(32),
            layers.Dropout(0.2),
            layers.Dense(16, activation="relu"),
            layers.Dense(1),  # salida RUL
        ]
    )
    model.compile(optimizer="adam", loss="mse")

    # --- 6. Entrenar con early stopping ---
    early_stop = EarlyStopping(
        monitor="val_loss", patience=10, restore_best_weights=True
    )
    model.fit(
        X_train_seq,
        y_train_seq,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.1,
        callbacks=[early_stop],
        verbose=1,
    )

    model.save(model_path)

    # --- 7. Predicción en test con padding ---
    y_pred = []
    motores_test = sorted(df_test["unit_number"].unique())  # asegurar orden
    for unit in motores_test:
        unit_data = df_test[df_test["unit_number"] == unit]
        unit_features = scaler.transform(unit_data[feature_cols].values)

        # Padding si el motor tiene menos ciclos que sequence_length
        if len(unit_features) < sequence_length:
            pad = np.zeros(
                (sequence_length - len(unit_features), unit_features.shape[1])
            )
            unit_features = np.vstack([pad, unit_features])

        last_seq = unit_features[-sequence_length:]
        pred = model.predict(last_seq[np.newaxis, :, :])[0, 0]
        y_pred.append(pred)

    # --- 8. Evaluar métricas ---
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(y_test - y_pred))
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    r2 = r2_score(y_test, y_pred)

    # NASA Score (CMAPSS)
    score = 0
    for d in y_pred - y_test:
        if d < 0:
            score += np.exp(-d / 13) - 1
        else:
            score += np.exp(d / 10) - 1

    # Tabla de resultados
    df_resultados = pd.DataFrame(
        {"Motor": motores_test, "RUL_real": y_test, "RUL_predicho": y_pred}
    )

    return {
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

if __name__ == "__main__":
    # --- BLOQUE DE EJECUCIÓN DIRECTA (Necesario para Make) ---
    set_seeds()  # Activar reproducibilidad

    print("Iniciando entrenamiento automático de LSTM...")

    # Usamos try/except para capturar errores si no existen los datos
    try:
        # Rutas por defecto para una ejecución estándar
        resultados = train_lstm_rul(
            train_path="output/output_csv/train_FD001_filtrado.csv",
            test_path="output/data_test/test_FD001_filtrado.csv",
            rul_path="data/raw_data/RUL_FD001.txt",
            epochs=50,  # Pocas épocas para probar el pipeline rápido
        )

        m = resultados["metrics"]
        print(f"\n✅ Entrenamiento completado correctamente.")
        print(f"   RMSE: {m['RMSE']:.2f}")
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

"""
resultados_fd002 = train_lstm_rul(
    train_path="../output/output_csv/train_FD002_filtrado.csv",
    test_path="../output/data_test/test_FD002_filtrado.csv",
    rul_path="../data/raw_data/RUL_FD002.txt",
    sequence_length=50,
    epochs=100
)

print("\nPredicciones FD002 (primeras filas):")
print(resultados_fd002["predicciones"].head())
"""

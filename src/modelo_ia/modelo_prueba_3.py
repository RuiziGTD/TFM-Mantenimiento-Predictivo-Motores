import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf

def train_lstm_rul(train_path, test_path, rul_path,
                   sequence_length=50, epochs=200, batch_size=64,
                   model_path="lstm_rul.keras"):
    """
    Entrena un modelo LSTM para predecir RUL usando secuencias de ciclos.
    Incluye padding automático, dropout, early stopping y métricas completas.
    """

    print("Versión TF:", tf.__version__)
    print("GPUs disponibles:", tf.config.list_physical_devices('GPU'))

    # --- 1. Definir columnas ---
    feature_cols = [
        "time_in_cycles",
        "op_setting_1","op_setting_2","op_setting_3",
        "T24","T30","T50","P30","Nf","Nc","Ps30","phi",
        "NRf","NRc","BPR","htBleed","W31","W32"
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
    def create_sequences(df, seq_len):
        X, y = [], []
        for unit in df["unit_number"].unique():
            unit_data = df[df["unit_number"] == unit]
            unit_features = unit_data[feature_cols].values
            unit_rul = unit_data["RUL"].values

            for i in range(len(unit_features) - seq_len + 1):
                X.append(unit_features[i:i+seq_len])
                y.append(unit_rul[i+seq_len-1])
        return np.array(X), np.array(y)

    X_train_seq, y_train_seq = create_sequences(df_train, sequence_length)

    # --- 5. Definir modelo LSTM ---
    model = models.Sequential([ 
        layers.Masking(mask_value=0., input_shape=(sequence_length, len(feature_cols))), 
        layers.LSTM(128, return_sequences=True), 
        layers.Dropout(0.2), 
        layers.LSTM(64), 
        layers.Dropout(0.2), 
        layers.Dense(32, activation="relu"), 
        layers.Dense(1)])
    model.compile(optimizer="adam", loss="mse")

    # --- 6. Entrenar con early stopping ---
    early_stop = EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=5, min_lr=1e-6, verbose=1)

    model.fit(X_train_seq, y_train_seq,
              epochs=epochs,
              batch_size=batch_size,
              validation_split=0.1,
              callbacks=[early_stop, reduce_lr],
              verbose=1)

    print("Entrenamiento terminado, guardando modelo...")
    model.save(model_path)
    print("Modelo guardado, empezando predicción en test...")

    # --- 7. Predicción en test con padding ---
    # 1) Obtener todos los motores una sola vez
    unit_numbers = df_test["unit_number"].values
    features = df_test[feature_cols].values

    print("Procesando test")

    X_test_seq = []
    for unit in np.unique(unit_numbers):
        mask = unit_numbers == unit
        unit_data = features[mask]
        if len(unit_data) < sequence_length:
            pad = np.zeros((sequence_length - len(unit_data), unit_data.shape[1]))
            unit_data = np.vstack([pad, unit_data])
        X_test_seq.append(unit_data[-sequence_length:])

    X_test_seq = np.array(X_test_seq)
    y_pred = model.predict(X_test_seq, batch_size=64).flatten()

    print("Test procesado")

    # --- 8. Evaluar métricas ---
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(y_test - y_pred))
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    r2 = r2_score(y_test, y_pred)

    # NASA Score (CMAPSS)
    score = 0
    for d in (y_pred - y_test):
        if d < 0:
            score += np.exp(-d/13) - 1
        else:
            score += np.exp(d/10) - 1

    motores_test_unique = np.unique(df_test["unit_number"].values)

    # Tabla de resultados
    df_resultados = pd.DataFrame({
        "Motor": motores_test_unique,
        "RUL_real": y_test,
        "RUL_predicho": y_pred
    })

    return {
        "model": model,
        "metrics": {
            "MSE": mse,
            "RMSE": rmse,
            "MAE": mae,
            "MAPE": mape,
            "R2": r2,
            "NASA_Score": score
        },
        "predicciones": df_resultados
    }

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
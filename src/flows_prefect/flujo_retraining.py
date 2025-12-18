from prefect import flow, task
import pandas as pd
import glob
import os
import numpy as np
import re
import joblib  
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.metrics import mean_squared_error, r2_score

# ----- TAREAS -----
@task
def cargar_datos():
    ruta_carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "nuevos_datos")
    archivos = glob.glob(os.path.join(ruta_carpeta, "*.csv"))
    lista_df = [pd.read_csv(f).dropna() for f in archivos]
    if lista_df:
        df = pd.concat(lista_df, ignore_index=True)
        return df
    else:
        raise ValueError(f"No se encontraron CSV en {ruta_carpeta}")

@task
def preprocesar(df):
    feature_cols = [
        "op_setting_1","op_setting_2","op_setting_3","T24","T30","T50","P30",
        "Nf","Nc","Ps30","phi","NRf","NRc","BPR","htBleed","W31","W32"
    ]
    # Asegurar columnas
    for col in feature_cols + ["unit_number", "RUL"]:
        if col not in df.columns:
            df[col] = 0.0
    df_features = df[feature_cols + ["unit_number", "RUL"]]

    # Normalizar
    scaler = MinMaxScaler()
    df_features[feature_cols] = scaler.fit_transform(df_features[feature_cols])
    
    # Guardar scaler
    ruta_models = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
    os.makedirs(ruta_models, exist_ok=True)
    joblib.dump(scaler, os.path.join(ruta_models, "scaler.pkl"))
    
    return df_features, feature_cols

def create_sequences_with_padding(df, seq_len, feature_cols):
    X, y, groups = [], [], []
    for unit in df["unit_number"].unique():
        unit_data = df[df["unit_number"] == unit]
        feats = unit_data[feature_cols].values
        rul = unit_data["RUL"].values
        L = len(feats)
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


@task
def entrenar_modelo(df_features, feature_cols, sequence_length=50, epochs=50, batch_size=64):
    X, y, groups = create_sequences_with_padding(df_features, sequence_length, feature_cols)
    
    # Split train/val por unidad
    from sklearn.model_selection import GroupShuffleSplit
    gss = GroupShuffleSplit(n_splits=1, test_size=0.1, random_state=42)
    train_idx, val_idx = next(gss.split(X, y, groups))
    X_tr, X_val = X[train_idx], X[val_idx]
    y_tr, y_val = y[train_idx], y[val_idx]
    
    # Carpeta nuevos modelos con versionado
    ruta_nuevos_modelos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "nuevos_modelos")
    os.makedirs(ruta_nuevos_modelos, exist_ok=True)
    existentes = glob.glob(os.path.join(ruta_nuevos_modelos, "lstm_rul_v*.keras"))
    versiones = [int(re.search(r'_v(\d+)\.keras$', f).group(1)) for f in existentes if re.search(r'_v(\d+)\.keras$', f)]
    nueva_version = max(versiones) + 1 if versiones else 1
    modelo_path = os.path.join(ruta_nuevos_modelos, f"lstm_rul_v{nueva_version}.keras")
    
    # Definir modelo LSTM
    model = models.Sequential([
        layers.Masking(mask_value=0.0, input_shape=(sequence_length, len(feature_cols))),
        layers.LSTM(128, return_sequences=True),
        layers.BatchNormalization(),
        layers.Dropout(0.2),
        layers.LSTM(64),
        layers.BatchNormalization(),
        layers.Dropout(0.2),
        layers.Dense(32, activation="relu"),
        layers.Dense(1),
    ])
    model.compile(optimizer="adam", loss="mse")
    
    # Callbacks
    early_stop = EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=5, min_lr=1e-6, verbose=1)
    
    # Entrenamiento
    model.fit(X_tr, y_tr, validation_data=(X_val, y_val),
              epochs=epochs, batch_size=batch_size,
              callbacks=[early_stop, reduce_lr], verbose=1)
    
    # Guardar modelo
    model.save(modelo_path)
    
    # --- Predicciones y métricas ---
    y_pred = model.predict(X_val, batch_size=batch_size).flatten()
    mse = mean_squared_error(y_val, y_pred)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(y_val - y_pred))
    den = np.where(y_val == 0, 1e-6, y_val)
    mape = np.mean(np.abs((y_val - y_pred) / den)) * 100
    r2 = r2_score(y_val, y_pred)
    
    df_resultados = pd.DataFrame({"RUL_real": y_val, "RUL_predicho": y_pred})
    metrics = {"MSE": mse, "RMSE": rmse, "MAE": mae, "MAPE": mape, "R2": r2}
    
    return {"modelo_path": modelo_path, "metrics": metrics, "predicciones": df_resultados}

@task
def guardar_modelo(modelo_path):
    print(f"Modelo guardado en: {modelo_path}")

# ----- FLOW -----
@flow(name="retraining_modelo_motores")
def flujo_retraining():
    df_features, feature_cols = preprocesar(cargar_datos())
    resultados = entrenar_modelo(df_features, feature_cols)
    guardar_modelo(resultados["modelo_path"])
    print("Métricas de validación:", resultados["metrics"])
    print("Predicciones RUL:", resultados["predicciones"].head())

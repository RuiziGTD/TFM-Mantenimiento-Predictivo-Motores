import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras import layers, models

def train_autoencoder_rul(train_paths, test_paths, rul_paths,
                          encoding_dim=16, epochs=50, batch_size=128,
                          model_path="autoencoder_rul.keras"):
    """
    Entrena un autoencoder con varios CSV de train concatenados.
    Incluye 'time_in_cycles' como feature para mejorar la predicción de RUL.
    Evalúa cada dataset de test por separado con su archivo de RUL correspondiente.
    """

    # --- 1. Definir columnas fijas ---
    feature_cols = [
        "unit_number","time_in_cycles",
        "op_setting_1","op_setting_2","op_setting_3",
        "T24","T30","T50","P30","Nf","Nc","Ps30","phi",
        "NRf","NRc","BPR","htBleed","W31","W32"
    ]

    # --- 2. Cargar y concatenar train ---
    train_dfs = [pd.read_csv(p) for p in train_paths]
    df_train = pd.concat(train_dfs, ignore_index=True)

    # --- 3. Separar features y target ---
    X_train = df_train[feature_cols].values
    y_train = df_train["RUL"].values

    # --- 4. Normalizar ---
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # --- 5. Definir autoencoder ---
    input_dim = X_train_scaled.shape[1]
    input_layer = layers.Input(shape=(input_dim,))
    encoded = layers.Dense(encoding_dim, activation="relu")(input_layer)
    decoded = layers.Dense(input_dim, activation="sigmoid")(encoded)

    autoencoder = models.Model(inputs=input_layer, outputs=decoded)
    autoencoder.compile(optimizer="adam", loss="mse")

    # --- 6. Entrenar autoencoder ---
    autoencoder.fit(X_train_scaled, X_train_scaled,
                    epochs=epochs,
                    batch_size=batch_size,
                    shuffle=True,
                    validation_split=0.1,
                    verbose=1)

    autoencoder.save(model_path)

    encoder = models.Model(inputs=input_layer, outputs=encoded)
    X_train_latent = encoder.predict(X_train_scaled)

    regressor = RandomForestRegressor(n_estimators=200, random_state=42)
    regressor.fit(X_train_latent, y_train)

    # --- 7. Evaluar cada dataset ---
    metrics = {}
    for test_path, rul_path in zip(test_paths, rul_paths):
        df_test = pd.read_csv(test_path)
        y_test = pd.read_csv(rul_path, header=None).values.flatten()

        X_test = df_test[feature_cols].values
        X_test_scaled = scaler.transform(X_test)
        X_test_latent = encoder.predict(X_test_scaled)

        # Última fila de cada unidad
        last_cycles = df_test.groupby("unit_number").tail(1).index
        X_test_last = X_test_latent[last_cycles]

        y_pred = regressor.predict(X_test_last)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        metrics[test_path] = {"MSE": mse, "R2": r2}

    return {
        "autoencoder": autoencoder,
        "encoder": encoder,
        "regressor": regressor,
        "metrics": metrics,
        "features_used": feature_cols
    }
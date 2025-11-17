import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras import layers, models


import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras import layers, models

def train_autoencoder_rul(train_path, test_path, rul_path,
                          encoding_dim=16, epochs=50, batch_size=128,
                          model_path="autoencoder_rul.keras"):
    """
    Entrena un autoencoder con datos de train y un regresor supervisado para predecir RUL.
    Usa archivo aparte de RUL para test (CMAPSS style).
    """

    # --- 1. Cargar datos ---
    df_train = pd.read_csv(train_path)
    df_test = pd.read_csv(test_path, sep=",")  # ajusta sep si es necesario

    # --- 2. Separar features y target ---
    X_train = df_train.drop(columns=["RUL"]).values
    y_train = df_train["RUL"].values

    # RUL real por unidad
    y_test = pd.read_csv(rul_path, header=None).values.flatten()

    # --- 3. Normalizar ---
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(df_test.values)

    # --- 4. Definir autoencoder ---
    input_dim = X_train_scaled.shape[1]
    input_layer = layers.Input(shape=(input_dim,))
    encoded = layers.Dense(encoding_dim, activation="relu")(input_layer)
    decoded = layers.Dense(input_dim, activation="sigmoid")(encoded)

    autoencoder = models.Model(inputs=input_layer, outputs=decoded)
    autoencoder.compile(optimizer="adam", loss="mse")

    # --- 5. Entrenar autoencoder ---
    autoencoder.fit(X_train_scaled, X_train_scaled,
                    epochs=epochs,
                    batch_size=batch_size,
                    shuffle=True,
                    validation_split=0.1,
                    verbose=1)

    # --- 6. Guardar autoencoder en formato moderno ---
    autoencoder.save(model_path)

    # --- 7. Encoder ---
    encoder = models.Model(inputs=input_layer, outputs=encoded)

    # --- 8. Extraer representaciones latentes ---
    X_train_latent = encoder.predict(X_train_scaled)
    X_test_latent = encoder.predict(X_test_scaled)

    # --- 9. Regresor supervisado ---
    regressor = RandomForestRegressor(n_estimators=200, random_state=42)
    regressor.fit(X_train_latent, y_train)

    # --- 10. Predicción por unidad ---
    # Tomar última fila de cada unidad en test
    df_test["unit_number"] = df_test.iloc[:,0]  # asume primera col es unit_number
    last_cycles = df_test.groupby("unit_number").tail(1).index
    X_test_last = X_test_latent[last_cycles]

    y_pred = regressor.predict(X_test_last)

    # --- 11. Evaluar ---
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return {
        "autoencoder": autoencoder,
        "encoder": encoder,
        "regressor": regressor,
        "metrics": {"MSE": mse, "R2": r2}
    }


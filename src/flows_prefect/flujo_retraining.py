from prefect import flow, task
import pandas as pd
import glob
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib

# ----- TAREAS -----
@task
def cargar_datos(ruta_carpeta="../../data/nuevos_datos/"):
    #   Funcion que carga los nuevos datos
    archivos = glob.glob(ruta_carpeta + "*.csv")
    lista_df = [pd.read_csv(f).dropna() for f in archivos]
    if lista_df:
        df = pd.concat(lista_df, ignore_index=True)
        return df
    else:
        raise ValueError(f"No se encontraron CSV en {ruta_carpeta}")

@task
def preprocesar(df):
    scaler = StandardScaler()
    X = scaler.fit_transform(df)
    joblib.dump(scaler, "models/scaler.pkl")
    return X

@task
def entrenar_modelo(X):
    model = Sequential()
    model.add(LSTM(32, input_shape=(X.shape[1], 1)))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse")
    model.fit(X, X, epochs=10, batch_size=16)
    model.save("models/modelo_autoencoder.h5")
    return "models/modelo_autoencoder.h5"

@task
def guardar_modelo(modelo_path):
    print(f"Modelo guardado en: {modelo_path}")

# ----- FLOW -----
@flow(name="retraining_modelo_motores")
def flujo_retraining():
    datos = cargar_datos()
    X = preprocesar(datos)
    modelo_path = entrenar_modelo(X)
    guardar_modelo(modelo_path)

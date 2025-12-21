import sys
import os

# --- PARCHE UNIVERSAL (WIN/MAC/LINUX) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"
# ----------------------------------------

import pandas as pd
import numpy as np
import joblib
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
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--fine-tune", action="store_true", help="Entrena sobre datos nuevos")
args = parser.parse_args()

def train_lstm_rul2(
    train_path,
    test_path,
    rul_path,
    sequence_length=50,
    epochs=200,
    batch_size=64,
    model_path="models/lstm_rul.keras",
):
    import mlflow
    
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
            "op_setting_1", "op_setting_2", "op_setting_3", "T24", "T30", "T50",
            "P30", "Nf", "Nc", "Ps30", "phi", "NRf", "NRc", "BPR", "htBleed", "W31", "W32",
        ]

        def ensure_columns(df, feature_cols):
            for col in feature_cols:
                if col not in df.columns:
                    df[col] = 0.0
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
            groups = []
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

        X_train_seq, y_train_seq, groups_train = create_sequences_with_padding(
            df_train, sequence_length, feature_cols
        )

        gss = GroupShuffleSplit(n_splits=1, test_size=0.1, random_state=42)
        train_idx, val_idx = next(gss.split(X_train_seq, y_train_seq, groups_train))

        X_tr, X_val = X_train_seq[train_idx], X_train_seq[val_idx]
        y_tr, y_val = y_train_seq[train_idx], y_train_seq[val_idx]

        # --- 5. Definir modelo LSTM ---
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

        # --- 6. Entrenar ---
        early_stop = EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
        reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=5, min_lr=1e-6, verbose=1)

        mlflow.log_param("epochs", epochs)
        mlflow.log_param("batch_size", batch_size)

        if os.path.exists(model_path) and args.fine_tune:
            print("Cargando modelo guardado para Fine Tuning...")
            model = load_model(model_path)
            optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5)
            model.compile(optimizer=optimizer, loss="mse")
            
            for layer in model.layers[:-2]:
                layer.trainable = False

            model.fit(
                X_tr, y_tr,
                validation_data=(X_val, y_val),
                epochs=30,
                batch_size=batch_size,
                callbacks=[early_stop, reduce_lr],
                verbose=1
            )
            model.save("models/lstm_rul2.keras")

        else:
            # Entrenamiento desde cero
            model.fit(
                X_tr, y_tr,
                validation_data=(X_val, y_val),
                epochs=epochs,
                batch_size=batch_size,
                callbacks=[early_stop, reduce_lr],
                verbose=1,
            )

            print("Entrenamiento terminado. Guardando modelos...")
            
            # Guardado robusto con rutas absolutas para Docker
            scaler_abs_path = '/app/models/minmax_scaler.save'
            joblib.dump(scaler, scaler_abs_path)
            
            model_abs_path = '/app/models/lstm_rul.keras'
            model.save(model_abs_path)
            
            print(f"Archivos guardados en: {scaler_abs_path} y {model_abs_path}")

        mlflow.tensorflow.log_model(model, "modelo_lstm_RUL_final")

        # --- 7. Predicción en test ---
        print("Procesando test...")
        test_units = np.unique(df_test["unit_number"])
        test_units.sort()

        X_test_seq = []
        for unit in test_units:
            mask = df_test["unit_number"] == unit
            unit_data = df_test.loc[mask, feature_cols].values
            if len(unit_data) < sequence_length:
                pad = np.zeros((sequence_length - len(unit_data), unit_data.shape[1]))
                unit_data = np.vstack([pad, unit_data])
            X_test_seq.append(unit_data[-sequence_length:])

        X_test_seq = np.array(X_test_seq)
        
        y_test_aligned = np.array([y_test[unit - 1] for unit in test_units], dtype=np.float32)
        y_test_aligned = np.clip(y_test_aligned, a_min=None, a_max=max_rul_cap)

        y_pred = model.predict(X_test_seq, batch_size=64).flatten()
        print("Test procesado.")

        # --- 8. Evaluar métricas ---
        mse = mean_squared_error(y_test_aligned, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test_aligned, y_pred)

        score = 0
        for d in y_pred - y_test_aligned:
            if d < 0:
                score += np.exp(-d / 13) - 1
            else:
                score += np.exp(d / 10) - 1

        df_resultados = pd.DataFrame(
            {"Motor": test_units, "RUL_real": y_test_aligned, "RUL_predicho": y_pred}
        )

        resultados = {
            "model": model,
            "metrics": {"MSE": mse, "RMSE": rmse, "R2": r2, "NASA_Score": score},
            "predicciones": df_resultados,
        }
        return resultados

if __name__ == "__main__":
    set_seeds()

    print("Iniciando entrenamiento automático de LSTM...")

    try:
        if args.fine_tune:
            train_files = ["output/output_csv/nuevos_datos.csv"]
        else:
            train_files = [
                "output/output_csv/train_FD001_filtrado.csv",
                "output/output_csv/train_FD002_filtrado.csv",
                "output/output_csv/train_FD003_filtrado.csv",
                "output/output_csv/train_FD004_filtrado.csv",
            ]

        # Configurado a 1 época para test de guardado. Cambiar a 50 para producción.
        resultados = train_lstm_rul2(
            train_path=train_files,
            test_path="output/data_test/test_FD002_filtrado.csv",
            rul_path="data/raw_data/RUL_FD002.txt",
            epochs=50, 
            batch_size=64,
            model_path="models/lstm_rul.keras",
        )

        m = resultados["metrics"]
        print(f"\n✅ Entrenamiento completado correctamente.")
        print(f"   RMSE: {m['RMSE']:.2f}")
        print(f"   R2: {m['R2']:.2f}")
        print(resultados["predicciones"].head(5))

    except FileNotFoundError as e:
        print(f"\n❌ Error: No se encuentran los archivos de datos.")
        print(f"   Detalle: {e}")

# RESULTADOS
"""
   MSE: 671.01
   RMSE: 25.90
   R2: 0.77
   NASA Score: 8881.94
   Motor  RUL_real  RUL_predicho
0      1      18.0     23.557371
1      2      79.0    100.564911
2      3     106.0    121.594467
3      4     110.0    108.830879
4      5      15.0     21.792208
5      6     155.0    119.715324
6      7       6.0      5.222230
7      8      90.0     82.437424
8      9      11.0      9.274798
9     10      79.0    112.077866
"""

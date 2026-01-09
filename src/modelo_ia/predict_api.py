import numpy as np
import os
import pandas as pd
from tensorflow.keras.models import load_model
import joblib

def predict_rul(df, sequence_length=50):
    feature_cols = [
        "op_setting_1","op_setting_2","op_setting_3","T24","T30","T50",
        "P30","Nf","Nc","Ps30","phi","NRf","NRc","BPR","htBleed","W31","W32"
    ]

    # 1) Normalizar con scaler guardado

    scaler = joblib.load("../models/minmax_scaler.save")

    print(scaler.n_features_in_)

    df[feature_cols] = scaler.transform(df[feature_cols])

    # 2) Crear secuencias
    test_units = df["unit_number"].unique()
    test_units.sort()
    X_test_seq = []
    for unit in test_units:
        unit_data = df[df["unit_number"] == unit][feature_cols].values
        if len(unit_data) < sequence_length:
            pad = np.zeros((sequence_length - len(unit_data), unit_data.shape[1]))
            unit_data = np.vstack([pad, unit_data])
        X_test_seq.append(unit_data[-sequence_length:])
    X_test_seq = np.array(X_test_seq)

    # 3) Cargar modelo y predecir
    model = load_model("../models/lstm_rul.keras")
    y_pred = model.predict(X_test_seq, batch_size=64).flatten()
    return y_pred
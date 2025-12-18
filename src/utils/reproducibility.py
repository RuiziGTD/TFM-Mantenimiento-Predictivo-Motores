import os
import random
import numpy as np

def set_seeds(seed=42, use_tensorflow=True):
    """
    Fija las semillas aleatorias para garantizar reproducibilidad.
    
    Args:
        seed (int): El número semilla (default 42).
        use_tensorflow (bool): Si es True, intenta fijar la semilla de TF. 
    """
    # 1. Python y Numpy (Siempre seguros)
    os.environ['PYTHONHASHSEED'] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    print(f"[Reproducibility] Semillas básicas (Python/Numpy) fijadas a: {seed}")

    # 2. TensorFlow (Solo si se pide y está disponible)
    if use_tensorflow:
        try:
            import tensorflow as tf
            tf.random.set_seed(seed)
            print(f"[Reproducibility] Semilla TensorFlow fijada a: {seed}")
        except ImportError:
            print("[Reproducibility] TensorFlow no está instalado o no se pudo cargar.")
        except Exception as e:
            print(f"[Reproducibility] Error al cargar TensorFlow (evitando bloqueo): {e}")
"""
Carga el modelo .keras una sola vez al iniciar Django.
"""
import numpy as np
from PIL import Image
from django.conf import settings

_model = None


def load_model():
    global _model
    if _model is not None:
        return _model

    model_path = settings.MODEL_PATH
    if not model_path.exists():
        print(f"[WARNING] Modelo no encontrado en {model_path}. Skipping load.")
        return None

    import keras
    _model = keras.models.load_model(str(model_path))
    print(f"[INFO] Modelo cargado desde {model_path}")
    return _model


def is_model_loaded() -> bool:
    return _model is not None


def predict(image_file) -> dict:
    """
    Corre inferencia sobre la imagen subida.
    Regresa: { class, confidence, scores }
    """
    model = _model or load_model()
    if model is None:
        raise RuntimeError("El modelo no está cargado.")

    img = Image.open(image_file).convert('RGB')
    img = img.resize(settings.MODEL_INPUT_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)

    preds = model.predict(arr)[0]
    classes = settings.MODEL_CLASSES
    idx = int(np.argmax(preds))

    scores = {c: float(round(preds[i], 4)) for i, c in enumerate(classes)}

    return {
        'class': classes[idx] if classes else str(idx),
        'confidence': float(round(float(preds[idx]), 4)),
        'scores': scores,
    }

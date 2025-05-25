import os
import requests
import numpy as np
import onnxruntime as ort
from PIL import Image

# URL pública del modelo ONNX (no se debe incluir en el repo)
MODEL_URL = "https://github.com/onnx/models/raw/main/Computer_Vision/regnet_x_16gf_Opset18_torch_hub/regnet_x_16gf_Opset18.onnx"
MODEL_PATH = "regnet.onnx"

# 1. Descargar modelo si no existe
def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Descargando modelo ONNX...")
        response = requests.get(MODEL_URL)
        with open(MODEL_PATH, "wb") as f:
            f.write(response.content)
        print("Modelo descargado.")
    else:
        print("El modelo ya está disponible localmente.")

# 2. Preprocesar imagen para que el modelo la entienda
def preprocess_image(image_path):
    img = Image.open(image_path).resize((224, 224)).convert("RGB")
    img = np.array(img).astype(np.float32)
    img = img.transpose(2, 0, 1)  # De (H, W, C) a (C, H, W)
    img /= 255.0
    img = np.expand_dims(img, axis=0)  # Agregar dimensión batch
    return img

# 3. Ejecutar predicción
def predict(image_path):
    download_model()
    img = preprocess_image(image_path)
    session = ort.InferenceSession(MODEL_PATH)
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: img})
    pred_class = int(np.argmax(outputs[0]))
    confidence = float(np.max(outputs[0]))
    return pred_class, confidence


import json

LABELS_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
LABELS_PATH = "imagenet_labels.json"

def download_labels():
    if not os.path.exists(LABELS_PATH):
        print("Descargando etiquetas de ImageNet...")
        response = requests.get(LABELS_URL)
        if response.status_code == 200:
            with open(LABELS_PATH, "wb") as f:
                f.write(response.content)
            print("Etiquetas descargadas.")
        else:
            print(f"Error al descargar etiquetas: {response.status_code}")

def get_label(index):
    download_labels()
    with open(LABELS_PATH, "r") as f:
        labels = json.load(f)
    return labels[index]

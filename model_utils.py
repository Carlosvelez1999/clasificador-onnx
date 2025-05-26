import os
import json
import requests
import numpy as np
import onnxruntime as ort
from PIL import Image

# URL pública del modelo ONNX
MODEL_URL = "https://github.com/onnx/models/raw/main/Computer_Vision/mobilenetv2_050_Opset18_timm/mobilenetv2_050_Opset18.onnx"
MODEL_PATH = "mobilenetv2.onnx"

# URL pública del archivo de etiquetas
LABELS_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
LABELS_PATH = "imagenet_labels.json"

# ---------- MODELO Y SESIÓN ----------

# Descargar el modelo si no existe
def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Descargando modelo ONNX...")
        response = requests.get(MODEL_URL)
        with open(MODEL_PATH, "wb") as f:
            f.write(response.content)
        print("Modelo descargado.")
    else:
        print("El modelo ya está disponible localmente.")

# Descargar etiquetas si no existen
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

# Preprocesamiento de imagen
def preprocess_image(image_path):
    img = Image.open(image_path).resize((224, 224)).convert("RGB")
    img = np.array(img).astype(np.float32)
    img = img.transpose(2, 0, 1)  # De (H, W, C) a (C, H, W)
    img /= 255.0
    img = np.expand_dims(img, axis=0)
    return img

# ---------- INICIALIZACIÓN GLOBAL ----------

# Descargar y cargar modelo al inicio
download_model()
session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])

# Descargar etiquetas
download_labels()
with open(LABELS_PATH, "r") as f:
    LABELS = json.load(f)

# ---------- PREDICCIÓN ----------

def predict(image_path):
    img = preprocess_image(image_path)
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: img})

    def softmax(x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()

    probs = softmax(outputs[0][0])
    pred_class = int(np.argmax(probs))
    confidence = float(np.max(probs))
    return pred_class, confidence

def get_label(index):
    return LABELS[index]

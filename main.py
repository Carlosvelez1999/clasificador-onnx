from flask import Flask, render_template, request
import os
from datetime import datetime
from model_utils import predict, get_label

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    label = None
    confidence = None

    if request.method == "POST":
        # Guardar imagen
        file = request.files["image"]
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        # Ejecutar predicción
        pred_class, confidence = predict(image_path)
        label = get_label(pred_class)

        # Detectar entorno: dev o prod
        ENV = os.getenv("APP_ENV", "dev")  # Por defecto usamos "dev"
        output_file = f"predicciones_{ENV}.txt"

        # Guardar predicción en archivo correspondiente
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} | {file.filename} | {label} | Confianza: {confidence:.2f}\n")

    return render_template("index.html", label=label, confidence=confidence)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


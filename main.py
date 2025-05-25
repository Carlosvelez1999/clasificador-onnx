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
        # 1. Guardar imagen
        file = request.files["image"]
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        # 2. Predecir
        pred_class, confidence = predict(image_path)
        label = get_label(pred_class)

        # 3. Detectar entorno: dev o prod
        ENV = os.getenv("APP_ENV", "dev")
        output_file = f"predicciones_{ENV}.txt"

        # 4. Guardar predicción
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} | {file.filename} | {label} | Confianza: {confidence:.2f}\n")

        # 5. Mostrar el contenido del archivo por consola (útil en Render)
        print(f"📝 Contenido actual de {output_file}:")
        with open(output_file, "r", encoding="utf-8") as f:
            print(f.read())

    return render_template("index.html", label=label, confidence=confidence)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

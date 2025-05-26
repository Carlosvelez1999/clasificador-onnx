from flask import Flask, render_template, request, url_for
import os
from datetime import datetime
import pytz  
from model_utils import predict, get_label
from sheets_utils import registrar_prediccion

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    label = None
    confidence = None
    image_filename = None

    if request.method == "POST":
        # Guardar imagen
        file = request.files["image"]
        zona_colombia = pytz.timezone("America/Bogota")  
        timestamp = datetime.now(zona_colombia).strftime("%Y%m%d%H%M%S")  
        image_filename = f"{timestamp}_{file.filename}"
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        file.save(image_path)

        # Ejecutar predicción
        pred_class, confidence = predict(image_path)
        label = get_label(pred_class)

        # Registrar en Google Sheets
        registrar_prediccion(image_filename, label, confidence)

    return render_template(
        "index.html",
        label=label,
        confidence=confidence,
        image_filename=image_filename
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

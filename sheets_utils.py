import os
import json
import gspread
import pytz
from dotenv import load_dotenv
from datetime import datetime
from google.oauth2.service_account import Credentials

# Cargar variables desde .env (solo en local)
load_dotenv()

# Leer JSON desde variable de entorno
json_str = os.getenv("GOOGLE_CREDENTIALS_JSON")
info = json.loads(json_str)

# Leer entorno (dev o prod)
APP_ENV = os.getenv("APP_ENV", "dev")

# Alcances
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Inicializar cliente de Google Sheets
credentials = Credentials.from_service_account_info(info, scopes=SCOPES)
client = gspread.authorize(credentials)

# ID de la hoja
SHEET_ID = "1rWdlpUYMYgJRrCL9WCjzNL-0wS0pzI3zCcH3OJFnRVw"
SHEET_NAME = "Predicciones Dev" if APP_ENV == "dev" else "Predicciones Prod"

def registrar_prediccion(nombre_imagen, etiqueta, confianza):
    try:
        hoja = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
        zona_colombia = pytz.timezone("America/Bogota")
        timestamp = datetime.now(zona_colombia).strftime("%Y-%m-%d %H:%M:%S")
        
        fila = [timestamp, nombre_imagen, etiqueta, f"{confianza * 100:.2f}%", APP_ENV]
        hoja.append_row(fila)
        print("✅ Predicción registrada en Google Sheets")

        # Guardar también en archivo TXT
        txt_filename = "predicciones_dev.txt" if APP_ENV == "dev" else "predicciones_prod.txt"
        with open(txt_filename, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} | {nombre_imagen} | {etiqueta} | {confianza:.4f} | {APP_ENV}\n")
        print(f"📄 Predicción guardada en {txt_filename}")

    except Exception as e:
        print("⚠️ Error al registrar en Sheets:")
        print(e)

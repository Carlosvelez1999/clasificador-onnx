import os
import gspread
import pytz
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta  
import traceback

# Ruta del archivo de credenciales
CREDENTIALS_PATH = "credentials/credentials.json"

# Alcances requeridos para usar Google Sheets
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Inicializar cliente de Google Sheets
credentials = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
client = gspread.authorize(credentials)

# ID de la hoja de cálculo (reemplaza por la tuya)
SHEET_ID = "1rWdlpUYMYgJRrCL9WCjzNL-0wS0pzI3zCcH3OJFnRVw"

# Nombre de la hoja dentro del archivo (ej. "Hoja 1")
SHEET_NAME = "Hoja 1"

def registrar_prediccion(nombre_imagen, etiqueta, confianza):
    try:
        hoja = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

        # Hora ajustada a Colombia (UTC−5)
        zona_colombia = pytz.timezone("America/Bogota")
        timestamp = datetime.now(zona_colombia).strftime("%Y-%m-%d %H:%M:%S")

        fila = [timestamp, nombre_imagen, etiqueta, f"{confianza * 100:.2f}%"]
        hoja.append_row(fila)
        print("✅ Predicción registrada en Google Sheets")
    except Exception as e:
        print("⚠️ Error al registrar en Sheets:")
        traceback.print_exc()

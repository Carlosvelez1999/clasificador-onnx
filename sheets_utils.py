import os
import gspread
import pytz
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta  
import traceback
import json

import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pytz
import json

# Leer JSON desde variable de entorno
json_str = os.getenv("GOOGLE_CREDENTIALS_JSON")
info = json.loads(json_str)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Inicializar cliente
credentials = Credentials.from_service_account_info(info, scopes=SCOPES)
client = gspread.authorize(credentials)

# Configuración de hoja
SHEET_ID = "1rWdlpUYMYgJRrCL9WCjzNL-0wS0pzI3zCcH3OJFnRVw"
SHEET_NAME = "Hoja 1"

def registrar_prediccion(nombre_imagen, etiqueta, confianza):
    try:
        hoja = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
        zona_colombia = pytz.timezone("America/Bogota")
        timestamp = datetime.now(zona_colombia).strftime("%Y-%m-%d %H:%M:%S")
        fila = [timestamp, nombre_imagen, etiqueta, f"{confianza * 100:.2f}%"]
        hoja.append_row(fila)
        print("✅ Predicción registrada en Google Sheets")
    except Exception as e:
        print("⚠️ Error al registrar en Sheets:")
        print(e)

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import urllib.parse
import gspread
from google.oauth2.service_account import Credentials

# --- GOOGLE SHEETS CONFIG ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1P8YJsjXVU3rqUH4zJx2vM0qtT43PsDfXuZ5nOhbW_sc"
SHEET_NAME = "Sheet1"

# 🔑 Credenciales embebidas directamente en el código
SERVICE_ACCOUNT_INFO = {
    "type": "service_account",
    "project_id": "proyectomillexsheet",
    "private_key_id": "1a4ae0b3a31e6741708886460a3675162d111f97",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkq...\n-----END PRIVATE KEY-----\n",
    "client_email": "mi-app-python@proyectomillexsheet.iam.gserviceaccount.com",
    "client_id": "116527539433049981352",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/mi-app-python%40proyectomillexsheet.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# Crear cliente de Google Sheets
try:
    credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
except Exception as e:
    st.error(f"❌ Error al conectar con Google Sheets: {e}")
    st.stop()

# --- INTERFAZ ---
st.set_page_config(page_title="Ruleta Mágica Millex", layout="wide")

# Pantalla completa para la ruleta
components.html("""
<html>
  <head>
    <style>
      html, body {
        margin: 0;
        padding: 0;
        height: 100%;
        width: 100%;
        overflow: hidden;
      }
      iframe {
        border: none;
        width: 100vw;
        height: 100vh;
        display: block;
      }
    </style>
  </head>
  <body>
    <iframe src="https://wheelofnames.com/es/kpz-yz7"></iframe>
  </body>
</html>
""", height=800, scrolling=False)

# Panel desplegable para cargar datos
with st.expander("🎁 Cargar datos del ganador", expanded=False):
    with st.form("formulario"):
        nombre = st.text_input("Nombre y apellido")
        razon = st.text_input("Razón social")
        whatsapp = st.text_input("WhatsApp (con código país)", placeholder="+549...")
        premio = st.selectbox("Premio ganado", ["", "10off", "20off", "25off", "5off", "Seguí participando"])
        enviar = st.form_submit_button("Enviar y guardar")

        if enviar:
            if nombre and razon and whatsapp and premio:
                try:
                    # Guardar en Google Sheets
                    fila = [nombre, razon, whatsapp, premio]
                    sheet.append_row(fila)
                    st.success("✅ Datos guardados correctamente en Google Sheets.")

                    # Enviar por WhatsApp
                    mensaje = f"¡Felicitaciones {nombre}! 🎉 Obtuviste el premio: *{premio}*. Presentá este mensaje para canjearlo."
                    link = f"https://wa.me/{whatsapp.strip()}?text={urllib.parse.quote(mensaje)}"
                    components.html(f"<script>window.open('{link}', '_blank')</script>", height=0)

                except Exception as e:
                    st.error(f"❌ Error al guardar en Google Sheets: {e}")
            else:
                st.warning("⚠️ Por favor completá todos los campos.")



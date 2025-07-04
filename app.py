import streamlit as st
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import pandas as pd
import urllib.parse
import streamlit.components.v1 as components

# Configuración
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1P8YJsjXVU3rqUH4zJx2vM0qtT43PsDfXuZ5nOhbW_sc"
SHEET_NAME = "Sheet1"

# Autenticación OAuth
def authenticate_gsheets():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials_oauth.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    client = gspread.authorize(creds)
    return client

# Inicializar cliente
client = authenticate_gsheets()
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# --- INTERFAZ ---
st.set_page_config(page_title="Ruleta Mágica Millex", layout="wide")

# Título pantalla completa
st.markdown("""
    <style>
        html, body, .block-container {
            height: 100%;
            margin: 0;
            padding: 0;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center;font-size:30px;font-weight:bold;">🎡 RULETA MÁGICA MILLEX 🎉</div>', unsafe_allow_html=True)

# Ruleta
components.html("""
<html>
  <head>
    <style>
      html, body {
        margin: 0;
        padding: 0;
        height: 100%;
        background: transparent;
      }
      iframe {
        width: 100%;
        height: 100%;
        border: none;
      }
    </style>
  </head>
  <body>
    <iframe src="https://wheelofnames.com/es/kpz-yz7"></iframe>
  </body>
</html>
""", height=800, scrolling=False)

# Formulario
with st.expander("🎁 Cargar datos del ganador"):
    nombre = st.text_input("Nombre y apellido")
    razon = st.text_input("Razón social")
    whatsapp = st.text_input("WhatsApp (con código país)", placeholder="+549...")
    premio = st.selectbox("Premio ganado", ["", "10off", "20off", "25off", "5off", "Seguí participando"])
    if st.button("Enviar y guardar"):
        if nombre and razon and whatsapp and premio:
            fila = [nombre, razon, whatsapp, premio]
            sheet.append_row(fila)
            st.success("✅ Datos guardados correctamente")
        else:
            st.warning("⚠️ Completá todos los campos.")




import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import urllib.parse
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# --- CONFIGURACIÓN GOOGLE SHEETS ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1P8YJsjXVU3rqUH4zJx2vM0qtT43PsDfXuZ5nOhbW_sc"
SHEET_NAME = "Sheet1"

credentials = Credentials.from_service_account_file("credenciales.json", scopes=SCOPES)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# --- Verifica si hay cabeceras, si no las agrega ---
cabeceras = sheet.row_values(1)
cabeceras_esperadas = ["Nombre y Apellido", "Razón Social", "WhatsApp", "Premio", "Fecha y hora"]
if cabeceras != cabeceras_esperadas:
    sheet.update("A1:E1", [cabeceras_esperadas])

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Ruleta Mágica Millex", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
<style>
    header, footer {visibility: hidden;}
    .block-container {padding: 0; margin: 0;}
    .title-container {
        background: rgba(0,0,0,0.9);
        padding: 16px 32px;
        text-align: center;
        color: white;
        font-family: 'Arial Black';
        font-size: 2.5rem;
        text-shadow: 1px 1px 4px rgba(255,255,255,0.5);
        border-bottom: 1px solid #333;
    }
    ::-webkit-scrollbar {
        width: 0px;
        background: transparent;
    }
</style>
""", unsafe_allow_html=True)

# --- TÍTULO ---
st.markdown('<div class="title-container">RULETA MÁGICA MILLEX</div>', unsafe_allow_html=True)

# --- RULETA (sin scroll ni marco) ---
components.html("""
<html>
  <head>
    <style>
      body {
        margin: 0;
        background: transparent;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
      }
      iframe {
        border: none;
        width: 600px;
        height: 600px;
        border-radius: 12px;
      }
    </style>
  </head>
  <body>
    <iframe src="https://wheelofnames.com/es/kpz-yz7"></iframe>
  </body>
</html>
""", height=620, scrolling=False)

# --- FORMULARIO DE GANADORES ---
with st.expander("🎁 Cargar datos del ganador", expanded=False):
    with st.form("formulario"):
        nombre = st.text_input("Nombre y apellido")
        razon = st.text_input("Razón social")
        whatsapp = st.text_input("WhatsApp (con código país)", placeholder="+549...")
        premio = st.selectbox("Premio ganado", ["", "10off", "20off", "25off", "5off", "Seguí participando"])
        enviar = st.form_submit_button("Enviar y guardar")

        if enviar:
            if nombre and razon and whatsapp and premio:
                fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                fila = [nombre, razon, whatsapp, premio, fecha_hora]
                sheet.append_row(fila)

                mensaje = f"¡Felicitaciones {nombre}! 🎉 Obtuviste el premio: *{premio}*. Presentá este mensaje para canjearlo."
                link = f"https://wa.me/{whatsapp.strip()}?text={urllib.parse.quote(mensaje)}"
                st.success("✅ Datos guardados correctamente. Abriendo WhatsApp...")
                components.html(f"<script>window.open('{link}', '_blank')</script>", height=0)
            else:
                st.warning("⚠️ Por favor completá todos los campos.")




import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import urllib.parse
from datetime import datetime
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
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCNY7Sug2b6mE44\nDUs9UWCluDjb4TspGAe1eyPHp+ux8kcWRuAknVzFZSg6hJsm9dL9ST3yazKGhogk\n7cQKS+AEIEbXCiyKmT+0Hlzrs+3lJp6peNrXilUgg0atG31+As0acTO0nSEzeY0F\nurPj+YVeZJqfuDQ7Kl1ZL6dLt8fFrw63N2/QptqmMU2N3/4Tf4PA/FnrxcXIyflQ\ni6gWrJZ++MbvMjJuL0u9Wu8ibHQIzeBenBklmXiejIgarY3uvhI36LtG+eFbEvz2\nOiicyRftTYPacJNxZeakz2Oqg+pqU/ry9xMUvkQs7dfZtAHXYz6cOZ4BkxoqjT2/\n97he2cxxAgMBAAECggEABoZp8b3VtE3wGi0e4ksNo0g/s4IO+WQHAwyWR6ILwhAU\n0MXflUD/5Yo4E49IG8GvhYnqRnRFBilSQiYI7JK42Wfl7QmmqZTN+FGIZ0ZL/c3M\n97RAoT7ck94LFnUU0wptDcHYqYaw4A/FftSxdZ1v1r3c1u8o1ewsF7AXz+pA2XIb\nsAMkDg6TNJlEO35RUd5qa8gm5pU/HxaKfbMwCsZP5px0lnG3M0el2SkSPlspq51n\nr+5AJMcOneJngZulpkaWEkA5uZjac59mgzHHt8QpPZTuRFccpNzIfXlJ0BRBFFt+\najY78jXG4EWKXtDH9K2x2P2CyNf9JqskcWKrIWbWeQKBgQDGPBCYwIxAZvUH2YQ3\nOUEqR/gr7Sl+f+0uHXlKc98QqwUAmLCi954eEVBSEVJ5uTimb48lTkQ8wBuFm8rG\ncmpxS9i3opznjqJjg0ssEv81eQ0lClyN69eWBeVJsJdfVzd1XH8StyknCQrhM0pi\nKAB5U9104xduqfs38eS3VtJ2HQKBgQC2lxkfVJxWLhkIfH2QlMZYRWDjvlrKXeyz\nJAhbhejulDqadaDzTINJSBYBiwlNETzVmsCZWzsLzBKEH7wz9gWk1FZwQLuZ/Fwa\nxid+FDsil54KJdS16wFwzina4wXLpam5Xw7R/IV9dXJAIa5Uhr6wkm8OC8EI2WCf\n5L+3AYOPZQKBgG+Hi67lZgM16dYowwJu7ALlyvKr1BSf1MmFO6Bv4Kh4D7BuN7L4\nrbUs+IuzwztIwl6hlV/f0PR9AP8Cz+smpExp59wpWS3OSf7C96Asb/mdyY91bO1M\nK1b0qjPzbrbtUv5ss/HLqxOTOtPJD6h56QpZ7Na+jYhtijHHnm6oInDhAoGABon0\nuV2DV8bA2L/0kzfwvnqFlMJdZ//jGStCLVznUZv3WU67G9tynC47s4RyKdNjNVcc\nbKGKxMpjI14rlETMQPHlwpFe5o3WEpNkGKzKzVtWqpBeRMGMxKhtcUxOCdP99wiD\ndFuxwCNzmv5ZyuckbxhfZ8Zd/F4kirVbdEdWmc0CgYAHcC7l8LZiVLnyf/jderZj\nKmO6Vcj0tg9+HYacV622pvBr9+3zx0m1TVnsK9V9vca39zMDHiBtkTMuhKB7MLT9\nFdr5kG/58hOjNNl5br6vPYUWmbLLTRQRAnBfuLAnL2fOOMdyouPPFjI2EU7MeuIn\nW8RoNRCC9kNICCEiSJ97lw==\n-----END PRIVATE KEY-----\n",
  "client_email": "mi-app-python@proyectomillexsheet.iam.gserviceaccount.com",
  "client_id": "116527539433049981352",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/mi-app-python%40proyectomillexsheet.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Crear las credenciales desde el diccionario
credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# --- INTERFAZ ---
st.set_page_config(page_title="Ruleta Mágica Millex", layout="wide")

# CSS personalizado
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
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown('<div class="title-container">RULETA MÁGICA MILLEX</div>', unsafe_allow_html=True)

# Ruleta centrada, grande y sin marco ni scroll
components.html("""
<html>
  <head>
    <style>
      body {
        margin: 0;
        overflow: hidden;
        background: transparent;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
      }
      iframe {
        border: none;
        border-radius: 12px;
        width: 600px;
        height: 600px;
        box-shadow: none;
        overflow: hidden;
        display: block;
      }
    </style>
  </head>
  <body>
    <iframe src="https://wheelofnames.com/es/kpz-yz7"></iframe>
  </body>
</html>
""", height=620, scrolling=False)

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
                # Guardar en Google Sheets
                fila = [nombre, razon, whatsapp, premio]
                sheet.append_row(fila)

                # Enviar por WhatsApp
                mensaje = f"¡Felicitaciones {nombre}! 🎉 Obtuviste el premio: *{premio}*. Presentá este mensaje para canjearlo."
                link = f"https://wa.me/{whatsapp.strip()}?text={urllib.parse.quote(mensaje)}"
                st.success("✅ Datos guardados correctamente. Abriendo WhatsApp...")
                components.html(f"<script>window.open('{link}', '_blank')</script>", height=0)
            else:
                st.warning("⚠️ Por favor completá todos los campos.")



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

# ✅ Credenciales embebidas en el código con formato correcto
SERVICE_ACCOUNT_INFO = {
  "type": "service_account",
  "project_id": "proyectomillexsheet",
  "private_key_id": "1a4ae0b3a31e6741708886460a3675162d111f97",
  "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCNY7Sug2b6mE44
DUs9UWCluDjb4TspGAe1eyPHp+ux8kcWRuAknVzFZSg6hJsm9dL9ST3yazKGhogk
7cQKS+AEIEbXCiyKmT+0Hlzrs+3lJp6peNrXilUgg0atG31+As0acTO0nSEzeY0F
urPj+YVeZJqfuDQ7Kl1ZL6dLt8fFrw63N2/QptqmMU2N3/4Tf4PA/FnrxcXIyflQ
i6gWrJZ++MbvMjJuL0u9Wu8ibHQIzeBenBklmXiejIgarY3uvhI36LtG+eFbEvz2
OiicyRftTYPacJNxZeakz2Oqg+pqU/ry9xMUvkQs7dfZtAHXYz6cOZ4BkxoqjT2/
97he2cxxAgMBAAECggEABoZp8b3VtE3wGi0e4ksNo0g/s4IO+WQHAwyWR6ILwhAU
0MXflUD/5Yo4E49IG8GvhYnqRnRFBilSQiYI7JK42Wfl7QmmqZTN+FGIZ0ZL/c3M
97RAoT7ck94LFnUU0wptDcHYqYaw4A/FftSxdZ1v1r3c1u8o1ewsF7AXz+pA2XIb
sAMkDg6TNJlEO35RUd5qa8gm5pU/HxaKfbMwCsZP5px0lnG3M0el2SkSPlspq51n
r+5AJMcOneJngZulpkaWEkA5uZjac59mgzHHt8QpPZTuRFccpNzIfXlJ0BRBFFt+
ajY78jXG4EWKXtDH9K2x2P2CyNf9JqskcWKrIWbWeQKBgQDGPBCYwIxAZvUH2YQ3
OUEqR/gr7Sl+f+0uHXlKc98QqwUAmLCi954eEVBSEVJ5uTimb48lTkQ8wBuFm8rG
cmpxS9i3opznjqJjg0ssEv81eQ0lClyN69eWBeVJsJdfVzd1XH8StyknCQrhM0pi
KAB5U9104xduqfs38eS3VtJ2HQKBgQC2lxkfVJxWLhkIfH2QlMZYRWDjvlrKXeyz
JAhbhejulDqadaDzTINJSBYBiwlNETzVmsCZWzsLzBKEH7wz9gWk1FZwQLuZ/Fwa
xid+FDsil54KJdS16wFwzina4wXLpam5Xw7R/IV9dXJAIa5Uhr6wkm8OC8EI2WCf
5L+3AYOPZQKBgG+Hi67lZgM16dYowwJu7ALlyvKr1BSf1MmFO6Bv4Kh4D7BuN7L4
rbUs+IuzwztIwl6hlV/f0PR9AP8Cz+smpExp59wpWS3OSf7C96Asb/mdyY91bO1M
K1b0qjPzbrbtUv5ss/HLqxOTOtPJD6h56QpZ7Na+jYhtijHHnm6oInDhAoGABon0
uV2DV8bA2L/0kzfwvnqFlMJdZ//jGStCLVznUZv3WU67G9tynC47s4RyKdNjNVcc
bKGKxMpjI14rlETMQPHlwpFe5o3WEpNkGKzKzVtWqpBeRMGMxKhtcUxOCdP99wiD
dFuxwCNzmv5ZyuckbxhfZ8Zd/F4kirVbdEdWmc0CgYAHcC7l8LZiVLnyf/jderZj
KmO6Vcj0tg9+HYacV622pvBr9+3zx0m1TVnsK9V9vca39zMDHiBtkTMuhKB7MLT9
Fdr5kG/58hOjNNl5br6vPYUWmbLLTRQRAnBfuLAnL2fOOMdyouPPFjI2EU7MeuIn
W8RoNRCC9kNICCEiSJ97lw==
-----END PRIVATE KEY-----""",
  "client_email": "mi-app-python@proyectomillexsheet.iam.gserviceaccount.com",
  "client_id": "116527539433049981352",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/mi-app-python%40proyectomillexsheet.iam.gserviceaccount.com",
}

# Autenticación
credentials = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# --- INTERFAZ ---
st.set_page_config(page_title="Ruleta Mágica Millex", layout="wide")

# Título en pantalla completa
st.markdown(
    """
    <style>
        html, body, .block-container {
            height: 100%;
            margin: 0;
            padding: 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Ruleta a pantalla completa
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

# Formulario para guardar datos
with st.expander("🎁 Cargar datos del ganador"):
    nombre = st.text_input("Nombre y apellido")
    razon = st.text_input("Razón social")
    whatsapp = st.text_input("WhatsApp (con código país)", placeholder="+549...")
    premio = st.selectbox("Premio ganado", ["", "10off", "20off", "25off", "5off", "Seguí participando"])
    if st.button("Enviar y guardar"):
        if nombre and razon and whatsapp and premio:
            fila = [nombre, razon, whatsapp, premio]
            try:
                sheet.append_row(fila)
                st.success("✅ Datos guardados correctamente")
            except Exception as e:
                st.error(f"❌ Error al guardar: {e}")
        else:
            st.warning("⚠️ Completá todos los campos.")




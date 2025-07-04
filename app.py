import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import urllib.parse
import requests

# --- GOOGLE SHEETS CONFIG ---
SPREADSHEET_ID = "1P8YJsjXVU3rqUH4zJx2vM0qtT43PsDfXuZ5nOhbW_sc"
SHEET_NAME = "Sheet1"

# URL para la API de Google Sheets (modo sin OAuth)
API_URL = f"https://docs.google.com/forms/d/e/{SPREADSHEET_ID}/formResponse"

def guardar_datos(nombre, razon, whatsapp, premio):
    try:
        # Agregá los datos como fila
        new_row = [[nombre, razon, whatsapp, premio]]
        df = pd.DataFrame(new_row)
        csv_content = df.to_csv(index=False, header=False)
        requests.post(
            f"https://sheetdb.io/api/v1/YOUR_API_KEY",
            json={"data": new_row}
        )
        return True
    except Exception as e:
        st.error(f"❌ Error al guardar: {e}")
        return False

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
                exito = guardar_datos(nombre, razon, whatsapp, premio)
                if exito:
                    mensaje = f"¡Felicitaciones {nombre}! 🎉 Obtuviste el premio: *{premio}*. Presentá este mensaje para canjearlo."
                    link = f"https://wa.me/{whatsapp.strip()}?text={urllib.parse.quote(mensaje)}"
                    st.success("✅ Datos guardados correctamente. Abriendo WhatsApp...")
                    components.html(f"<script>window.open('{link}', '_blank')</script>", height=0)
            else:
                st.warning("⚠️ Por favor completá todos los campos.")



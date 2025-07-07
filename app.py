import streamlit as st
import urllib.parse
import requests
import json
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="Ruleta Mágica Millex", layout="wide")

GOOGLE_APPS_SCRIPT_WEBAPP_URL = "https://script.google.com/macros/s/AKfycbxGthdziUjWC3jB5_0YBDfnXCcTBj-7RGD2W4_mf5I/exec"

# CSS + Título + Ruleta
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
::-webkit-scrollbar {display: none;}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="title-container">RULETA MÁGICA MILLEX</div>', unsafe_allow_html=True)
components.html("""
<html>
  <head>
    <style>
      html, body {
        margin: 0; height: 100%; overflow: hidden; background: transparent;
        display: flex; justify-content: center; align-items: center;
      }
      iframe {
        border: none; width: 600px; height: 600px; border-radius: 12px;
      }
    </style>
  </head>
  <body>
    <iframe src="https://wheelofnames.com/es/kpz-yz7"></iframe>
  </body>
</html>
""", height=620, scrolling=False)

# Formulario
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

                data = {
                    "nombre": nombre,
                    "razon": razon,
                    "whatsapp": whatsapp,
                    "premio": premio,
                    "fecha_hora": fecha_hora
                }

                headers = {"Content-Type": "application/json"}
                res = requests.post(GOOGLE_APPS_SCRIPT_WEBAPP_URL, data=json.dumps(data), headers=headers)

                if res.status_code == 200:
                    st.success("✅ Datos guardados correctamente en Google Sheet.")
                else:
                    st.error(f"❌ Error al guardar en Google Sheet. Código: {res.status_code}, Respuesta: {res.text}")

                mensaje = f"¡Felicitaciones {nombre}! 🎉 Obtuviste el premio: *{premio}*. Presentá este mensaje para canjearlo."
                link = f"https://wa.me/{whatsapp.strip()}?text={urllib.parse.quote(mensaje)}"
                st.markdown(f"[Abrir WhatsApp para enviar mensaje]({link})", unsafe_allow_html=True)
            else:
                st.warning("⚠️ Por favor completá todos los campos.")




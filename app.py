import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import requests

# Nueva URL pública de Google Apps Script Web App
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzky9Nqrs7V2ly8_SnccOD5Ytw9W5DC0byQpR_iNfGMwYNYpaRQv_Pk8ALvKvcSeAO8/exec"

st.set_page_config(page_title="Ruleta Mágica Millex", layout="wide")

# Estilos
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
    ::-webkit-scrollbar { display: none; }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown('<div class="title-container">RULETA MÁGICA MILLEX</div>', unsafe_allow_html=True)

# Ruleta
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
                datos = {
                    "nombre": nombre,
                    "razonSocial": razon,
                    "whatsapp": whatsapp,
                    "premio": premio
                }
                try:
                    # Enviar datos al Apps Script como parámetros
                    respuesta = requests.get(WEB_APP_URL, params=datos)
                    if respuesta.status_code == 200 and "ok" in respuesta.text.lower():
                        mensaje = f"¡Felicitaciones {nombre}! 🎉 Obtuviste el premio: *{premio}*. Presentá este mensaje para canjearlo."
                        link = f"https://wa.me/{whatsapp.strip()}?text={urllib.parse.quote(mensaje)}"
                        st.success("✅ Datos guardados correctamente. Abriendo WhatsApp...")
                        components.html(f"<script>window.open('{link}', '_blank')</script>", height=0)
                    else:
                        st.error("❌ Error al guardar los datos en Google Sheets.")
                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}")
            else:
                st.warning("⚠️ Por favor completá todos los campos.")




import streamlit as st
import streamlit.components.v1 as components
import gspread

# ID de la hoja de cálculo pública
SPREADSHEET_ID = "1P8YJsjXVU3rqUH4zJx2vM0qtT43PsDfXuZ5nOhbW_sc"
SHEET_NAME = "Sheet1"

# Conexión anónima (solo funciona si la hoja es pública)
gc = gspread.Client(auth=None)
sheet = gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# --- UI ---
st.set_page_config(page_title="Ruleta Mágica Millex", layout="wide")

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
            try:
                sheet.append_row(fila)
                st.success("✅ Datos guardados correctamente")
            except Exception as e:
                st.error(f"❌ Error al guardar: {e}")
        else:
            st.warning("⚠️ Completá todos los campos.")





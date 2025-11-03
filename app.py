import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import requests

# URL actualizada de tu Apps Script
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxTX0rNV7sXquRIS1Q_Pc7ZsRkiQpTHzMfHWb5ROf3muJGGBnY_J2juYEqNGJw4CC2x/exec"

# Configuración de la página
st.set_page_config(page_title="Ruleta Mágica Petsu", layout="wide", initial_sidebar_state="collapsed")

# --- Estilos personalizados ---
st.markdown("""
    <style>
        body {
            background-color: #fff8f2;
            font-family: 'Montserrat', sans-serif;
        }
        h1 {
            color: #f57c00;
            text-align: center;
            font-weight: 700;
        }
        .stButton>button {
            background-color: #f57c00;
            color: white;
            font-weight: 600;
            border-radius: 10px;
            padding: 0.6em 1.2em;
        }
        .stButton>button:hover {
            background-color: #ff9800;
            color: white;
        }
        .stExpander {
            background-color: #fff3e0 !important;
            border-radius: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Listas ---
PROVINCIAS_ARGENTINA = [
    "Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", 
    "Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa", 
    "La Rioja", "Mendoza", "Misiones", "Neuquén", "Río Negro", 
    "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", 
    "Santiago del Estero", "Tierra del Fuego", "Tucumán"
]

INTERESES = ["Perro", "Gato", "Roedores", "Aves", "Acuario"]

CATEGORIAS_PRODUCTOS = [
    "JUGUETES PARA PERROS", "JUGUETES PARA GATOS", "CAMAS Y CUIDADO",
    "ACCESORIOS DE PASEO", "ALIMENTACIÓN Y COMEDEROS", "ACCESORIOS VARIOS"
]

# --- Encabezado ---
st.markdown('<h1>🎯 RULETA MÁGICA PETSU 🎯</h1>', unsafe_allow_html=True)
st.markdown("""
<p style='text-align:center; color:#333; font-size:18px;'>
Gir&aacute; la ruleta y descubr&iacute; tu premio 🎁<br>
Descuentos, juguetes y sorpresas para vos y tu mascota 🐶🐱
</p>
""", unsafe_allow_html=True)

# --- Ruleta incrustada ---
st.markdown("""
<div style="display:flex; justify-content:center; align-items:center; margin-top:20px;">
    <iframe src="https://wheelofnames.com/es/vug-z3k" width="600" height="600" style="border:none; border-radius:20px;"></iframe>
</div>
""", unsafe_allow_html=True)

# --- Formulario ---
with st.expander("🎁 CARGAR DATOS DEL GANADOR", expanded=False):
    with st.form("formulario", clear_on_submit=True):
        nombre = st.text_input("Nombre y apellido")
        razon_social = st.text_input("Razón social (opcional)")
        nombre_fantasia = st.text_input("Nombre de fantasía")
        cuil_cuit = st.text_input("Número de CUIL o CUIT")
        whatsapp = st.text_input("WhatsApp (con código país)", placeholder="+549...")
        cliente_tipo = st.radio("¿Es cliente nuevo o actual?", ["Nuevo", "Actual"])
        cliente_estrella = st.radio("¿Es cliente estrella?", ["Sí", "No"])
        tipo_cliente = st.selectbox("Tipo de cliente", ["Pet Shop", "Veterinaria", "Distribuidora", "Otro"])
        provincia = st.selectbox("Provincia", PROVINCIAS_ARGENTINA)
        interes_principal = st.multiselect("Interés principal", INTERESES)
        categorias_productos = st.multiselect("Categorías de productos", CATEGORIAS_PRODUCTOS)
        marcas = st.multiselect("Marcas que maneja", ["GiGwi", "AFP", "Beeztees", "Flexi", "Boyu", "Shanda", "Dayang", "The Pets", "Otros"])
        
        # Premios adaptados Petsu
        premio = st.selectbox("Premio ganado", [
            "5% de descuento",
            "10% de descuento",
            "15% de descuento",
            "20% de descuento",
            "25% de descuento",
            "Juguete de regalo",
            "Seguí participando"
        ])

        enviar = st.form_submit_button("🎯 ENVIAR Y GUARDAR DATOS")

        if enviar:
            datos = {
                "Nombre y Apellido": nombre,
                "Razon Social": razon_social,
                "Nombre Fantasía": nombre_fantasia,
                "CUIL/CUIT": cuil_cuit,
                "whatsapp": whatsapp,
                "Cliente Tipo": cliente_tipo,
                "Cliente Estrella": cliente_estrella,
                "Tipo Cliente": tipo_cliente,
                "Provincia": provincia,
                "Interés Principal": ", ".join(interes_principal),
                "Categorías Productos": ", ".join(categorias_productos),
                "Marcas": ", ".join(marcas),
                "Premio ganado": premio
            }

            try:
                headers = {'Content-Type': 'application/json'}
                respuesta = requests.post(WEB_APP_URL, json=datos, headers=headers)
                respuesta.raise_for_status()

                try:
                    respuesta_json = respuesta.json()
                    if respuesta_json.get("status") in ["success", "ok"]:
                        mensaje = f"🎉 ¡Felicitaciones {nombre}! Obtuviste: *{premio}*. Presentá este mensaje para canjearlo en Petsu."
                        whatsapp_limpio = whatsapp.strip().replace(" ", "").replace("-", "")
                        link = f"https://wa.me/{whatsapp_limpio}?text={urllib.parse.quote(mensaje)}"
                        st.success("✅ ¡Datos guardados correctamente!")
                        st.markdown(f"[📱 Abrir conversación de WhatsApp]({link})", unsafe_allow_html=True)
                    else:
                        st.error(f"❌ Error: {respuesta_json.get('message', 'Error desconocido')}")
                except ValueError:
                    st.error("❌ La respuesta del servidor no es JSON válido.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error de conexión: {str(e)}")





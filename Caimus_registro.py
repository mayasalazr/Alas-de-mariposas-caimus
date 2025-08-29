import streamlit as st
import pandas as pd
from datetime import datetime

url ="https://docs.google.com/spreadsheets/d/e/2PACX-1vRiqSoTatlwg9RCNUP1XUzNEV2GWW9a0CdiuUJedH148If1EgY2HGyoI0n-qxOrLQrH-V2PsjM0_Gzo/pub?output=csv"
df = pd.read_csv(url)

def load_data():
    return pd.read_csv(url)

df = load_data()

st.title("📊 CAIMUS - Población Beneficiada")

# Mostrar tabla
st.subheader("📋 Base de datos actual")
st.dataframe(df, use_container_width=True)

# Formulario
st.subheader("📝 Ingresar nuevo registro")

with st.form("nuevo_registro", clear_on_submit=True):
    # Datos generales
    dia = st.date_input("📅 Día", datetime.today())
    departamento = st.text_input("Departamento")
    municipio = st.text_input("Municipio")
    no_caso = st.text_input("Número de caso")
    fecha_nac = st.date_input("Fecha de nacimiento")
    edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
    nombre = st.text_input("Nombre y Apellido")
    dpi = st.text_input("DPI")

    # Género
    genero = st.radio("Género", ["M", "H"])

    # Rangos de edad (marcar uno)
    rango_edad = st.radio("Rango de Edad", ["0 a 13 años", "14 a 30 años", "31 a 60 años", "Mayores de 60 años"])

    # Grupo étnico
    grupo_etnico = st.selectbox("Grupo Étnico", ["Maya", "Xinca", "Garífuna", "Ladino", "Otro"])

    # Ubicación y tipología
    ubicacion = st.text_input("Ubicación Geográfica")
    tipologia = st.text_input("Tipología 22-2008")

    # Botón de guardar
    submitted = st.form_submit_button("➕ Guardar registro")

    if submitted:
        # Validar que no haya campos vacíos
        if not all([departamento, municipio, no_caso, nombre, dpi, ubicacion, tipologia]):
            st.error("❌ Por favor llena todos los campos obligatorios.")
        else:
            nuevo = {
                "Día": dia.strftime("%Y-%m-%d"),
                "Departamento": departamento,
                "Municipio": municipio,
                "No. de caso": no_caso,
                "Fecha de Nacimiento": fecha_nac.strftime("%Y-%m-%d"),
                "Edad": edad,
                "Nombre y Apellido": nombre,
                "DPI": dpi,
                "Genero": genero,
                "Rango Edad": rango_edad,
                "Grupo Étnico": grupo_etnico,
                "Ubicación Geográfica": ubicacion,
                "Tipología 22-2008": tipologia
            }

            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)

            st.success("✅ Registro agregado correctamente (en memoria).")
            st.dataframe(df, use_container_width=True)
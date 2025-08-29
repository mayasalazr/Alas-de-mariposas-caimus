
import streamlit as st
import pandas as pd
from datetime import datetime

# URL de la hoja de cálculo de Google publicada como CSV
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRiqSoTatlwg9RCNUP1XUzNEV2GWW9a0CdiuUJedH148If1EgY2HGyoI0n-qxOrLQrH-V2PsjM0_Gzo/pub?gid=1666377556&single=true&output=csv"

# --- FUNCIÓN PARA CARGAR DATOS ---
# Es una buena práctica encapsular la carga de datos en una función con caché
@st.cache_data
def load_data(url):
    """Carga los datos desde la URL y especifica tipos de datos para evitar errores."""
    # Especificamos 'DPI' y 'No. de caso' como string (object) para conservar ceros a la izquierda
    df = pd.read_csv(url, dtype={'DPI': str, 'No. de caso': str})
    return df

# --- INICIALIZACIÓN DEL ESTADO DE LA SESIÓN ---
# Se carga el DataFrame en el estado de la sesión solo la primera vez que se ejecuta el script.
if "df" not in st.session_state:
    st.session_state.df = load_data(url)

# --- INTERFAZ DE USUARIO ---
st.title("📊 CAIMUS - Población Beneficiada")

# Mostrar la tabla directamente desde session_state
st.subheader("📋 Base de datos actual")
st.dataframe(st.session_state.df, use_container_width=True)

# Formulario para ingresar nuevos registros
st.subheader("📝 Ingresar nuevo registro")
with st.form("nuevo_registro_form", clear_on_submit=True):
    # Definimos las columnas para un diseño más limpio
    col1, col2 = st.columns(2)

    with col1:
        departamento = st.text_input("Departamento")
        no_caso = st.text_input("Número de caso")
        nombre = st.text_input("Nombre y Apellido")
        genero = st.radio("Género", ["M", "H"], horizontal=True)
        grupo_etnico = st.selectbox("Grupo Étnico", ["Maya", "Xinca", "Garífuna", "Ladino", "Otro"])
        tipologia = st.text_input("Tipología 22-2008")

    with col2:
        municipio = st.text_input("Municipio")
        fecha_nac = st.date_input("Fecha de nacimiento")
        dpi = st.text_input("DPI (si aplica)")
        edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
        rango_edad = st.radio("Rango de Edad", ["0 a 13 años", "14 a 30 años", "31 a 60 años", "Mayores de 60 años"])
        ubicacion = st.text_input("Ubicación Geográfica")

    # Botón para enviar el formulario
    submitted = st.form_submit_button("➕ Guardar registro")

    if submitted:
        # Validación de campos obligatorios
        campos_obligatorios = [departamento, municipio, no_caso, nombre, ubicacion, tipologia]
        if not all(campos_obligatorios):
            st.error("❌ Por favor, llena todos los campos obligatorios.")
        else:
            # Creación del nuevo registro como un DataFrame de una fila
            nuevo_registro = pd.DataFrame([{
                "Día": datetime.today().strftime("%Y-%m-%d"),
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
            }])

            # Concatenar el DataFrame existente con el nuevo registro
            st.session_state.df = pd.concat([st.session_state.df, nuevo_registro], ignore_index=True)
            
            st.success("✅ ¡Registro agregado exitosamente!")
            
            # (Opcional) Forzar un re-run del script para limpiar todo y mostrar la tabla actualizada arriba.
            # st.rerun() # Descomentar si quieres forzar la recarga de inmediato.
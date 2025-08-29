import streamlit as st
import pandas as pd

url ="https://docs.google.com/spreadsheets/d/e/2PACX-1vRiqSoTatlwg9RCNUP1XUzNEV2GWW9a0CdiuUJedH148If1EgY2HGyoI0n-qxOrLQrH-V2PsjM0_Gzo/pub?output=csv"
df = pd.read_csv(url)

def load_data():
    return pd.read_csv(url)

df = load_data()

st.title("📊 CAIMUS - Población Beneficiada")

# --- Mostrar tabla ---
st.subheader("📋 Base de datos actual")
st.dataframe(df, use_container_width=True)

# --- Buscar registros ---
st.subheader("🔍 Buscar registros")
col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("Buscar por nombre")
    if nombre and "Nombre" in df.columns:
        result = df[df["Nombre"].str.contains(nombre, case=False, na=False)]
        st.dataframe(result, use_container_width=True)

with col2:
    if "Tipo de Violencia" in df.columns:
        violencia = st.selectbox("Buscar por tipo de violencia", [""] + df["Tipo de Violencia"].dropna().unique().tolist())
        if violencia:
            result = df[df["Tipo de Violencia"] == violencia]
            st.dataframe(result, use_container_width=True)

# --- Formulario dinámico ---
st.subheader("📝 Ingresar nuevo registro")

with st.form("nuevo_registro", clear_on_submit=True):
    nuevo_registro = {}
    for col in df.columns:
        # Generar input según tipo de dato
        if df[col].dtype == "int64" or df[col].dtype == "float64":
            nuevo_registro[col] = st.number_input(col, step=1)
        else:
            nuevo_registro[col] = st.text_input(col)

    submitted = st.form_submit_button("➕ Guardar registro")

    if submitted:
        df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
        st.success("✅ Registro agregado (en memoria, aún no guardado en Google Sheets).")
        st.dataframe(df, use_container_width=True)
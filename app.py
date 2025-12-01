import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image

# ============================
# 🔧 CONFIGURACIÓN GENERAL
# ============================
st.set_page_config(
    page_title="Dashboard Biomédico – Troponina",
    layout="wide",
    page_icon="🧬",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 48px;
        font-weight: 900;
        text-align: center;
        color: #4A90E2;
        margin-bottom: -10px;
    }
    .subtitle {
        text-align: center;
        color: #6B6B6B;
        font-size: 20px;
        margin-bottom: 30px;
    }
    .card {
        padding: 20px;
        background: white;
        border-radius: 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .upload-box {
        border: 3px dashed #4A90E2;
        padding: 35px;
        border-radius: 18px;
        text-align: center;
        background: #F7FBFF;
    }
    .metric-card {
        background: #F0F8FF;
        padding: 20px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================
# 🎨 TÍTULO PRINCIPAL
# ============================
st.markdown('<h1 class="main-title">Dashboard de Análisis de Troponina (cTnI)</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Visualización profesional para análisis clínico y bioinformático</p>', unsafe_allow_html=True)

# Imagen de referencia (sin copyright, ejemplo genérico)
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Troponin.png/640px-Troponin.png", width=350)

st.write("---")

# ============================
# 📁 SUBIR ARCHIVO
# ============================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📤 Cargar archivo CSV de datos de Troponina")
st.markdown('<div class="upload-box">', unsafe_allow_html=True)
file = st.file_uploader("Sube un archivo CSV (máx. 200MB)", type=["csv"])
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if file:
    df = pd.read_csv(file)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Vista Preliminar de los Datos")
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ============================
    # 📈 GRÁFICAS PRINCIPALES
    # ============================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📈 Distribución de Troponina")

    numeric_cols = df.select_dtypes(include=["int", "float"]).columns.tolist()

    if numeric_cols:
        selected = st.selectbox("Selecciona la columna de Troponina:", numeric_cols)

        fig = px.histogram(df, x=selected, nbins=30, title=f"Distribución de {selected}")
        st.plotly_chart(fig, use_container_width=True)

        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Media", f"{df[selected].mean():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Mediana", f"{df[selected].median():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Máximo", f"{df[selected].max():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ============================
    # 📉 Gráfica de Línea
    # ============================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📉 Tendencia de Troponina en el Tiempo")

    if len(numeric_cols) >= 1:
        time_col = st.selectbox("Columna de tiempo (opcional)", df.columns)
        value_col = st.selectbox("Columna de valores", numeric_cols)

        fig2 = px.line(df, x=time_col, y=value_col, title=f"Tendencia temporal de {value_col}")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ============================
    # 🔬 Interpretación simple
    # ============================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧪 Interpretación Clínica Simplificada")

    st.info(
        "**Niveles elevados de Troponina I (cTnI)** suelen asociarse con daño cardíaco agudo, incluyendo infarto del miocardio, sepsis o miocarditis."
    )

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.warning("Sube un archivo CSV para comenzar.")




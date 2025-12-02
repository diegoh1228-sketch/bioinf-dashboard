# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# ---------- Config ----------
st.set_page_config(page_title="Dashboard Troponina (cTnI) - Profesional",
                   page_icon="🫀",
                   layout="wide")

# ---------- Styles ----------
st.markdown("""
<style>
.header { font-size:36px; font-weight:700; color:#b71c1c; }
.card { background: #fff; padding:14px; border-radius:12px; box-shadow: 0 6px 18px rgba(0,0,0,0.06); }
.small { font-size:14px; color:#555; }
.metric { background: linear-gradient(90deg,#fff5f5,#fff); padding:12px; border-radius:10px; }
.upload-box { border:2px dashed #ef9a9a; padding:18px; border-radius:12px; background:#fff7f7; text-align:center; }
</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown('<div class="header">Dashboard Profesional — Troponina cardíaca (cTnI)</div>', unsafe_allow_html=True)
st.markdown('**Interfaz interactiva** para explorar niveles de troponina, datos clínicos y visualizaciones de la proteína.')

st.write("---")

# ---------- Default dataset generator ----------
def generate_default_df(n=60, seed=42):
    np.random.seed(seed)
    start = datetime(2025, 1, 1)

    ids = list(range(1, n+1))
    edades = np.random.randint(18, 90, n)
    sexos = np.random.choice(["Masculino", "Femenino"], n)

    troponina = np.round(np.concatenate([
        np.random.beta(1.5, 50, int(n*0.75)) * 0.05,
        np.random.beta(2, 5, n - int(n*0.75)) * 3.0
    ]), 3)
    np.random.shuffle(troponina)

    diagnosticos = []
    for v in troponina:
        if v < 0.014:
            diagnosticos.append("Normal")
        elif v < 0.05:
            diagnosticos.append("Riesgo Moderado")
        elif v < 0.5:
            diagnosticos.append("Sospecha de daño")
        else:
            diagnosticos.append("Probable Infarto")

    fechas = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(n)]

    return pd.DataFrame({
        "Paciente_ID": ids,
        "Edad": edades,
        "Sexo": sexos,
        "Troponina_cTnI_ng_mL": troponina,
        "Diagnóstico": diagnosticos,
        "Fecha": fechas
    })

# ---------- Load default dataset ----------
df_default = generate_default_df()

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Datos")
    file = st.file_uploader("Sube un archivo CSV (opcional)", type=["csv"])
    use_default = st.checkbox("Usar solo el dataset por defecto", value=True)

    st.markdown("### Filtros")
    sexo_filtro = st.multiselect("Sexo:", ["Masculino", "Femenino"], default=["Masculino", "Femenino"])
    edad_min, edad_max = st.slider("Edad", 18, 90, (18, 90))

# ---------- Load Data ----------
if use_default:
    df = df_default.copy()
else:
    if file:
        df = pd.read_csv(file)
    else:
        df = df_default.copy()

# Safety check
if "Troponina_cTnI_ng_mL" not in df.columns:
    st.error("El CSV debe incluir la columna 'Troponina_cTnI_ng_mL'.")
    st.stop()

# Filters
df = df[df["Sexo"].isin(sexo_filtro)]
df = df[(df["Edad"] >= edad_min) & (df["Edad"] <= edad_max)]

# ---------- Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Exploración", "📈 Análisis", "📘 Información clínica", "🧬 Visualizar proteína"])

# ---------- TAB 1 EXPLORACIÓN ----------
with tab1:
    st.subheader("📊 Exploración del Dataset")
    st.dataframe(df, use_container_width=True)

    # Scatter plot
    st.markdown("### Troponina vs Edad")
    fig = px.scatter(df, x="Edad", y="Troponina_cTnI_ng_mL",
                     color="Diagnóstico",
                     size="Troponina_cTnI_ng_mL",
                     hover_data=["Paciente_ID", "Sexo", "Fecha"],
                     title="Relación Troponina–Edad")
    st.plotly_chart(fig, use_container_width=True)

# ---------- TAB 2 ANÁLISIS ----------
with tab2:
    st.subheader("📈 Análisis estadístico")

    col1, col2, col3 = st.columns(3)
    col1.metric("Media (ng/mL)", f"{df['Troponina_cTnI_ng_mL'].mean():.3f}")
    col2.metric("Mediana (ng/mL)", f"{df['Troponina_cTnI_ng_mL'].median():.3f}")
    col3.metric("Máximo (ng/mL)", f"{df['Troponina_cTnI_ng_mL'].max():.3f}")

    st.markdown("### Distribución de troponina")
    fig2 = px.histogram(df, x="Troponina_cTnI_ng_mL", nbins=40, color="Diagnóstico")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Boxplot por diagnóstico")
    fig3 = px.box(df, x="Diagnóstico", y="Troponina_cTnI_ng_mL", points="all")
    st.plotly_chart(fig3, use_container_width=True)

# ---------- TAB 3 INFO CLÍNICA ----------
with tab3:
    st.subheader("📘 Información sobre la Troponina Cardíaca (cTnI)")
    st.markdown("""
    La **troponina cardíaca** es un biomarcador fundamental para evaluar daño al músculo cardíaco.
    Valores elevados sugieren daño miocárdico, incluyendo **infarto agudo al miocardio (IAM)**.
    """)

    st.markdown("### Imágenes explicativas")

    st.image("https://raw.githubusercontent.com/MChevi/biomedia-assets/main/troponin_complex.png",
             caption="Complejo de Troponina (I, T y C)", width=400)

    st.image("https://raw.githubusercontent.com/MChevi/biomedia-assets/main/heart_anterior.png",
             caption="Vista anatómica del corazón", width=420)

# ---------- TAB 4 PROTEÍNA ----------
with tab4:
    st.subheader("🧬 Visualización de la proteína Troponina")

    st.markdown("Modelo molecular ilustrativo:")
    st.image("https://raw.githubusercontent.com/MChevi/biomedia-assets/main/molecular_model.png",
             caption="Modelo molecular de la Troponina", width=360)

    st.markdown("Estructura en el músculo y filamentos:")
    st.image("https://raw.githubusercontent.com/MChevi/biomedia-assets/main/muscle_structure.png",
             caption="Estructura del sarcómero con troponina", width=520)

st.write("---")
st.markdown("Dashboard profesional creado para análisis y visualización de troponina cardíaca (cTnI).")




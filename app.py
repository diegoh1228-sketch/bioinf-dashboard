import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Ultra Pro - Troponina",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# DATASET POR DEFECTO
# ---------------------------------------------------------
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 60
    df = pd.DataFrame({
        "Paciente_ID": range(1, n+1),
        "Edad": np.random.randint(20, 90, n),
        "Troponina_ng_mL": np.round(np.random.uniform(0.01, 12, n), 2)
    })
    
    # Clasificación automática
    condiciones = [
        df["Troponina_ng_mL"] < 0.04,
        df["Troponina_ng_mL"].between(0.04, 0.4),
        df["Troponina_ng_mL"].between(0.4, 1),
        df["Troponina_ng_mL"].between(1, 5),
        df["Troponina_ng_mL"] > 5
    ]
    categorias = ["Normal", "Leve", "Moderado", "Alto", "Crítico"]
    df["Diagnóstico"] = np.select(condiciones, categorias)
    return df

df = load_data()

# ---------------------------------------------------------
# SIDEBAR (controls)
# ---------------------------------------------------------
st.sidebar.title("Configuración")
seccion = st.sidebar.radio(
    "Selecciona una sección:",
    ["📊 Análisis Interactivo", "📈 Gráficas Avanzadas", "📚 Información Médica", "🧬 Troponina - Detalles Proteicos"]
)

st.sidebar.write("---")
st.sidebar.subheader("Filtros Globales")

# Filtro de rango de troponina
rango_trop = st.sidebar.slider(
    "Rango de troponina (ng/mL)",
    float(df.Troponina_ng_mL.min()),
    float(df.Troponina_ng_mL.max()),
    (float(df.Troponina_ng_mL.min()), float(df.Troponina_ng_mL.max()))
)

# Filtro diagnóstico
dx_filtro = st.sidebar.multiselect(
    "Filtrar por diagnóstico:",
    options=df["Diagnóstico"].unique(),
    default=df["Diagnóstico"].unique()
)

# Aplicar filtros globales
df_f = df[
    (df["Troponina_ng_mL"].between(rango_trop[0], rango_trop[1])) &
    (df["Diagnóstico"].isin(dx_filtro))
]

# ---------------------------------------------------------
# SECCIÓN: ANÁLISIS INTERACTIVO
# ---------------------------------------------------------
if seccion == "📊 Análisis Interactivo":
    st.title("📊 Análisis Interactivo de Troponina")

    st.subheader("📌 Dataset Filtrado")
    st.caption("El dataset cambia dinámicamente con los filtros del sidebar.")
    st.dataframe(df_f, use_container_width=True)

    # Estadísticas
    st.subheader("📈 Estadísticas Rápidas")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Promedio", f"{df_f.Troponina_ng_mL.mean():.2f} ng/mL")
    col2.metric("Máximo", f"{df_f.Troponina_ng_mL.max():.2f} ng/mL")
    col3.metric("Mínimo", f"{df_f.Troponina_ng_mL.min():.2f} ng/mL")
    col4.metric("Pacientes", len(df_f))

# ---------------------------------------------------------
# SECCIÓN: GRÁFICAS AVANZADAS
# ---------------------------------------------------------
elif seccion == "📈 Gráficas Avanzadas":
    st.title("📈 Gráficas Avanzadas de Troponina")

    # Barplot
    st.subheader("Distribución por Diagnóstico")
    fig = px.box(
        df_f,
        x="Diagnóstico",
        y="Troponina_ng_mL",
        points="all",
        title="Distribución de troponina por categoría diagnóstica"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Scatter edad vs troponina
    st.subheader("Edad vs Troponina (Scatter interactivo)")
    fig2 = px.scatter(
        df_f,
        x="Edad",
        y="Troponina_ng_mL",
        size="Troponina_ng_mL",
        color="Diagnóstico",
        hover_data=["Paciente_ID"],
        title="Relación entre Edad y Niveles de Troponina"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Histograma
    st.subheader("Histograma de Troponina")
    fig3 = px.histogram(
        df_f,
        x="Troponina_ng_mL",
        nbins=20,
        color="Diagnóstico",
        title="Distribución general de valores de troponina"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------
# INFORMACIÓN MÉDICA
# ---------------------------------------------------------
elif seccion == "📚 Información Médica":
    st.title("📚 Información Clínica de la Troponina")

    st.write("""
La **troponina** es el biomarcador más importante para diagnosticar un **infarto agudo al miocardio (IAM)**.

### Interpretación clínica:
- **0–0.04 ng/mL** → Normal  
- **0.04–0.4 ng/mL** → Sospecha de daño  
- **0.4–1 ng/mL** → Daño moderado  
- **1–5 ng/mL** → Alto riesgo  
- **>5 ng/mL** → Daño severo al miocardio  
""")

# ---------------------------------------------------------
# INFORMACIÓN PROTEICA
# ---------------------------------------------------------
elif seccion == "🧬 Troponina - Detalles Proteicos":
    st.title("🧬 Troponina: Subunidades y Función")

    st.write("""
La troponina está compuesta por **tres subunidades principales**:

### Troponina C (TnC)
- Se une al calcio para iniciar la contracción muscular.

### Troponina I (TnI)
- Inhibe la interacción actina-miosina.
- Es el biomarcador más específico en sangre.

### Troponina T (TnT)
- Ancla el complejo troponina a la tropomiosina.

Elevaciones de **TnI** o **TnT** se utilizan para diagnosticar daño cardíaco.
""")






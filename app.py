import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard de Troponina",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# DATASET CARGADO POR DEFECTO
# ---------------------------------------------------------
@st.cache_data
def load_data():
    data = {
        "Paciente_ID": [1, 2, 3, 4, 5, 6],
        "Troponina_ng_mL": [0.01, 0.15, 0.47, 1.2, 3.4, 8.9],
        "Edad": [23, 45, 67, 38, 59, 71],
        "Diagnóstico": [
            "Sano",
            "Sospecha",
            "IAM leve",
            "IAM moderado",
            "IAM severo",
            "Crítico"
        ]
    }
    df = pd.DataFrame(data)
    return df

df = load_data()

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("🔬 Dashboard de Troponina")
opcion = st.sidebar.radio(
    "Selecciona una sección:",
    ["📈 Análisis", "ℹ️ Información", "🧬 Estructura Proteica"]
)

st.sidebar.write("---")
st.sidebar.write("Desarrollado para proyecto final 💻🧪")

# ---------------------------------------------------------
# SECCIÓN 1: ANÁLISIS
# ---------------------------------------------------------
if opcion == "📈 Análisis":
    st.title("📈 Análisis de Niveles de Troponina")
    st.write(
        "Aquí puedes visualizar los valores almacenados y observar "
        "si existen indicios de infarto agudo al miocardio (IAM)."
    )

    st.subheader("📊 Tabla de Datos")
    st.dataframe(df, use_container_width=True)

    st.subheader("📉 Distribución de Troponina")
    fig = px.bar(
        df,
        x="Paciente_ID",
        y="Troponina_ng_mL",
        color="Diagnóstico",
        title="Niveles de Troponina por Paciente",
        labels={"Troponina_ng_mL": "Troponina (ng/mL)", "Paciente_ID": "ID"},
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 Relación Edad vs Troponina")
    fig2 = px.scatter(
        df,
        x="Edad",
        y="Troponina_ng_mL",
        size="Troponina_ng_mL",
        color="Diagnóstico",
        title="Relación entre Edad y Troponina",
        labels={"Troponina_ng_mL": "Troponina (ng/mL)"}
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------
# SECCIÓN 2: INFORMACIÓN
# ---------------------------------------------------------
elif opcion == "ℹ️ Información":
    st.title("ℹ️ Información sobre la Troponina")
    st.write("""
La **troponina** es una proteína estructural del músculo cardíaco.  
Su medición en sangre es la **prueba más importante y confiable** para diagnosticar un **infarto agudo al miocardio (IAM)**.

### 🔍 ¿Qué indica su nivel en sangre?

- **0–0.04 ng/mL** → Normal  
- **0.04–0.4 ng/mL** → Posible lesión  
- **>0.4 ng/mL** → SOSPECHA de infarto  
- **>1 ng/mL** → ALTO riesgo  
- **>5 ng/mL** → PROBABLE daño cardíaco severo  

### 🧪 ¿Qué mide este dashboard?

Este dashboard analiza:

- Niveles numéricos de troponina  
- Edad del paciente  
- Clasificación diagnóstica  
- Relaciones entre variables  

Todo esto ayuda a simular cómo se interpretan estos estudios en un contexto clínico.
""")

# ---------------------------------------------------------
# SECCIÓN 3: ESTRUCTURA PROTEICA
# ---------------------------------------------------------
elif opcion == "🧬 Estructura Proteica":
    st.title("🧬 Estructura de la Troponina (Descripción)")
    st.write("""
La **troponina** está formada por **tres subunidades**:

### **1. Troponina C (TnC)**
- Une calcio durante la contracción muscular.

### **2. Troponina I (TnI)**
- Inhibe la interacción actina-miosina.  
- Es la más usada como **biomarcador cardiaco**.

### **3. Troponina T (TnT)**
- Conecta el complejo a la tropomiosina.

La presencia elevada de **TnI** o **TnT** en sangre indica daño en el miocardio.
""")





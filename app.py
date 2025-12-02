# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from io import StringIO

# ---------- Config ----------
st.set_page_config(page_title="Dashboard Troponina (cTnI) - Pro",
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
st.markdown('**Interfaz interactiva** para explorar niveles de troponina, con información clínica y visualización de la proteína.')

st.write("---")

# ---------- Default dataset generator ----------
def generate_default_df(n=40, seed=42):
    np.random.seed(seed)
    start = datetime(2025,1,1)
    ids = list(range(1, n+1))
    edades = np.random.randint(18, 90, n)
    sexos = np.random.choice(["Masculino", "Femenino"], n)
    # troponina distribution skewed: most low, some high
    troponina = np.round(np.concatenate([
        np.random.beta(1.5, 50, int(n*0.75)) * 0.05,  # low values
        np.random.beta(2, 5, n - int(n*0.75)) * 3.0   # some high
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
    df = pd.DataFrame({
        "Paciente_ID": ids,
        "Edad": edades,
        "Sexo": sexos,
        "Troponina_cTnI_ng_mL": troponina,
        "Diagnóstico": diagnosticos,
        "Fecha": fechas
    })
    return df

# Load default dataset (embedded)
default_df = generate_default_df(n=60)

# ---------- Sidebar: upload / options ----------
with st.sidebar:
    st.header("Datos")
    uploaded = st.file_uploader("Sube CSV (opcional). Si no, se usa dataset por defecto.", type=["csv"])
    replace_default = st.checkbox("Usar únicamente datos por defecto", value=False)
    st.markdown("**Filtros rápidos**")
    sexo_filter = st.multiselect("Sexo", options=["Masculino","Femenino"], default=["Masculino","Femenino"])
    edad_min, edad_max = st.slider("Rango de edad", 18, 90, (18,90))
    download_btn = st.empty()

# ---------- Decide dataset ----------
if uploaded and not replace_default:
    try:
        df = pd.read_csv(uploaded)
        st.success("CSV cargado ✅ (puedes usar el dataset por defecto con la caja lateral).")
    except Exception as e:
        st.error("Error cargando CSV. Usando dataset por defecto.")
        df = default_df.copy()
elif uploaded and replace_default:
    st.warning("Ha seleccionado usar solo los datos por defecto. Ignorando el CSV subido.")
    df = default_df.copy()
else:
    df = default_df.copy()

# Basic sanitization: ensure troponina column exists
if "Troponina_cTnI_ng_mL" not in df.columns:
    # try to find a numeric column and rename it
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        df = df.rename(columns={numeric_cols[0]: "Troponina_cTnI_ng_mL"})
    else:
        st.error("El dataset no contiene columna numérica de troponina. Asegúrate de tener una columna numérica.")
        st.stop()

# Apply sidebar filters
df = df[df["Sexo"].isin(sexo_filter)]
df = df[(df["Edad"] >= edad_min) & (df["Edad"] <= edad_max)]

# ---------- Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs(["Explorar datos", "Análisis", "Información clínica", "Visualizar proteína"])

# ---------- Tab 1: Exploración ----------
with tab1:
    st.subheader("Exploración de datos")
    st.markdown("Vista previa del dataset (filtrado). Puedes descargar el subset filtrado.")
    st.dataframe(df.reset_index(drop=True), use_container_width=True)

    # Download filtered data
    csv = df.to_csv(index=False).encode('utf-8')
    download_btn.download_button("Descargar CSV filtrado", data=csv, file_name="troponina_filtrado.csv", mime="text/csv")

    st.markdown("---")
    # Quick scatter: troponina vs edad
    st.markdown("**Troponina vs Edad**")
    fig = px.scatter(df, x="Edad", y="Troponina_cTnI_ng_mL", color="Diagnóstico",
                     hover_data=["Paciente_ID","Sexo","Fecha"], size="Troponina_cTnI_ng_mL",
                     title="Troponina (ng/mL) según edad y diagnóstico")
    st.plotly_chart(fig, use_container_width=True)

# ---------- Tab 2: Análisis ----------
with tab2:
    st.subheader("Análisis estadístico y visualizaciones")
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        mean_val = df["Troponina_cTnI_ng_mL"].mean()
        st.metric("Media (ng/mL)", f"{mean_val:.3f}")
    with col2:
        median_val = df["Troponina_cTnI_ng_mL"].median()
        st.metric("Mediana (ng/mL)", f"{median_val:.3f}")
    with col3:
        max_val = df["Troponina_cTnI_ng_mL"].max()
        st.metric("Máximo (ng/mL)", f"{max_val:.3f}")

    st.markdown("**Distribución de Troponina**")
    fig2 = px.histogram(df, x="Troponina_cTnI_ng_mL", nbins=40, color="Diagnóstico",
                        marginal="box", title="Histograma de Troponina (con boxplot marginal)")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Series temporales (si la columna Fecha está presente)**")
    if "Fecha" in df.columns:
        try:
            df["Fecha_dt"] = pd.to_datetime(df["Fecha"])
            df_ts = df.groupby("Fecha_dt")["Troponina_cTnI_ng_mL"].mean().reset_index()
            fig3 = px.line(df_ts, x="Fecha_dt", y="Troponina_cTnI_ng_mL", markers=True,
                           title="Promedio diario de Troponina")
            st.plotly_chart(fig3, use_container_width=True)
        except Exception:
            st.info("La columna Fecha no tiene formato válido; conviértela a YYYY-MM-DD para ver la serie temporal.")
    else:
        st.info("No hay columna Fecha en el dataset.")

    st.markdown("**Boxplot por diagnóstico**")
    fig4 = px.box(df, x="Diagnóstico", y="Troponina_cTnI_ng_mL", points="all", title="Troponina por Diagnóstico")
    st.plotly_chart(fig4, use_container_width=True)

# ---------- Tab 3: Información clínica ----------
with tab3:
    st.subheader("Información sobre Troponina cardíaca (cTnI)")
    st.markdown("""
    - La **troponina cardíaca (cTnI / cTnT)** es una proteína del músculo cardíaco que se libera en sangre
      cuando hay daño al miocardio (por ejemplo infarto agudo).
    - Los **rangos** dependen del ensayo del laboratorio; valores típicos de referencia suelen ser muy bajos
      (por ejemplo < 0.014 ng/mL en algunos kits).  
    - Valores detectables y en aumento en muestras seriadas son un criterio importante para el diagnóstico de infarto.
    """)
    st.markdown("**Referencias generales:**")
    st.markdown("- MedlinePlus: prueba de troponina")
    st.markdown("- Guías clínicas: interpretación depende del ensayo y del contexto clínico")

    st.markdown("**Imágenes y recursos**")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Troponin.png/640px-Troponin.png",
             caption="Complejo de troponina (I, T, C) — imagen ilustrativa", width=420)
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/44/Heart_anterior_exterior_view.jpg",
             caption="Anatomía: vista anterior del corazón", width=420)

# ---------- Tab 4: Visualizar la proteína ----------
with tab4:
    st.subheader("Visualización de la proteína — Troponina T / Troponina I")
    st.markdown("Aquí mostramos imágenes representativas de la proteína y su localización en el músculo cardiaco.")
    st.markdown("**Modelos moleculares / estructuras (ilustrativas)**")
    st.image("https://files.rcsb.org/ligands/view/TPO_idealized_1.png", caption="Modelo (ilustrativo) — PDB / representaciones", width=360)
    st.markdown("**Secuencia y notas (ejemplo)**")
    st.code("Muestra: Troponina T (fragmento) — MKSK... (secuencia ilustrativa)", language="text")
    st.markdown("**Explicación gráfica**")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Skeletal_muscle_diagram.svg/800px-Skeletal_muscle_diagram.svg.png",
             caption="Diagrama músculo/filamentos — troponina regula interacciones actina-miosina", width=520)

st.write("---")
st.markdown("⚠️ **Nota:** Los valores y las interpretaciones mostradas son **para fines educativos**. En la práctica clínica, siempre seguir protocolos y laboratorios autorizados.")





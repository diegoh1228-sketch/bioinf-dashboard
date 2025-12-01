import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# ESTILO (CSS)
# -----------------------------
st.markdown("""
<style>
.big-title {
    font-size: 38px;
    color: #4A90E2;
    font-weight: bold;
}

.card {
    padding: 18px;
    border-radius: 12px;
    background-color: #F3F6FA;
    border-left: 6px solid #4A90E2;
    margin-bottom: 15px;
}

.section-title {
    font-size: 26px;
    color: #2C3E50;
    font-weight: bold;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TÍTULO PRINCIPAL
# -----------------------------
st.markdown('<p class="big-title">📊 Dashboard Bioinformático – Troponina</p>', unsafe_allow_html=True)

st.sidebar.title("📌 Menú")
seccion = st.sidebar.selectbox(
    "Selecciona sección",
    ["Inicio", "Cargar datos", "Ejemplo: Troponina"]
)

# -----------------------------
# SECCIÓN INICIO
# -----------------------------
if seccion == "Inicio":
    st.markdown('<p class="section-title">Bienvenido</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    Este dashboard permite cargar archivos CSV, generar gráficas automáticas 
    y visualizar un ejemplo biomédico usando niveles simulados de 
    <b>Troponina cardíaca</b>, un importante biomarcador para diagnóstico de infarto.
    </div>
    """, unsafe_allow_html=True)

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Troponin.png/640px-Troponin.png",
        caption="Complejo de Troponina (I, T y C)"
    )

# -----------------------------
# SECCIÓN CARGAR DATOS
# -----------------------------
elif seccion == "Cargar datos":
    st.markdown('<p class="section-title">📂 Cargar archivo CSV</p>', unsafe_allow_html=True)

    archivo = st.file_uploader(
        "Arrastra o selecciona un archivo CSV (máx. 200 MB)",
        type="csv"
    )

    if archivo is None:
        st.info("📁 Aún no has cargado un archivo.")
    else:
        df = pd.read_csv(archivo)
        st.success("Archivo cargado correctamente ✔")
        st.dataframe(df)

        st.markdown('<p class="section-title">📈 Histograma automático</p>', unsafe_allow_html=True)

        try:
            fig, ax = plt.subplots()
            df.iloc[:, 0].hist(ax=ax, bins=20)
            ax.set_xlabel(df.columns[0])
            ax.set_ylabel("Frecuencia")
            st.pyplot(fig)
        except:
            st.error("No se pudo graficar. La primera columna debe ser numérica.")

# -----------------------------
# SECCIÓN TROPONINA
# -----------------------------
elif seccion == "Ejemplo: Troponina":
    st.markdown('<p class="section-title">🔬 Ejemplo biomédico: Niveles de Troponina cardíaca</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    La <b>troponina</b> es un biomarcador que aumenta en sangre cuando hay daño al corazón, 
    como durante un infarto agudo al miocardio.
    </div>
    """, unsafe_allow_html=True)

    datos = pd.DataFrame({
        "Muestra": [f"S{i}" for i in range(1, 11)],
        "Troponina (ng/mL)": [0.01, 0.02, 0.015, 0.03, 0.05, 0.20, 0.15, 0.04, 0.08, 0.12]
    })

    st.subheader("📋 Valores simulados")
    st.dataframe(datos)

    st.subheader("📉 Gráfica de niveles de Troponina")
    fig, ax = plt.subplots()
    ax.plot(datos["Muestra"], datos["Troponina (ng/mL)"], marker='o')
    ax.set_ylabel("ng/mL")
    ax.set_xlabel("Muestra")
    plt.xticks(rotation=45)
    st.pyplot(fig)



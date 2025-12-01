import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard Bioinformático – Ejemplo: Troponina cardíaca")

st.sidebar.title("Menú")
sección = st.sidebar.selectbox(
    "Selecciona sección",
    ["Inicio", "Cargar datos", "Ejemplo: niveles de Troponina"]
)

if sección == "Inicio":
    st.write("""
    Bienvenido al dashboard. Este proyecto permite cargar datos, visualizar tablas y gráficas,
    y además incluye un ejemplo biomédico usando niveles simulados de troponina cardíaca.
    """)

elif sección == "Cargar datos":
    st.write("Carga un archivo CSV para visualizar y graficar datos.")
    archivo = st.file_uploader("Sube archivo CSV", type="csv")
    if archivo is not None:
        df = pd.read_csv(archivo)
        st.write("Datos cargados:")
        st.dataframe(df)
        st.write("Histograma de la primera columna:")
        try:
            fig, ax = plt.subplots()
            df.iloc[:,0].hist(ax=ax, bins=20)
            st.pyplot(fig)
        except Exception as e:
            st.error("No se puede graficar: asegúrate que la primera columna sea numérica.")

elif sección == "Ejemplo: niveles de Troponina":
    st.header("Ejemplo simulado: Troponina cardíaca (I/T)")

    st.write("""
    La troponina cardíaca se mide en sangre para detectar daño al músculo del corazón.
    En personas sanas, los valores son muy bajos o indetectables.  
    A continuación un conjunto de valores simulados (ng/mL) correspondientes a diferentes muestras.
    """)

    # Datos simulados
    datos = pd.DataFrame({
        "Muestra": [f"S{i}" for i in range(1,11)],
        "Troponina (ng/mL)": [0.01, 0.02, 0.015, 0.03, 0.05, 0.2, 0.15, 0.04, 0.08, 0.12]
    })

    st.write("Valores simulados de troponina:")
    st.dataframe(datos)

    st.write("Gráfica de niveles de troponina por muestra:")
    fig, ax = plt.subplots()
    ax.plot(datos["Muestra"], datos["Troponina (ng/mL)"], marker='o')
    ax.set_ylabel("ng/mL")
    ax.set_xlabel("Muestra")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.write("""
    En un contexto clínico, valores elevados de troponina pueden indicar daño al miocardio — por ejemplo tras un infarto.  
    En cambio valores muy bajos o indetectables suelen corresponder a un corazón sano.  
    Este ejemplo es solo ilustrativo; los rangos reales dependen del test de laboratorio.  
    """)


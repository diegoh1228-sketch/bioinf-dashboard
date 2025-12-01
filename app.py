import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard Bioinformático Simple")

st.sidebar.title("Menú")
opcion = st.sidebar.selectbox("Selecciona una sección", ["Inicio", "Cargar Datos", "Proteína Ejemplo"])

if opcion == "Inicio":
    st.write("Bienvenido a un dashboard simple desarrollado para visualizar datos y un ejemplo biomédico.")

elif opcion == "Cargar Datos":
    archivo = st.file_uploader("Carga un archivo CSV", type="csv")
    if archivo is not None:
        df = pd.read_csv(archivo)
        st.write("Datos cargados:")
        st.dataframe(df)

        st.write("Gráfica automática:")
        fig, ax = plt.subplots()
        df.iloc[:,0].plot(kind="hist", ax=ax)
        st.pyplot(fig)

elif opcion == "Proteína Ejemplo":
    st.write("Ejemplo: niveles simulados de proteína Albúmina")
    datos = pd.DataFrame({
        "Concentración (g/dL)": [3.5, 4.0, 4.2, 3.8, 4.5, 3.9, 4.1]
    })
    st.dataframe(datos)

    fig, ax = plt.subplots()
    ax.plot(datos["Concentración (g/dL)"])
    st.pyplot(fig)

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import sys
import os
import funciones_logs
# Obtener la ruta absoluta del directorio padre
directorio_padre = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Agregar el directorio padre al sys.path
sys.path.append(directorio_padre)
import funciones_logs

st.title("Estadísticas de Logs")
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Dias ", "Generos", "Tipos op", "Op por usuario", "Imagenes mas usadas", "Palabras mas usadas", "Op por genero"])

with tab1:

    figura = funciones_logs.grafico_diario()
    st.pyplot(figura)
    
with tab2:
    st.subheader('Gráfico de torta que muestra los generos que realizaron operaciones')
    figura = funciones_logs.grafico_generos()
    st.pyplot(figura)

with tab3:
    st.subheader('Gráfico de barras sobre los los tipos de operaciones que se realizaron.')
    grafico = funciones_logs.grafico_operaciones()
    st.pyplot(grafico)

with tab4:
    st.subheader('Gráfico de barras sobre la cantidad y tipo de operacion por usuario.')
    grafico_barras = funciones_logs.grafico_barras_operaciones()
    st.pyplot(grafico_barras)

with tab5:
    st.subheader('Imagenes más usadas por el generador de memes:')
    datos = funciones_logs.imagenes_mas_usadas('generacion_meme')
    st.write(datos)
    st.subheader('Imagenes más usadas por el generador de collage:')
    datos = funciones_logs.imagenes_mas_usadas('generacion_collage')
    st.write(datos)

with tab6:
    st.subheader('Nube de palalabras con las mas usadas en los memes: ')
    nube = funciones_logs.nube_palabras_memes()
    st.write(nube)
    st.subheader('Nube de palalabras con las mas usadas en los collages: ')
    nube = funciones_logs.nube_palabras_collage()
    st.write(nube)

with tab7:
    st.subheader('Gráfico de totas con los tipos de generos que etiquetaron una nueva imagen')
    fig = funciones_logs.grafico_tortas_genero('nueva_imagen')
    st.write(fig)
    st.subheader('Gráfico de totas con los tipos de generos que modificaron una imagen')
    fig = funciones_logs.grafico_tortas_genero('modificacion_imagen')
    st.write(fig)


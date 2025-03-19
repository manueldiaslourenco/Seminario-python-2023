import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import sys
import os
# Obtener la ruta absoluta del directorio padre
directorio_padre = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Agregar el directorio padre al sys.path
sys.path.append(directorio_padre)
import funciones_imagenes

st.title("Estadísticas de Imágenes")
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8  = st.tabs(["Tipo imagen", "Tamaño imagen", "Tipos tamaños", "Dia", "Fechas", "Tags mas usados", "Promedio ", "nube"  ])

with tab1:
    st.subheader("Gráfico de torta que muestre los porcentajes según el tipo de imagen")
    datos,figura = funciones_imagenes.grafico_tortas()
    st.write(datos)
    st.pyplot(figura)
    
with tab2:
    ancho, alto = funciones_imagenes.calc_tam_max()
    texto_ancho = f"<h1 style='font-size: 24px; font-family: Georgia;'>El ancho maximo de las imagenes es es: {ancho} px</h1>"
    texto_alto = f"<h1 style='font-size: 24px; font-family: Georgia;'>El alto maximo de las imagenes es: {alto} px</h1>"

    st.write(texto_ancho, unsafe_allow_html=True, )
    st.write(texto_alto, unsafe_allow_html= True )

with tab3:
    st.subheader("Gráfico de dispersión con los distintos anchos y altos de las fotos")
    grafico_dispersion = funciones_imagenes.grafico_dispersion()
    st.pyplot(grafico_dispersion)

with tab4:
    st.subheader('Gráfico de barras sobre los días que se realizaron actualizaciones de etiquetas')
    grafico_barras = funciones_imagenes.grafico_barras()
    st.pyplot(grafico_barras)

with tab5:
    st.subheader('Gráfico de la cantidad de actualizaciones con el paso del tiempo')
    grafico_lineas = funciones_imagenes.grafico_lineas()
    st.pyplot(grafico_lineas)

with tab6:
    st.subheader('Los 3 tags mas utilizados son: ')
    tags = funciones_imagenes.tags_mas_usados()
    st.write(tags)

with tab7:
    promedio = funciones_imagenes.tam_promedio()
    st.subheader('El tamaño promedio de las imagenes es el siguiente:')
    st.write(promedio)
    
with tab8:
    st.subheader('Nube de palabras con los tags mas usados')
    nube = funciones_imagenes.nubes_de_palabras()
    st.write ( nube )
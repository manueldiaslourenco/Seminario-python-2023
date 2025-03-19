import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
from datetime import datetime as dt
from wordcloud import WordCloud, STOPWORDS
from collections import Counter


ruta = os.path.join('..','unlpimage', 'data', 'informacion_imagenes.csv')
df = pd.read_csv(ruta, encoding='utf-8')
copia = df.copy()

def grafico_tortas():

    """Se retorna un grafico de tortas que muestra los porcentajes según el tipo de imagen"""

    st.markdown("""
                    Paso 1: Cuento la cantidad de valores por tipo.<br>
                    Paso 2: Genero una lista con los tipos (sin repetidos) para usar como etiquetas.
                """, unsafe_allow_html= True)
    
    fig, ax = plt.subplots()
    # Cuento cuantos valores hay de cada tipo
    datos = df['tipo'].value_counts()
    st.write('Paso 1: ', datos)
    etiquetas = df['tipo'].unique()
    st.markdown('Paso 2: {}' .format(etiquetas) )

    ax.pie(datos, labels= etiquetas, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Asegura que el gráfico sea una figura circular

    return datos, fig

def calc_tam_max():

    """Se retorna los valores máximos de ancho y de alto de las imágenes clasificadas."""
 
    st.markdown("""
                    Paso 1: Agrego las columnas de alto y ancho de la copia del df con las resoluciones respectivas de las imagenes.<br>
                    Paso 2: Calculo los maximos.
                """, unsafe_allow_html= True)
    # Genero columnas de alto y ancho para almacenar los valores correspondientes
    for i, fila in df.iterrows():
       copia.at[i,'ancho'] = fila['resolucion'].strip('()').strip().split(',')[0]
       copia.at[i,'alto'] = fila['resolucion'].strip('()').strip().split(',')[1]

    st.write('Paso 1: ', copia[['ruta', 'resolucion', 'alto', 'ancho']])
    # Calculo los maximos
    alto_max = copia['alto'].astype(int).max() 
    ancho_max = copia['ancho'].astype(int).max()

    st.write('Paso 2: ')

    return ancho_max, alto_max

def grafico_dispersion():

    """Se retorna un gráfico de dispersión para visualizar la relación entre el ancho y el alto de las imágenes"""

    st.markdown("""
                    Paso 1: Ordeno de menor a mayor las columnas de alto y ancho.<br>
                    Paso 2: Genero el gráfico.
                """, unsafe_allow_html= True)

    # Creo el scatter plot con los valores ordenados
    valores_alto = copia['alto'].astype(int).sort_values()
    valores_ancho = copia['ancho'].astype(int).sort_values()

    st.write('Paso 1: ', copia[['ruta', 'resolucion', 'alto', 'ancho']])
    fig, ax = plt.subplots()
    ax.scatter( valores_alto, valores_ancho, label='Y')

    # Configuro el título y etiquetas de los ejes
    ax.set_title('Gráfico de dispersión')
    ax.set_xlabel('ALTO')
    ax.set_ylabel('ANCHO')

    st.write('Paso 2: ')


    return fig

def grafico_barras():

    """Se retorna, en base a la fecha de última actualización, cantidad de cambios realizados para cada día de la semana"""

    st.markdown("""
                    Paso 1: En base al timestamp de la ultima actualizacion, calculo en que dia de la semana se realizó.<br>
                    Paso 2: Genero una lista con todos los dias posibles en los que se pueden realizar actualizaciones.<br>
                    Paso 3: Agrupo por dia y cuento cuantos se realizaron por dia.<br>
                    Paso 4: Genero una nueva lista con los dias en que se realizaron actualizaciones.<br>
                    Paso 5: Creo otra lista con la cantidad de actualizaciones por dia.
                """, unsafe_allow_html= True)

    # Detallo que día fue el de la ultima actualizacion
    copia['Fecha'] = df['ultima actualizacion'].apply(lambda x: dt.fromtimestamp(x))
    copia['Dia de la semana'] = copia['Fecha'].dt.day_name()

    st.write('Paso 1: ', copia[['perfil actualizo', 'Dia de la semana']])
    # Genero una lista con todos los posibles dias de la semana
    dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    st.markdown('Paso 2: {}' .format(dias_semana) )
    # Agrupo por dia y los cuento
    cant_por_dia = copia.groupby('Dia de la semana').size()
    st.write('Paso 3: ', cant_por_dia)
    # Guardo los dias que aparecieron en esta variable
    todos_dias = copia['Dia de la semana'].unique().tolist()
    st.markdown('Paso 4: {}' .format(todos_dias) )

    valores = [cant_por_dia[dia] if dia in todos_dias else 0 for dia in dias_semana]
    st.markdown('Paso 5: {}' .format(valores) )

    etiquetas = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    # Crear el gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(etiquetas,valores)

    # Personalizar el gráfico
    ax.set_xlabel('Dias')
    ax.set_ylabel('Actualizaciones')

    return fig

def grafico_lineas():

    """Se retorna un gráfico de líneas para visualizar la evolución de la cantidad de actualizaciones a lo largo del tiempo"""
    st.markdown("""
                    Paso 1: Almaceno las fechas en que se realizaron actualizaciones(sin repeticiones) y las ordeno.<br>
                    Paso 2: Agrupo fecha y cuento cuantas actualizaciones hubo en cada día.
                """, unsafe_allow_html= True)

    # Guardo la columna de las fechas
    x = copia['Fecha'].dt.date.unique()
    # Las ordeno
    x.sort()
    st.write('Paso 1: ', x)  

    # Ordeno y cuento por fecha
    y = copia.groupby(copia['Fecha'].dt.date.sort_values()).size()
    st.write('Paso 2: ', y)

    st.write(y)

    #Grafico
    fig, ax = plt.subplots()
    ax.plot(x, y, marker = "o", markersize = 5)

    #Etiquetas
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Actualizaciones')
    plt.xticks(rotation=45, ha='right')

    return fig

def tags_mas_usados():
    
    """Se retorna un DataFrame con los 3 tags más utilizados"""

    st.markdown("""
                    Paso 1: Almaceno todos los tags utilizados.<br>
                    Paso 2: Genero una lista de tuplas con el nombre y repeticiones de los 3 mas utilizados.<br>
                    Paso 3: Genero un df con esos datos.
                """, unsafe_allow_html= True)
    # Datos
    tags = []
    df_tags = df['lista de tags'].astype(str)
    # Agrego a 'tags' todos los tags que aparecieron
    df_tags.apply(lambda x: tags.extend(x.split(',')))
    st.markdown('Paso 1: {}' .format(tags) )   
    # Almaceno solo los mas comunes
    tags = Counter(tags).most_common(3)
    st.markdown('Paso 2: {}' .format(tags) )   
    # Creo el DataFrame
    datos = pd.DataFrame(tags, columns=['tags', 'frecuencias'])

    # Cuento la cantidad de filas
    cant_filas = datos.shape[0]
    if (cant_filas < 3):
        # Genero un rango desde 1 hasta la cantidad de tipos de tags
        numeros = range(1,cant_filas+1)
        # Los almaceno en una lista
        lista = list(numeros)
        # Los asigno a los indices
        datos.index = lista
    else:
        datos.index = [1,2,3]
    
    st.write('Paso 3:')

    return datos

def tam_promedio():

    """Se retorna un DataFrame  el tamano en bytes promedio de las imágenes actualizadas por cada perfil,
    incluir los perfiles que no hayan realizado actualizaciones."""

    st.markdown("""
                    Paso 1: Creo una columna 'tamano strip' para almacenar solamente el float del tamano de la imagen.<br>
                    Paso 2: Realizo un merge entre el alias del archivo json de usuarios y el perfil que actualizo en el csv, tambien pongo en 0 las celdas que contengan Nan para contabilizar luego los usuarios que no actualizaron imagenes.<br>
                    Paso 3: Agrupo por alias y sumo los tamanos.<br>
                    Paso 4: Cuento la cantidad de imagenes de cada usuario.<br>
                    Paso 5: Calculo el promedio ordenandolos y reseteando los indices para que queden ordenados, por último le agrego el 'MB' al final.
                """, unsafe_allow_html= True)

    ruta_json = os.path.join('..','unlpimage', 'data', 'datos_usuarios.json')
    json = pd.read_json(ruta_json)

    #Modifico la columna 'tamano' para que queden solo los float
    copia['tamano strip'] = copia['tamano'].str.replace('KB', '').str.strip()
    copia['tamano strip'] = copia['tamano strip'].astype(float)

    st.write('Paso 1', copia[['perfil actualizo', 'tamano strip']])

    st.write(json)

    #Hago un merge entre los alias y los perfiles que actualizaron
    merge = pd.merge(json, copia, left_on= 'Alias', right_on= 'perfil actualizo', how= 'outer' ).fillna(0)
    st.write('Paso 2', merge[['Alias', 'tamano strip']])

    #Cuento la suma de los tamanos y las apariciones
    suma = merge.groupby(merge['Alias'])['tamano strip'].sum()
    st.write('Paso 3', suma)
    apariciones = merge.groupby(merge['Alias']).size()
    st.write('Paso 4', apariciones)

    #Genero una series con los promdedios
    promedio = suma / apariciones

    #Acomodo los valores, indices y columnas
    promedio = promedio.sort_values(ascending=False).reset_index()
    promedio.index = promedio.index + 1
    promedio.columns = ['Perfil', 'Tamano Promedio']

    #Limito el formato a solo dos numeros despues del punto
    promedio['Tamano Promedio'] = promedio['Tamano Promedio'].apply(lambda x: '{:.2f}'.format(x))
    #Agrego mb al final de cada tamano
    promedio['Tamano Promedio'] = promedio['Tamano Promedio'].astype('string') + ' MB'

    st.write('Paso 5: ')

    return promedio

def nubes_de_palabras():

    st.markdown("""
                    Paso 1: Elimino los tags repetidos.<br>
                    Paso 2: Genero una lista con todos los tags.<br>
                    Paso 3: Si la lista no esta vacia, genero un string con todos los tags utilizados.
                """, unsafe_allow_html= True)

    @st.cache_data()
    def generar_wordcloud(lista):
        wordcloud = WordCloud(width=300, height=200, random_state=1, background_color='white', colormap='Set2', collocations=False, stopwords=STOPWORDS).generate(lista)
        return wordcloud


    lista = []
    palabras = copia['lista de tags'].astype(str)
    # Elimino los tags repetidos
    palabras.unique()
    st.write('Paso 1', palabras)
    # Agrego los distintos tags a una lista
    palabras = palabras.apply(lambda x: lista.extend(x.split(',')))
    st.markdown('Paso 2: {}' .format(lista) )   

    if len(lista) == 0:
        fig = 'No hay palabras para utilizar en la nube'
    else:
        # Espacio las palabras de la lista de tags
        lista = ' '.join(lista)
        st.markdown('Paso 3: {}' .format(lista) )   
        wordcloud = WordCloud(width = 50, height = 50, random_state=1,background_color='white', colormap='Set2', collocations=False, stopwords =STOPWORDS).generate(lista)
        wordcloud = generar_wordcloud(lista)
        fig, ax = plt.subplots(figsize=(40, 30))
        # Mostrar la imagen
        ax.imshow(wordcloud)
        # Ocultar detalles de los ejes
        ax.axis("off")

    return fig

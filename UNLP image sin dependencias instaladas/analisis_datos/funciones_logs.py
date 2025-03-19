import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
from datetime import datetime as dt
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
import numpy as np

ruta = os.path.join('..','unlpimage', 'data', 'logs_sistema.csv')
df = pd.read_csv(ruta)
copia = df.copy()

ruta_json = os.path.join('..','unlpimage', 'data', 'datos_usuarios.json')
json = pd.read_json(ruta_json)

def grafico_diario():

    """Se retorna un grafico de barras sobre los días de la semana en que se realizaron operaciones usando la aplicación"""

    # Obtengo los dias de cada operacion y los almaceno en la columa de 'Dia de la semana'



    copia['Fecha'] = copia['Fecha y hora'].apply(lambda x: dt.fromtimestamp(x))
    copia['Dia de la semana'] = copia['Fecha'].dt.day_name()

    st.markdown("Calculo en qué día de la semana se realizó cada operación en base al timestamp: ")
    st.dataframe(copia[['Alias', 'Operacion', 'Dia de la semana']])

    # Guardo todos los días de la semana por si en algunos días NO se realizaron operaciones
    dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # Cuento cuántos hay de cada día
    cant_por_dia = copia.groupby('Dia de la semana').size()

    st.markdown('Agrupo por día de la semana y cuento la cantidad por día')
    st.write(cant_por_dia.to_frame())

    # Hago una lista de los días en los que se realizaron operaciones
    todos_dias = copia['Dia de la semana'].unique().tolist()

    # En la lista de valores guardo la cantidad de operaciones por día
    valores = [cant_por_dia[dia] if dia in todos_dias else 0 for dia in dias_semana]

    st.markdown('Genero una lista con los días que SI aparecen en el DataFrame: {}'.format(todos_dias))
    st.markdown('Y otra para las cantidad de operaciones por día (incluyendo los que NO aparecen): {}'.format(valores))

    etiquetas = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    # Crear el gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(etiquetas, valores)

    # Personalizar el gráfico
    ax.set_ylabel('Operaciones')
    ax.set_title('Gráfico de barras sobre los días que se realizaron operaciones')



    return fig

def grafico_generos():

    """Se retorna un grafico de tortas que muestra los porcentajes de de uso de la aplicación por genero"""

    st.markdown(""" 
                    Paso 1: Tomo los datos del json.<br>
                    Paso 2: Realizo un merge entre el json y el csv sobre el Alias.<br>
                    Paso 3: Agrupo por género y cuento la cantidad de ocurrencias de cada uno.<br>
                    Paso 4: Mi conjunto de datos es el merge en la columna 'cantidad'.

                """, unsafe_allow_html= True)

    datos_json = json[['Alias', 'Genero']]
    st.write('Paso 1: ', datos_json)

    #Realizo un merge entre el json y el csv
    merge = pd.merge(copia, datos_json, on= 'Alias', how= 'inner')
    st.write('Paso 2: ', merge)

    #Agrupo por genero y agrego la columna 'Cantidad'
    merge = merge.groupby('Genero').size().reset_index(name='Cantidad')
    st.write('Paso 3: ', merge)

    fig, ax = plt.subplots()
    datos = merge['Cantidad']
    st.write('Paso 4: ', datos)

    ax.pie(datos, labels=merge['Genero'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Asegura que el gráfico sea una figura circular

    return fig

def grafico_operaciones():

    """Se retorna un grafico de barras que refleja las cantidades de cada operacion realizada"""
    


    st.markdown("""
                    Paso 1: Almaceno la cantidad de operaciones en una lista.<br>
                    Paso 2: Genero otra lista con las operaciones realizadas.<br>
                """, unsafe_allow_html= True)

    # Agrupo por operacion y cuento cuantas hay de c u
    cantidad = copia.groupby('Operacion').size()
    st.markdown ('Paso 1: {}' .format(cantidad.tolist()) )

    # Almaceno las operaciones en una lista
    operaciones = cantidad.index.tolist()
    st.markdown ('Paso 2: {}' .format(operaciones) ) 

    # Agrego tildes y mayúsculas a las operaciones

    # Crear el gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(operaciones,cantidad)

    # Personalizar el gráfico
    ax.set_xlabel('Operaciones')
    ax.set_ylabel('Cantidad')
    plt.xticks(rotation=45, ha='right')

    return fig

def convertidor(datos, operaciones):
    """Devuelve una lista de series con la cantidad de veces que cada usuario realizó cada operación"""

    resultado = []

    for operacion in operaciones:
        # Tomo los datos de la operacion que corresponde
        informacion = datos[datos['Operacion'] == operacion]
        # Hago un merge para tener tambien los usuarios que no realizaron esa op
        merge = pd.merge(informacion, datos['Alias'], how='outer').fillna(0).sort_values(by='Alias')
        # Agrupo y me fijo cuantas hay en total
        merge = merge.groupby(['Alias','Cantidad']).size().reset_index()
        cantidad = merge['Cantidad'].tolist()
        #Agrego a la lista de resultados
        resultado.append(cantidad)


    return resultado

def grafico_barras_operaciones():

    """Se retorna un gráfico de barraas con las operaciones que realizó cada usuario"""

    st.markdown("""
                    Paso 1: Agrupo los datos por Alias y Operacion y cuento cuantas realizó cada usuario.<br>
                    Paso 2: Genero una lista con las operaciones realizadas.<br>
                    Paso 3: Genero una lista con la cantidad de operaciones de cada tipo.<br>
                    Paso 4: Creo un arreglo con los alias que hicieron las operaciones.
                """, unsafe_allow_html= True)

    datos = copia[['Alias', 'Operacion']]
    datos = datos.groupby(['Alias', 'Operacion']).size()
    datos = datos.reset_index(name='Cantidad')

    st.write ('Paso 1: ', datos)

    # Creo una lista con las operaciones
    operaciones = datos['Operacion'].unique().tolist()
    st.markdown('Paso 2: {}' .format(operaciones) )
    # Almaceno los resultados de la cantidad de operaciones de cada tipo
    resultados = convertidor(datos, operaciones)


    usuarios = datos['Alias'].unique()
    st.markdown('Paso 4: {}' .format(usuarios) )
    # Datos para las barras
    fig, ax = plt.subplots()
    # Hago un arreglo desde 0 hasta la cantidad de usuarios-1
    x = np.arange(len(usuarios))
    # Modifico las operaciones para que queden mas esteticas a la hora de mostrarse

    
    for i in range(len(operaciones)):
        datos = resultados[i]
        # En bottom pongo la suma de los datos anteriores para que se apilen
        ax.bar(x, datos, label=operaciones[i], bottom=np.sum(resultados[:i], axis=0))


    # Personalizar el gráfico
    ax.set_xlabel('Usuarios')
    ax.set_ylabel('Cantidad de operaciones')

    # Pongo las variables de salida  de x con la cantidad de operariones
    ax.set_xticks(x)
    # Pongo las variables de salida  de y con los usuarios
    ax.set_xticklabels(usuarios)
    # Agrego la leyenda para identificar las operaciones
    ax.legend()
    plt.xticks(rotation=90, ha='right')

    return fig

def imagenes_mas_usadas(operacion):
     
    """Se retorna un DataFrame com las imagenes mas usadas de 'generar meme'"""
    st.markdown("""
                    Paso 1: Selecciono solamente las filas que realizaron la operacion..<br>
                    Paso 2: Genero una lista todas las imagenes utilizadas(incluyendo las repetidas).<br>
                    Paso 3: Genero una lista de tuplas con  el nombre y las repeticiones de cada imagen.<br>
                    Paso 4: Creo un data frame con los datos.
                """, unsafe_allow_html= True)

    info = copia.dropna()
    info = info[['Alias', 'Operacion', 'Valores']]
    info = info[(info['Operacion'] == operacion)]
    st.write('Paso 1:' , info)

    lista_imagenes = []
    # Agrego todas las imagenes a una sola lista de imagenes
    valores = info['Valores'].astype(str)
    valores.apply(lambda x: lista_imagenes.extend(x.split(',')))
    st.markdown('Paso 2: {}' .format(lista_imagenes) )

    # Cuento cuantas hay de cada una
    repeticiones = Counter(lista_imagenes).most_common(3)
    st.markdown('Paso 3: {}' .format(repeticiones) )

    datos = pd.DataFrame(repeticiones, columns=['imagenes', 'repeticiones'])
    st.write ( 'Paso 4: ')
    # Los indices comienzan a partir de 1
    cant_filas = datos.shape[0]
    if (cant_filas < 3):
        numeros = range(1,cant_filas+1)
        lista = list(numeros)
        datos.index = lista
    else:
        datos.index = [1,2,3]

    return datos

def nube_palabras_memes():

    """Se retorna una nube de palabras con los textos mas escritos en los memes"""

    st.markdown("""
                    Paso 1: Selecciono solamente las filas que realizaron la operacion..<br>
                    Paso 2: Elimino las palabras repetidas.<br>
                    Paso 3: Genero una lista todas las palabras.<br>
                    Paso 4: Si la lista no esta vacia, genero un string con todas las palabras utilizadas.
                """, unsafe_allow_html= True)

    @st.cache_data()
    def generar_wordcloud(lista):
        wordcloud = WordCloud(width=300, height=200, random_state=1, background_color='white', colormap='Set2', collocations=False, stopwords=STOPWORDS).generate(lista)
        return wordcloud
    
    # Me quedo con las operaciones de generacion de meme
    info = copia[(copia['Operacion'] == 'generacion_meme')]
    # Creo una lista vacia para almacenar las palabras
    lista = []
    palabras = info['Texto'].astype(str)
    # Elimino las palabras repetidas
    palabras.unique()
    st.write('Paso 2: ' ,palabras )
    # Agrego a una sola lista todas las palabras
    palabras = palabras.apply(lambda x: lista.extend(x.split(',')))
    st.markdown('Paso 3: {}' .format(lista) )
    if len(lista) == 0:
        fig = 'No hay palabas para realizar una nube'
    else: 
        lista = ' '.join(lista)
        st.write('Paso 4: ', lista)
        wordcloud = WordCloud(width = 50, height = 50, random_state=1,background_color='white', colormap='Set2', collocations=False, stopwords =STOPWORDS).generate(lista)
        wordcloud = generar_wordcloud(lista)
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.figure = plt.figure(figsize=(20,10))
        # Mostrar la imagen
        ax.imshow(wordcloud)
        # Ocultar detalles de los ejes
        ax.axis("off")

    return fig

def nube_palabras_collage():

    """Se genera una nube de palabras con los textos mas utilizados en el collage"""

    st.markdown("""
                    Paso 1: Selecciono solamente las filas que realizaron la operacion..<br>
                    Paso 2: Elimino las palabras repetidas.<br>
                    Paso 3: Genero una lista todas las palabras.<br>
                    Paso 4: Si la lista no esta vacia, genero un string con todas las palabras utilizadas.
                """, unsafe_allow_html= True)

    @st.cache_data()
    def generar_wordcloud(lista):
        wordcloud = WordCloud(width=300, height=200, random_state=1, background_color='white', colormap='Set2', collocations=False, stopwords=STOPWORDS).generate(lista)
        return wordcloud
    

    # Me quedo con las operaciones de generacion de collage
    info = copia[(copia['Operacion'] == 'generacion_collage')]
    st.write('Paso 1', info)
    # Creo una lista vacia para almacenar las palabras
    lista = []
    palabras = info['Texto'].astype(str)
    # Elimino las palabras repetidas
    palabras.unique()
    st.write('Paso 2: ' ,palabras )
    # Agrego a una sola lista todas las palabras
    palabras = palabras.apply(lambda x: lista.extend(x.split(','))) 
    st.markdown('Paso 3: {}' .format(lista) )
    if len(lista) == 0:
        fig = 'No hay palabas para realizar una nube'
    else:
        lista = ' '.join(lista)
        st.write('Paso 4: ', lista)
        wordcloud = WordCloud(width = 50, height = 50, random_state=1,background_color='white', colormap='Set2', collocations=False, stopwords =STOPWORDS).generate(lista)
        wordcloud = generar_wordcloud(lista)
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.figure = plt.figure(figsize=(20,10))
        # Mostrar la imagen
        ax.imshow(wordcloud)
        # Ocultar detalles de los ejes
        ax.axis("off")

    return fig

def grafico_tortas_genero(operacion):

    """Se retorna un grafico de totas con los tipos de generos que realizaron la operación recibida como parametro"""

    st.markdown(""" 
                    Paso 1: Tomo los datos del json.<br>
                    Paso 2: Realizo un merge entre el json y el csv sobre el Alias.<br>
                    Paso 3: Almaceno solamente los que realizaron la operacipon.<br>
                    Paso 4: Genero una lista con las operaciones realizadas.<br>
                    Paso 5: Si dicha lista no es vacia, realizo el gráfico y sus datos serán el merge en la columa 'Genero'.

                """, unsafe_allow_html= True)

    #Datos
    datos_json = json[['Alias', 'Genero']]
    st.write('Paso 1: ', datos_json)

    #Realizo un merge entre el json y el csv
    merge = pd.merge(copia, datos_json, on= 'Alias', how= 'left')
    st.write('Paso 2:', merge)
    merge = merge[(merge['Operacion'] == operacion)]
    st.write('Paso 3:', merge)

    lista = (merge['Operacion'].tolist())
    st.markdown('Paso 4: {}' .format(lista) )
    if len(lista) == 0:
        fig = f'Aún no se han realizado operaciones de {operacion}.'
    else:
        fig, ax = plt.subplots(figsize=(8,4))
        datos = merge['Genero'].value_counts()
        st.write(datos)

        ax.pie(datos, labels=merge['Genero'].unique(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Asegura que el gráfico sea una figura circular

    return fig
import PySimpleGUI as sg
import json
import os
import unlpimage.interfaces.agregar_perfil as ap
import unlpimage.funcionalidad.funciones_agregar_perfil as funciones_agregar_perfil
import unlpimage.interfaces.menu_principal as mp
import unlpimage.funcionalidad.layout_inicio as layout_inicio
from unlpimage.funcionalidad.paths import DIR_PROYECTO

# Rutas relativas que van a ser utilizadas

def inicializar_programa():
    
    usuarios = []

    ruta_imagenes = os.path.join(DIR_PROYECTO, 'imagenes_proyecto', 'imagenes_perfiles')

    # Cargar los datos de los usuarios desde el archivo JSON
    usuarios = funciones_agregar_perfil.informacion_json()

    return ruta_imagenes, usuarios

def mostrar_todos_los_usuarios(usuarios, ruta_imagenes):
    """"
    funcion que genera una pantalla para seleccionar entre todos los usuarios
    que se encuentran en el archivo json
    """
    # Definimos los tamaños de los botones
    max_botones_por_fila = 4

    # Creamos la lista de botones
    botones = []
    fila_botones = []
    contador_botones_en_fila = 0

    # Mostramos los botones de usuario
    for usuario in usuarios:
        if contador_botones_en_fila == max_botones_por_fila:
            botones.append(fila_botones)
            fila_botones = []
            contador_botones_en_fila = 0

        nombre_imagen = usuario["Imagen"]
        ruta_imagen = os.path.join(ruta_imagenes, nombre_imagen)
        fila_botones.append(sg.Button(image_source= ruta_imagen, image_size=(128,128), size=(12,5), key=usuario["Alias"], tooltip=usuario["Alias"]))

        contador_botones_en_fila += 1

    # Si no se terminó de completar la última fila de botones, la agregamos a la lista de botones
    if fila_botones:
        botones.append(fila_botones)

    # Agregamos un botón de "Volver"
    botones.append([sg.Button('Volver', size=(10,2), key='-VOLVER-')])

    # Creamos el layout con los botones
    layout = [
        [sg.Text('UNLPImage', font=('Helvetica', 20), pad=((20, 0), (20, 10)), background_color="#000000")],
        [sg.Column(botones, scrollable=True, vertical_scroll_only=True, background_color="#000000", justification='center', size=(None, None), expand_x=True, expand_y=True, pad=(100, 0))],
    ]




    # Creamos la ventana
    ventana = sg.Window('Todos los usuarios', layout, size=(800, 600), resizable=True, background_color="#000000")

    # Mostramos la ventana y leemos eventos
    while True:
        evento, valores = ventana.read()
        if evento == sg.WIN_CLOSED:
            break
        # Manejamos los eventos según su key
        if evento == '-VOLVER-':
            ventana.close()
            generar_pantalla_inicio()
        elif evento in [usuario["Alias"] for usuario in usuarios]:
            ventana.close()
            usuario_seleccionado = next(usuario for usuario in usuarios if usuario["Alias"] == evento)
            mp.menu_principal(usuario_seleccionado)
            break

    # Cerramos la ventana y terminamos el programa
    ventana.close()




def procesar_inicio ( ventana_actual, evento, usuarios, ruta_imagenes):

    
    if evento == '-INICIO-AGREGAR-PERFIL-':
    #abre la ventan de agregar perfil
        ventana_actual.close()
        funciones_agregar_perfil.crear_ventana_agregar_perfil()
    elif evento == '-INICIO-MOSTRAR-PERFILES-':
        #cierro la ventana actual
        #muestra todos los usuarios existentes
        ventana_actual.close()
        mostrar_todos_los_usuarios(usuarios, ruta_imagenes )
        
    elif evento.split("-")[2] in [usuario["Alias"] for usuario in usuarios]:
        usuario_seleccionado = next(usuario for usuario in usuarios if usuario["Alias"] == evento.split("-")[2])
        #abro el menu principal
        ventana_actual.close()
        mp.menu_principal(usuario_seleccionado)
        
        





def generar_pantalla_inicio():
    """"
    Esta función genera una pantalla con las opciones de agregar perfil y de presionar sobre 
    una imagen de perfil para acceder a su menu principal

    """
    ruta_imagenes, usuarios = inicializar_programa()

    lista = [ruta_imagenes, usuarios]

    ventana_actual = layout_inicio.layouts(ruta_imagenes, usuarios )
    
    imagen_actual = '0.png'
    # Mostramos la ventana y leemos eventos
    while True:

        ventana_actual, evento, valores = sg.read_all_windows()
        
        if evento == sg.WIN_CLOSED:
            break

        evento_palabra = evento.split("-")[1]
        
        match evento_palabra:
            case 'INICIO':
                procesar_inicio ( ventana_actual, evento, usuarios, ruta_imagenes )
                if evento.split("-")[2] in [usuario["Alias"] for usuario in usuarios]:
                    break              
            case 'AGREGAR':
                usuarios, imagen_actual = ap.procesar_eventos(ventana_actual, evento, valores, imagen_actual, lista)
        

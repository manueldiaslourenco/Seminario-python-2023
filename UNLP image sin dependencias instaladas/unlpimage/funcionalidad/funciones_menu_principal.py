import os
import io
import json
import csv
import PySimpleGUI as sg
from datetime import datetime
from PIL import Image
from PIL import ImageDraw 
from PIL import ImageOps 
from PIL import ImageTk 
from PIL import ImageFont
from unlpimage.funcionalidad.paths import DIR_PROYECTO
import unlpimage.funcionalidad.paths as p

def crear_archivo_guardar_configuracion():
    """Esta funcion crea archivo que contiene la configuración de la aplicación."""

    ruta_json = os.path.join(DIR_PROYECTO,'data','ruta_configuracion.json')
    ruta_imagenes = os.path.join(DIR_PROYECTO,'imagenes_proyecto','imagenes_etiquetar')
    ruta_collage = os.path.join(DIR_PROYECTO,'imagenes_proyecto','imagenes_collage')
    ruta_memes = os.path.join(DIR_PROYECTO,'imagenes_proyecto','imagenes_memes')
    rutas_por_defecto = { "ruta_imagenes": p.convertir_para_guardar(ruta_imagenes,DIR_PROYECTO), "ruta_collage": p.convertir_para_guardar(ruta_collage,DIR_PROYECTO), "ruta_memes": p.convertir_para_guardar(ruta_memes,DIR_PROYECTO) }
    escribir_json(ruta_json, rutas_por_defecto)

def existe_archivo( ruta ):
    """Esta funcion revisa si el archivo existe en una ruta determinada."""
    
    if os.path.isfile(ruta):
        return True
    else:
        return False

def informacion_archivo_json():
    """Esta funcion devuelve informacion de las rutas de mi archivo de configuracion json."""

    ruta_json = os.path.join(DIR_PROYECTO,'data','ruta_configuracion.json')
    rutas = leer_json(ruta_json)
    imagenes = rutas ["ruta_imagenes"]
    collage = rutas ["ruta_collage"]
    memes = rutas ["ruta_memes"]
    return imagenes,collage,memes

def actualizar_informacion_archivo(imagenes,collage,memes):
    """Esta funcion actualiza la informacion de las rutas de mi archivo de configuracion json."""

    rutas_actualizadas = {"ruta_imagenes": imagenes, "ruta_collage": collage, "ruta_memes":memes}
    ruta_json = os.path.join(DIR_PROYECTO,'data','ruta_configuracion.json')
    escribir_json(ruta_json, rutas_actualizadas)


def calculo_formato_resolucion_peso(ruta_completa):
    """Esta funcion calcula la informacion de la imagen seleccionada(resolucion,formato,tamaño)"""

    imagen = Image.open(ruta_completa)
    resolucion = imagen.size
    formato = imagen.format
    imagen.close()
    peso = os.path.getsize(ruta_completa)
    peso_final = peso/(1024 * 1024)
    peso_final = peso/1024
    return formato, resolucion, f" {peso_final:.2f} KB "

def actualizar_ventana_etiquetar(ruta_completa,ventana_actual,datos,tags,descripcion):
    """Esta funcion actualiza el layout de la ventana etiquetar imagenes con sus respectivos datos."""

    imagen = Image.open(ruta_completa)
    imagen.thumbnail((200,150))
    bio = io.BytesIO()
    imagen.save(bio, format="PNG")
    ventana_actual["-IMAGEN-SELECCIONADA-"].update(data=bio.getvalue())
    ventana_actual["-IMAGEN-SELECCIONADA-"].update(visible=True)
    ventana_actual["-ETIQUETAR-DATOS-IMAGENES-"].update(f" | {datos[4]} |  {datos[3]} | {datos[2][0]}x{datos[2][1]} | ")
    ventana_actual["-ETIQUETAR-DATOS-IMAGENES-"].update(visible=True)
    ventana_actual["-ETIQUETAR-TAG-"].update(disabled=False)
    ventana_actual["-ETIQUETAR-AGREGAR-TAG-"].update(disabled=False)
    ventana_actual["-ETIQUETAR-ELIMINAR-TAG-"].update(disabled=False)
    ventana_actual["-ETIQUETAR-DESCRIPCION-"].update(disabled=False)
    ventana_actual["-ETIQUETAR-AGREGAR-DESCRIPCION-"].update(disabled=False)
    ventana_actual["-ETIQUETAR-ELIMINAR-DESCRIPCION-"].update(disabled=False)
    ventana_actual["-ETIQUETAR-GUARDAR-"].update(disabled=False)
    cadena_tags = 'Tags: '+ ' | '.join(map(str, tags))
    ventana_actual["-ETIQUETAR-MOSTRAR-TAG-"].update(cadena_tags)
    ventana_actual["-ETIQUETAR-MOSTRAR-DESCRIPCION-"].update("Descripcion: " + descripcion)

def crear_archivo_csv(encabezado,ruta_relativa):
    """Esta funcion crea archivo en csv con su respectivo encabezado."""
    try:
        with open(ruta_relativa, 'w', newline='') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(encabezado)
    except PermissionError:
        sg.popup('No tiene permisos de escritura sobre el archivo. La aplicación finalizará')
    except FileNotFoundError:
        sg.popup('No se ha encontrado el archivo. La apliación finalizará.')
    except:
        sg.popup('Ups! Ha ocurrido un error. La aplicación finalizará.')

def cargar_linea_csv(linea,ruta_relativa):
    """Esta funcion agrega una linea nueva en un archivo csv ya existente."""
    try:
        with open(ruta_relativa, 'a', newline='') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(linea)
    except PermissionError:
        sg.popup('No tiene permisos de escritura sobre el archivo. La aplicación finalizará')
    except FileNotFoundError:
        sg.popup('No se ha encontrado el archivo. La apliación finalizará.')
    except:
        sg.popup('Ups! Ha ocurrido un error. La aplicación finalizará.')

def verificar_ruta_en_csv(ruta_relativa):
    """Esta funcion verifica si se encuentra un dato(en este caso ruta relativa de la imagen) el archivo csv."""
    esta = False
    lista_encontrada= []
    try:
        ruta_archivo_etiquetar = os.path.join (DIR_PROYECTO,'data', "informacion_imagenes.csv")
        with open(ruta_archivo_etiquetar, 'r') as archivo:
            lector = csv.reader(archivo)
            # línea del encabezado
            next(lector)
            for linea in lector:
                ruta_actual = linea[0].strip()  # Eliminar espacios en blanco adicionales
                if ruta_actual.lower() == ruta_relativa.strip().lower():
                    lista_encontrada= linea.copy()
                    esta = True
    except PermissionError:
        sg.popup('No tiene permisos de escritura sobre el archivo. La aplicación finalizará')
    except FileNotFoundError:
        sg.popup('No se ha encontrado el archivo. La apliación finalizará.')
    except:
        sg.popup('Ups! Ha ocurrido un error. La aplicación finalizará.')   
    return lista_encontrada, esta

def buscar_reescribir_en_csv(imagen, tags, descripcion, fecha, usuario):
    """Esta funcion reescribe lineas en el csv debiendo copiar nuevamente todo el archivo con su linea cambiada."""

    
    archivo_temporal = os.path.join (DIR_PROYECTO,'data', 'informacion_imagenes_temporal.csv')
    archivo_original = os.path.join (DIR_PROYECTO,'data', "informacion_imagenes.csv")

    try:
        with open(archivo_original, 'r', newline='') as archivo_orig, open(archivo_temporal, 'w', newline='') as archivo_temp:
            lector = csv.reader(archivo_orig)
            escritor = csv.writer(archivo_temp)
            # Copiar la línea de encabezado al archivo temporal
            encabezado = next(lector)
            escritor.writerow(encabezado)
            # Copiar las líneas del archivo original al archivo temporal, realizando modificaciones en la línea deseada
            for linea in lector:
                if linea[0] == imagen:
                    linea[5] = ','.join(map(str, tags))
                    linea[1] = descripcion
                    linea[6] = usuario["Alias"]
                    linea[7] = fecha
                escritor.writerow(linea)
    except PermissionError:
        sg.popup('No tiene permisos de escritura sobre el archivo. La aplicación finalizará')
    except FileNotFoundError:
        sg.popup('No se ha encontrado el archivo. La apliación finalizará.')
    except:
        print ('buscar_reescribir_en_csv')
        sg.popup('Ups! Ha ocurrido un error. La aplicación finalizará.')

    os.replace(archivo_temporal, archivo_original)



def registro_carga_logs(alias,operacion, valores = '', texto = ''):
    """Esta funcion agrega una linea en el archivo de logs.csv."""
    
    fecha= datetime.timestamp(datetime.now())
    linea = [alias,operacion,fecha, valores, texto]
    ruta_logs= os.path.join(DIR_PROYECTO, 'data', 'logs_sistema.csv')
    cargar_linea_csv(linea, ruta_logs)

def actualizar_usuario ( usuario_modificado, valores, imagen ):
    """Esta funcion actualiza el perfil de un usuario."""

    usuario_modificado['Nombre'] = valores['-EDITAR-NOMBRE-'] 
    usuario_modificado['Edad'] = valores['-EDITAR-EDAD-'] 
    usuario_modificado['Genero'] = valores['-EDITAR-COMBO-'] 
    usuario_modificado['Imagen'] = imagen

    ruta_perfiles = os.path.join(DIR_PROYECTO,'data', 'datos_usuarios.json')

    usuarios= leer_json(ruta_perfiles)
    
    for usuario in usuarios:
        if usuario_modificado['Alias'] == usuario["Alias"] :
            usuario.update(usuario_modificado)

    escribir_json(ruta_perfiles,usuarios)


def leer_json (ruta_json):
    """Leo el json y devuelvo sus datos"""

    try: 
        if existe_archivo (ruta_json):
            with open(ruta_json, 'r') as f:
                datos = json.load(f)
        else:
            datos = []
        return datos
    except PermissionError:
        sg.popup('No tiene permisos de lectura sobre el archivo. La aplicación finalizará')
    except FileNotFoundError:
        sg.popup('No se ha encontrado el archivo. La apliación finalizará.')
    except:
        sg.popup('Ups! Ha ocurrido un error, la aplicación finalizará.')

def escribir_json (ruta_json, datos):
    """Abro y escribo los datos pasados como parametros en el json correspondiente"""

    try: 
        with open(ruta_json, 'w') as f:
            json.dump(datos, f, indent=4)
    except PermissionError:
        sg.popup('No tiene permisos de escritura sobre el archivo. La aplicación finalizará')
    except FileNotFoundError:
        sg.popup('No se ha encontrado el archivo. La apliación finalizará.')
    except:
        sg.popup('Ups! Ha ocurrido un error. La aplicación finalizará.')

def Cumple( cant, num):
    """Devuelvo un booleano si cumple la condición. """
    if(cant >= num):
        return True
    else:
        return False

def tam_box(x1, y1, x2, y2):
    """Calculo ancho y alto de una caja."""
    return (x2 - x1 , y2 - y1)

def entra(contenedor, contenido):
    """Devuelvo verdadero si entra el contenido dentro del contenedor."""
    return contenido[0] <= contenedor[0] and contenido[1] <= contenedor[1]

def calcular_tam_fuente(draw, texto, path_fuente, box):
    """Calculo tamaño de fuente."""
    tam_contenedor = tam_box(*box)
    for tam in range(105, 10, -5):
        fuente= ImageFont.truetype(path_fuente,tam)
        box_texto = draw.textbbox((0,0),texto, font= fuente)
        tam_box_texto = tam_box(*box_texto)
        if entra(tam_contenedor, tam_box_texto):
            return fuente
        
    return fuente

def actualizoimagen(texto_a_mostrar,draw,cajas_texto,num,letra):
    top_left_x= cajas_texto["text_boxes"][num]["top_left_x"]
    top_left_y= cajas_texto["text_boxes"][num]["top_left_y"]
    bottom_right_x= cajas_texto["text_boxes"][num]["bottom_right_x"]
    bottom_right_y= cajas_texto["text_boxes"][num]["bottom_right_y"]
    fuente_ajustada= calcular_tam_fuente(draw, texto_a_mostrar,letra,(top_left_x,top_left_y,bottom_right_x,bottom_right_y))
    if num == 0:
        draw= draw.text(( top_left_x, top_left_y), texto_a_mostrar, font=fuente_ajustada,fill=(0,0,0))
    elif num == 1:
        draw= draw.text(( top_left_x, top_left_y ), texto_a_mostrar, font=fuente_ajustada,fill=(0,0,0))
    elif num == 2:
        draw= draw.text(( top_left_x, top_left_y ), texto_a_mostrar, font=fuente_ajustada,fill=(0,0,0))
    elif num == 3:
        draw= draw.text(( top_left_x, top_left_y ), texto_a_mostrar, font=fuente_ajustada,fill=(0,0,0))
    
def ajustar_imagen(imagen, tamaño):
    return ImageOps.fit(imagen, tamaño)


def actualizar_vista_previa(ventana, nombre_imagenes):
    """
    Esta función actualiza la imagen que se muestra como vista previa en la generación de collage.
    """
    nombre_imagenes= []
    IMAGE_SIZE = (500, 500)
    collage_path = "temp_collage.png"

    # Obtengo los valores de los combos, el título ingresado por el usuario y el tipo de diseño
    imagen1 = ventana['-COLLAGE-ACTUALIZAR-1'].get()
    imagen2 = ventana['-COLLAGE-ACTUALIZAR-2'].get()
    imagen3 = ventana['-COLLAGE-ACTUALIZAR-3'].get()
    titulo = ventana['-COLLAGE-TITULO-'].get()
    diseño_texto = ventana["-COLLAGE-DISEÑO-"].get()
    diseño = int(diseño_texto.split()[-1])

    # Leer la configuración del archivo JSON
    ruta_imagenes_etiquetar = p.convertir_guardado_para_usar(informacion_archivo_json()[0],DIR_PROYECTO)

    #Esta función genera un diccionario utilizando el archivo csv de información de imágenes.
    imagenes_etiquetar = crear_diccionario_collage()

    # Generar la nueva imagen de collage
    collage = Image.new("RGB", IMAGE_SIZE)

    if imagen1:
        imagen1_path = os.path.join(DIR_PROYECTO, ruta_imagenes_etiquetar, imagenes_etiquetar[imagen1])
        nombre_imagenes.append(imagenes_etiquetar[imagen1])
        imagen1 = Image.open(imagen1_path)
        if diseño == 1:
            imagen1 = ajustar_imagen(imagen1, (250, 500))
            collage.paste(imagen1, (0, 0))
        elif diseño == 2:
            imagen1 = ajustar_imagen(imagen1, (250, 250))
            collage.paste(imagen1, (0, 0))
        elif diseño == 3:
            imagen1 = ajustar_imagen(imagen1, (500, 250))
            collage.paste(imagen1, (0, 0))
        elif diseño == 4:
            imagen1 = ajustar_imagen(imagen1, (166, 500))
            collage.paste(imagen1, (0, 0))

    if imagen2:
        imagen2_path = os.path.join(DIR_PROYECTO, ruta_imagenes_etiquetar, imagenes_etiquetar[imagen2])
        nombre_imagenes.append(imagenes_etiquetar[imagen2])
        imagen2 = Image.open(imagen2_path)
        if diseño == 1:
            imagen2 = ajustar_imagen(imagen2, (250, 250))
            collage.paste(imagen2, (250, 0))
        elif diseño == 2:
            imagen2 = ajustar_imagen(imagen2, (250, 250))
            collage.paste(imagen2, (0, 250))
        elif diseño == 3:
            imagen2 = ajustar_imagen(imagen2, (250, 250))
            collage.paste(imagen2, (0, 250))
        elif diseño == 4:
            imagen2 = ajustar_imagen(imagen2, (166, 500))
            collage.paste(imagen2, (166, 0))

    if imagen3:
        imagen3_path = os.path.join(DIR_PROYECTO, ruta_imagenes_etiquetar, imagenes_etiquetar[imagen3])
        nombre_imagenes.append(imagenes_etiquetar[imagen3])
        imagen3 = Image.open(imagen3_path)
        if diseño == 1:
            imagen3 = ajustar_imagen(imagen3, (250, 250))
            collage.paste(imagen3, (250, 250))
        elif diseño == 2:
            imagen3 = ajustar_imagen(imagen3, (250, 500))
            collage.paste(imagen3, (250, 0))
        elif diseño == 3:
            imagen3 = ajustar_imagen(imagen3, (250, 250))
            collage.paste(imagen3, (250, 250))
        elif diseño == 4:
            imagen3 = ajustar_imagen(imagen3, (166, 500))
            collage.paste(imagen3, (333, 0))

    

    if titulo:
        # Agregar el título al collage
        draw = ImageDraw.Draw(collage)
        fuente = os.path.join(DIR_PROYECTO, 'fuentes', 'arial_narrow_7.ttf' )
        font = ImageFont.truetype(fuente, 24)
        text_width, text_height = draw.textsize(titulo, font=font)
        text_position = ((IMAGE_SIZE[0] - text_width) // 2, IMAGE_SIZE[1] - text_height - 10)

        # Dibujar un rectángulo blanco detrás del texto
        bbox = [
            text_position[0] - 5,
            text_position[1] - 5,
            text_position[0] + text_width + 5,
            text_position[1] + text_height + 5
        ]
        draw.rectangle(bbox, fill=(255, 255, 255))
        draw.text(text_position, titulo, font=font, fill=(0, 0, 0))

    collage.save(collage_path, format="PNG")

    # Cargar la nueva imagen de collage como bytes
    with open(collage_path, 'rb') as f:
        imagen_bytes = f.read()

    return nombre_imagenes, imagen_bytes



def crear_diccionario_collage():
    """
    Esta función genera un diccionario utilizando el archivo csv de información de imágenes.
    El diccionario guarda la descripción como clave y el nombre de la imagen como valor.
    """
    ruta_csv = os.path.join(DIR_PROYECTO, 'data', 'informacion_imagenes.csv')
    imagenes_etiquetar = {}

    try:
        with open(ruta_csv, "r") as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            next(lector_csv)

            # Me guardo la descripción como clave y el nombre de la imagen como valor
            for fila in lector_csv:
                ruta_imagen = fila[0]
                texto_descriptivo = fila[1]
                imagenes_etiquetar[texto_descriptivo] = ruta_imagen

    except FileNotFoundError:
        sg.popup("No se encontró el archivo")
    except:
        sg.popup("Se produjo un error.")

    return imagenes_etiquetar

def obtener_descripciones_imagenes(ruta_csv, ruta_imagenes_etiquetar):
    """
    Esta función retorna una lista con las descripciones de aquellas imagenes que se encuentran en la carpeta de imagenes configurada.
    """
    imagenes_etiquetar = crear_diccionario_collage()
    archivos_etiquetar = os.listdir(ruta_imagenes_etiquetar)
    descripciones_imagenes = []

    for descripcion, ruta_imagen in imagenes_etiquetar.items():
        nombre_archivo = os.path.basename(ruta_imagen)
        if nombre_archivo in archivos_etiquetar:
            descripciones_imagenes.append(descripcion)

    return descripciones_imagenes
import PySimpleGUI as sg
import os
import unlpimage.funcionalidad.ventanas as ventanas
import unlpimage.funcionalidad.principal as principal
import unlpimage.interfaces.configuracion as configuracion
import unlpimage.interfaces.editar_perfil as editar
import unlpimage.interfaces.etiquetar_imagenes as etiquetar
import unlpimage.interfaces.generar_collage as collage
import unlpimage.interfaces.diseño_collage as diseño
import unlpimage.interfaces.generar_meme as generar_meme
import unlpimage.interfaces.template_meme as template
import unlpimage.funcionalidad.funciones_menu_principal as f
from unlpimage.funcionalidad.paths import DIR_PROYECTO

def menu_principal(usuario):
    ventanas.crear_ventana_principal(usuario["Imagen"])
    tags= set()
    descripcion = ""
    datos= []
    imagen_actual= usuario["Imagen"]
    ruta_config_json= os.path.join (DIR_PROYECTO, "data" ,"ruta_configuracion.json")
    if not f.existe_archivo(ruta_config_json):
        f.crear_archivo_guardar_configuracion()
    
    ruta_memes_json= os.path.join (DIR_PROYECTO, "data","box_memes.json")
    templates = f.leer_json(ruta_memes_json)
    cantidad = 0
    meme_actualizado= None
    lista_textos= []
    nombre_imagenes = []
    
    while True:
        ventana_actual, evento, valores = sg.read_all_windows()
        
        if evento == sg.WIN_CLOSED:
            break

        evento_palabra = evento.split("-")[1]
        
        match evento_palabra:
            case "PRINCIPAL":
                principal.procesar_eventos(ventana_actual, evento,usuario)
                if( evento== "-PRINCIPAL-SALIR-"):
                    break
            case "CONFIGURACION":
                configuracion.procesar_eventos(ventana_actual, evento,valores,usuario)
            case "AYUDA":
                ventana_actual.close()
                ventanas.crear_ventana_principal(usuario)
            case "EDITAR":
                imagen_actual= editar.procesar_eventos(ventana_actual,evento,valores, usuario, imagen_actual)
            case "DISEÑO":
                diseño.procesar_eventos(ventana_actual,evento, usuario["Imagen"])
            case "COLLAGE":
                nombre_imagenes = collage.procesar_eventos(ventana_actual,evento, valores, nombre_imagenes, usuario)
            case "TEMPLATE":
                meme_original, actual, cantidad = template.procesar_eventos(ventana_actual,evento,valores,usuario["Imagen"])
                cajas_texto = next((item for item in templates if item.get("image") == actual), None)
            case "MEME":
                meme_actualizado,lista_textos= generar_meme.procesar_eventos(ventana_actual,evento,valores, usuario, meme_original, cajas_texto,cantidad, meme_actualizado,lista_textos)
            case "ETIQUETAR":
                tags, descripcion, datos= etiquetar.procesar_eventos(ventana_actual,evento,valores,tags,descripcion,usuario,datos)
            

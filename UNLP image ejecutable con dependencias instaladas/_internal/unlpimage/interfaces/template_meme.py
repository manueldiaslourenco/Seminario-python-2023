import PySimpleGUI as sg
import os
from PIL import Image
from PIL import ImageTk
from unlpimage.funcionalidad.paths import DIR_PROYECTO
import unlpimage.funcionalidad.ventanas as ventanas

def procesar_eventos(ventana_actual, evento, valores,usuario_imagen):
    #Falta por implementar mas eventos.
    cantidad=0
    if evento == "-TEMPLATE-SELECCION-IMAGEN-":
        actual= valores["-TEMPLATE-SELECCION-IMAGEN-"][0]
        imagen_original = Image.open(os.path.join(DIR_PROYECTO,"imagenes_proyecto", "creacion_memes", actual))
        imagen_original.thumbnail((300,300))
        imagen_original_tk = ImageTk.PhotoImage(imagen_original)

        ventana_actual["-TEMPLATE-SELECCIONADO-"].update(data= imagen_original_tk)
        ventana_actual["-TEMPLATE-SELECCIONADO-"].update(visible= True)
        ventana_actual["-TEMPLATE-GENERAR-"].update(disabled= False)
    elif evento == "-TEMPLATE-VOLVER-":
        imagen_original= None
        actual= ""
        ventana_actual.close()
        ventanas.crear_ventana_principal(usuario_imagen)
    elif evento == "-TEMPLATE-GENERAR-":
        actual= valores["-TEMPLATE-SELECCION-IMAGEN-"][0]
        cantidad= actual.split("-")[1]
        imagen_original = Image.open(os.path.join(DIR_PROYECTO,"imagenes_proyecto", "creacion_memes", actual))
        imagen_original_tk = ImageTk.PhotoImage(imagen_original)
        ventana_actual.close()
        ventana_actual= ventanas.crear_ventana_generar_meme(int(cantidad))
        ventana_actual["-MEME-SELECCIONADO-"].update(data= imagen_original_tk)
    
    return imagen_original, actual, int(cantidad)
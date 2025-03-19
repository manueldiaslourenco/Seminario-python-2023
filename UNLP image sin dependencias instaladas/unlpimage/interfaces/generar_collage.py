import PySimpleGUI as sg
import unlpimage.funcionalidad.ventanas as v
from PIL import Image, ImageDraw, ImageOps, ImageTk
import io
import unlpimage.funcionalidad.funciones_menu_principal as f
from unlpimage.funcionalidad.paths import DIR_PROYECTO
import unlpimage.funcionalidad.paths as paths
import os
from datetime import datetime


IMAGE_SIZE = (400,400)
def procesar_eventos(ventana_actual, evento, valores, nombre_imagenes, usuario):
    """
    Esta función procesa los eventos de la ventana de generación de collage
    """
    if evento == "-COLLAGE-VOLVER-":
        v.crear_ventana_diseño_collage()
        ventana_actual.close()
        nombre_imagenes = []
        ruta_imagen_temp= os.path.join('temp_collage.png')
        os.remove(ruta_imagen_temp)
        
    elif evento == '-COLLAGE-ACTUALIZAR-TITULO' or evento.startswith('-COLLAGE-ACTUALIZAR-'):
        nombre_imagenes, imagen_collage = f.actualizar_vista_previa(ventana_actual, nombre_imagenes)
        ventana_actual['-IMAGEN-COLLAGE-'].update(data=imagen_collage)
        ventana_actual['-COLLAGE-GUARDAR-'].update(disabled= False)

    elif evento == "-COLLAGE-GUARDAR-":
        ruta_imagenes_guardar= paths.convertir_guardado_para_usar(f.informacion_archivo_json()[1],DIR_PROYECTO)
        imagen_collage = ventana_actual["-IMAGEN-COLLAGE-"].Filename
    
        # Crear la carpeta de destino si no existe
        os.makedirs(ruta_imagenes_guardar, exist_ok=True)
        try:
        # Generar un nombre de archivo único usando la fecha y hora actual
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"imagen_{timestamp}.png"

            # Guardar la imagen en la carpeta de destino con el nombre único
            ruta_imagenes_guardar= os.path.join(ruta_imagenes_guardar,nombre_archivo)
            Image.open(imagen_collage).save(ruta_imagenes_guardar)

            sg.popup("Imagen guardada correctamente", title="Éxito")

            operacion = "generacion_collage"
            imagenes_logs = ','.join(filter(lambda x: x != '', nombre_imagenes))
            f.registro_carga_logs(usuario["Alias"],operacion,imagenes_logs,valores['-COLLAGE-TITULO-'])

        except Exception as e:
            sg.popup(f"No se pudo guardar la imagen: {str(e)}", title="Error")

        v.crear_ventana_principal(usuario['Imagen'])
        ventana_actual.close()
        ruta_imagen_temp= os.path.join('temp_collage.png')
        os.remove(ruta_imagen_temp)

    return nombre_imagenes
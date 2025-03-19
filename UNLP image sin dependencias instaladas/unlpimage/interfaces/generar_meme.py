import PySimpleGUI as sg
import os
from PIL import ImageDraw
from PIL import ImageTk
import unlpimage.funcionalidad.ventanas as ventanas
import unlpimage.funcionalidad.paths as p
from unlpimage.funcionalidad.paths import DIR_PROYECTO
import unlpimage.funcionalidad.funciones_menu_principal as f

def procesar_eventos(ventana_actual, evento, valores,usuario, meme_original,cajas_texto,cantidad,meme,lista_textos):

    if evento == "-MEME-ACTUALIZAR-":
        letra = os.path.join(DIR_PROYECTO,"fuentes",valores["-MEME-FUENTE-"]+ ".ttf")
        meme = meme_original.copy()
        lista_textos= []
        texto_a_mostrar = valores["-MEME-TEXTO1-"]
        draw = ImageDraw.Draw(meme)
        for i in range(0,cantidad,1):
            texto_a_mostrar = valores[f"-MEME-TEXTO{i + 1}-"]
            lista_textos.append(texto_a_mostrar)
            f.actualizoimagen(texto_a_mostrar,draw,cajas_texto,i,letra)
   
        actualizada = ImageTk.PhotoImage(meme)
        ventana_actual["-MEME-SELECCIONADO-"].update(data= actualizada)
        ventana_actual["-MEME-NOMBRE-GUARDAR-"].update(disabled= False)
        ventana_actual["-MEME-GUARDAR-"].update(disabled= False)

    elif evento == "-MEME-VOLVER-":
        ventana_actual.close()
        ventanas.crear_ventana_seleccionar_template()
    elif evento == "-MEME-GUARDAR-":
        nombre_archivo= valores["-MEME-NOMBRE-GUARDAR-"]
        ruta_guardar= p.convertir_guardado_para_usar(f.informacion_archivo_json()[2],DIR_PROYECTO)
        ruta_guardar= os.path.join(ruta_guardar,nombre_archivo)
        meme.save(ruta_guardar)
        operacion = "generacion_meme"
        texto_logs = ','.join(filter(lambda x: x != '', lista_textos))
        f.registro_carga_logs(usuario["Alias"],operacion,cajas_texto["image"],texto_logs)
        ventana_actual.close()
        ventanas.crear_ventana_principal(usuario["Imagen"])

    return meme, lista_textos
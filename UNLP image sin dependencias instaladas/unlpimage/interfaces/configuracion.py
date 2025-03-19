import PySimpleGUI as sg
import unlpimage.funcionalidad.ventanas as ventanas
import unlpimage.funcionalidad.funciones_menu_principal as f
from unlpimage.funcionalidad.paths import DIR_PROYECTO
import unlpimage.funcionalidad.paths as p

def procesar_eventos(ventana_actual, evento,valores,usuario):
    if evento == "-CONFIGURACION-VOLVER-":
        ventanas.crear_ventana_principal(usuario["Imagen"])
        ventana_actual.close()
    elif evento == "-CONFIGURACION-GUARDAR-":
        ruta1 = p.convertir_guardado_para_usar(valores[0],DIR_PROYECTO)
        ruta1 = p.convertir_para_guardar(ruta1,DIR_PROYECTO)
        ruta2 = p.convertir_guardado_para_usar(valores[1],DIR_PROYECTO)
        ruta2 = p.convertir_para_guardar(ruta2,DIR_PROYECTO)
        ruta3 = p.convertir_guardado_para_usar(valores[2],DIR_PROYECTO)
        ruta3 = p.convertir_para_guardar(ruta3,DIR_PROYECTO)
        f.actualizar_informacion_archivo(ruta1,ruta2,ruta3)
        operacion = "cambio_configuracion"
        f.registro_carga_logs(usuario["Alias"],operacion)
        sg.popup("Los Datos se actualizaron con exito")
    
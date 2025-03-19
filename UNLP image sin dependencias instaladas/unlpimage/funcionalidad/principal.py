import os
import unlpimage.funcionalidad.funciones_menu_principal as f
import unlpimage.funcionalidad.ventanas as v
import unlpimage.interfaces.inicio as inicio
from unlpimage.funcionalidad.paths import DIR_PROYECTO


def procesar_eventos(ventana_actual, evento,usuario):
    usuario_imagen = usuario["Imagen"]
    if evento == "-PRINCIPAL-CONFIG-":
        texto= f.informacion_archivo_json()
        ventana_actual.close()
        v.crear_ventana_configuracion(texto[0], texto[1], texto[2])
        
        
    elif evento == "-PRINCIPAL-AYUDA-":
        ventana_actual.close()
        v.crear_ventana_ayuda()
    
    elif evento == "-PRINCIPAL-NICK-":
        ventana_actual.close()
        v.crear_ventana_editar_perfil(usuario)
    
    elif evento == "-PRINCIPAL-ETIQUETAR-":
        ruta_completa= os.path.join (DIR_PROYECTO,'data', "informacion_imagenes.csv")
        if not f.existe_archivo(ruta_completa) :
            encabezado = ['ruta', 'texto descriptivo', 'resolucion', 'tamano', 'tipo', 'lista de tags', 'perfil actualizo', 'ultima actualizacion']
            f.crear_archivo_csv(encabezado,ruta_completa)

        ventana_actual.close()
        v.crear_ventana_etiquetar_imagenes()
        

    elif evento == "-PRINCIPAL-MEME-":
        ventana_actual.close()
        v.crear_ventana_seleccionar_template()
    
    elif evento == "-PRINCIPAL-COLLAGE-":
        ruta_completa= os.path.join (DIR_PROYECTO,'data', "informacion_imagenes.csv")
        if not f.existe_archivo(ruta_completa) :
            encabezado = ['ruta', 'texto descriptivo', 'resolucion', 'tamano', 'tipo', 'lista de tags', 'perfil actualizo', 'ultima actualizacion']
            f.crear_archivo_csv(encabezado,ruta_completa)
            
        ventana_actual.close()
        v.crear_ventana_diseño_collage()

    elif evento == "-PRINCIPAL-SALIR-":
        ventana_actual.close()
        inicio.generar_pantalla_inicio()
        
        


import PySimpleGUI as sg
import unlpimage.funcionalidad.ventanas as ventanas

def procesar_eventos(ventana_actual, evento, usuario_imagen):
    """
    Esta función maneja los eventos de la ventana para seleccionar un diseño de collage
    """
    if evento == "-DISEÑO-VOLVER-":
        ventanas.crear_ventana_principal(usuario_imagen)
        ventana_actual.close()
    elif evento.startswith("-DISEÑO-AVANZAR-"):
        num_diseno = int(evento.split("-")[-1])
        if num_diseno == 1:
            texto = "1"
            ventana_actual.close()
            ventanas.generar_collage(texto)
            
        elif num_diseno == 2:
            texto = "2"
            ventana_actual.close()
            ventanas.generar_collage(texto)
            
        elif num_diseno == 3:
            texto = "3"
            ventana_actual.close()
            ventanas.generar_collage(texto)
            
        elif num_diseno == 4:
            texto = "4"
            ventana_actual.close()
            ventanas.generar_collage(texto)

import PySimpleGUI as sg
import unlpimage.funcionalidad.funciones_agregar_perfil as funciones_ap
import unlpimage.funcionalidad.funciones_menu_principal as funciones_mp
from unlpimage.funcionalidad.funciones_agregar_perfil import imagen_actual
import unlpimage.funcionalidad.layout_inicio as layout_inicio




def procesar_eventos ( ventana_actual , eventos, valores, imagen_actual , lista  ):

    """Esta funcion los eventos de la ventana Agregar Perfil"""
    
    #verifico que los datos sean correctos
    correctos = funciones_ap.controlador_datos ( eventos, valores, ventana_actual )

   #nombro las varibales
    valor_otro = valores['-AGREGAR-OTRO-']
    texto_otro = valores['-AGREGAR-TEXTO-OTRO-']

    if valor_otro == True:
        if texto_otro == 'Especifique el genero':
            print ( 'entre')
            correctos = False
        else:
            valores['-AGREGAR-COMBO-'] = texto_otro
    else:
        if valores['-AGREGAR-COMBO-'] == '{---Elija una opcion---}':
            correctos = False

    #si se selecciona un avatar, actualizo el que aparece en pantalla
    if eventos == '-AGREGAR-AVATAR-':
        imagen_seleccionada = ventana_actual['-AGREGAR-IMAGEN-']
        nueva_imagen = funciones_ap.crear_ventana_archivos(imagen_seleccionada, None)
        if nueva_imagen != None:
            imagen_actual = nueva_imagen.split("/")[-1]

    # guardo los datos si son correctos
    elif eventos == "-AGREGAR-GUARDAR-"  and correctos:
        #agrego un usuario al archivo de usuarios
        funciones_ap.cargo_un_usuario ( valores , imagen_actual)
        sg.popup ( 'El perfil se generó correctamente.')
        ventana_actual.close()
        lista[1] = funciones_ap.informacion_json()
        layout_inicio.layouts(lista[0], lista[1])
        #agrego al csv de logs la creacion
        funciones_ap.verifico_archivo_logs()
        operacion = "creacion_perfil"
        alias = valores['-AGREGAR-ALIAS-']
        funciones_mp.registro_carga_logs(alias, operacion)


    # si los datos no son correctos, realizo un popup notificandolo
    elif eventos == "-AGREGAR-GUARDAR-" and not correctos:
        sg.popup ( 'Hay campos que contienen datos no validos.')

    elif eventos == "-AGREGAR-VOLVER-":
        ventana_actual.close()
        lista[1] = funciones_ap.informacion_json()
        layout_inicio.layouts(lista[0], lista[1])

    return lista[1], imagen_actual



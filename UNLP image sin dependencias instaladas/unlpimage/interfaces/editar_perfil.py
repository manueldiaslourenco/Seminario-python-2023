import PySimpleGUI as sg
import unlpimage.funcionalidad.ventanas as ventanas
import unlpimage.funcionalidad.funciones_menu_principal as f
import unlpimage.funcionalidad.funciones_agregar_perfil as fa


def procesar_eventos(ventana_actual, evento,valores, usuario, imagen_actual ):

    if evento == "-EDITAR-VOLVER-":
        ventanas.crear_ventana_principal(imagen_actual)
        ventana_actual.close()

    elif evento == '-EDITAR-AVATAR-':
        #abro la carpeta de archivos para que el usuario elija una nueva imagen
        nueva_imagen = fa.crear_ventana_archivos(ventana_actual['-EDITAR-IMAGEN-'], nueva_imagen= None)
        
        #si eligio una nueva imahen
        if ( nueva_imagen != None ):
            nueva_imagen= nueva_imagen.split("/")[-1]
            #actualizo la imagen actual
            nueva_imagen= nueva_imagen.split("/")[-1]
            imagen_actual = nueva_imagen

    elif evento == "-EDITAR-GUARDAR-" :
        #verifico que los datos sean correctos
        correctos = fa.controlador_datos( evento, valores, ventana_actual )
        if correctos :
            #los guardo y cierro la ventana
            if valores["-EDITAR-OTRO-"] == True:
                valores['-EDITAR-COMBO-'] = valores['-EDITAR-TEXTO-OTRO-']
            f.actualizar_usuario ( usuario, valores , imagen_actual )
            sg.popup('Se actualizaron con exito los datos.')
            #agrego al csv de logs la modificacion
            operacion = "mod_perfil"
            alias = valores['-EDITAR-ALIAS-']
            f.registro_carga_logs(alias, operacion)
        else:
            #le informo al usuario
            sg.popup ( 'Hay campos que se actualizaron con datos no validos.')


    return imagen_actual
    
    
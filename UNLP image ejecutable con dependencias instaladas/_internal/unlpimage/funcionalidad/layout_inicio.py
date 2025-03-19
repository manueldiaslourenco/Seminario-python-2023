import PySimpleGUI as sg
import os


def layouts(ruta_imagenes, usuarios ):
    # Definimos los tamaños de los botones

    max_botones_por_fila = 4

    # Creamos la lista de botones de usuario y botones adicionales
    botones_usuarios = []
    botones_adicionales = []
    alias = []

    # Si no hay usuarios, solo mostramos el botón de agregar perfil
    if not usuarios:
        layout = [[sg.Text('UNLPImage', font=('Helvetica', 20), pad=((0, 0), (20, 40)),background_color="#000000")],
                  [sg.Text('Bienvenido, presione el siguiente botón para crear su usuario:', font=('Helvetica', 15), pad=((120, 0), (20, 50)),background_color="#000000")],
                  [sg.Column([[sg.Button('Agregar perfil', size=(12,5), key='-INICIO-AGREGAR-PERFIL-')]], 
                  pad=(20, 0), justification='center',background_color="#000000")]]
    else:
        # Mostramos los botones de usuario
        for i, usuario in enumerate(usuarios):
            if i < max_botones_por_fila:
                nombre_imagen = usuario["Imagen"]
                ruta_imagen = os.path.join(ruta_imagenes, nombre_imagen)
                #print(ruta_imagen)
                botones_usuarios.append(sg.Button(image_source= ruta_imagen, image_size=(128,128), size=(12,5), key= '-INICIO-' + usuario["Alias"] + '-',tooltip=usuario["Alias"] ))
                alias.append(usuario["Alias"])

            else:
                break
    

        # Si hay menos de 4 usuarios, mostramos también el botón de agregar perfil
        if len(usuarios) <= max_botones_por_fila:
            botones_adicionales.append(sg.Button('Agregar perfil', size=(10,2), key='-INICIO-AGREGAR-PERFIL-'))
        else:
            # Si hay más de 4 usuarios, agregamos un botón para mostrar todos los usuarios
            botones_adicionales.append(sg.Button('Ver todos los usuarios', size=(10,2), key='-INICIO-MOSTRAR-PERFILES-'))
            botones_adicionales.append(sg.Button('Agregar perfil', size=(10,2), key='-INICIO-AGREGAR-PERFIL-'))
        # Agregamos los botones de usuario y los botones adicionales a la lista de botones

    # Creamos el layout con los botones
        layout = [
            [sg.Text('UNLPImage', font=('Helvetica', 20), pad=((20, 0), (20, 50)),background_color="#000000")],
            [sg.Text('Seleccione su usuario:', font=('Helvetica', 15), pad=(285,25),background_color="#000000")],
            [sg.Column([botones_usuarios], expand_y=True, vertical_scroll_only=True, justification='center', background_color="#000000")],
            [sg.Column([botones_adicionales], background_color="#000000",justification='center', pad=((0, 0), (0, 220)))]
    ]

    # Creamos la ventana
    return sg.Window('UNLPImage', layout, finalize= True, size=(800, 600), resizable=True, background_color="#000000")
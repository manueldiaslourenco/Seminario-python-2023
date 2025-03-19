import PySimpleGUI as sg
import os
import json
import unlpimage.funcionalidad.funciones_menu_principal as funciones_mp
from unlpimage.funcionalidad.paths import DIR_PROYECTO
import unlpimage.funcionalidad.paths as p

imagen_actual = None
veces = 0
def crear_ventana_agregar_perfil():
    """Esta funcion retorna la ventana del Agregar Perfil"""

    #columna de datos del usuario
    culumna1 = sg.Column ( layout= [  
                [sg.Text('Ingrese Alias', key= '-AGREGAR-TEXTO_ALIAS-',background_color='#000000')]   ,  
                [sg.Input(key = '-AGREGAR-ALIAS-')] , 
                [sg.Text('Ingrese nombre:', key= '-AGREGAR-TEXTO_NOMBRE-',background_color='#000000')] , 
                [sg.Input( key = '-AGREGAR-NOMBRE-')] , 
                [sg.Text('Ingrese edad:', key= '-AGREGAR-TEXTO_EDAD-', background_color='#000000')] ,
                [sg.Input ( key= '-AGREGAR-EDAD-')] ,
                [sg.Text('Genero autopercibido', background_color='#000000')] ,
                [sg.Combo( ['Masculino','Femenino' ] , key= '-AGREGAR-COMBO-', readonly = True, size= (29,6), default_value=['---Elija una opcion---'] )] ,
                [sg.Checkbox ( 'Otro', key = '-AGREGAR-OTRO-' ) ]  ,
                [sg.Input( key= '-AGREGAR-TEXTO-OTRO-', default_text= 'Especifique el genero'  )] ,
                [sg.Button( 'Guardar' , key= '-AGREGAR-GUARDAR-' )] 
                ] , 
                background_color='#000000'
                )
    

    #columna del avatar

    directorio_imagen = os.path.join ( DIR_PROYECTO, 'imagenes_proyecto','imagenes_perfiles' )

    imagen = os.path.join ( directorio_imagen, '0.png' )

    columna2 = sg.Column (  

                layout= [                
                
                [sg.Image(filename=imagen, key='-AGREGAR-IMAGEN-' , subsample=1  , size= ( 150,150) )  ] ,
 
                [sg.Button ( 'Seleccionar avatar', key= '-AGREGAR-AVATAR-' , ) ] 
                             
                ], background_color='#000000'
                 
                )       
    



    #columna del volver
    
    columna3 = sg.Column ( layout= [ [ sg.Button( 'Volver', key= '-AGREGAR-VOLVER-') ] ] , expand_x=True, element_justification='right' , background_color='#000000') 
    
    layout = [ [columna3] , [ culumna1, columna2 ]  ]

    ventana= sg.Window('Nuevo Perfil',layout,finalize=True, resizable=True, background_color='#000000', size= ( 800,600 ))

    return ventana


def crear_ventana_archivos (agregar_imagen, nueva_imagen ):
    """Esta funcion crea una ventana para elegir una imagen mediante el browse"""

    layout = [[sg.Text('Seleccione un archivo:')],
          [sg.Input(), sg.FileBrowse()],
          [sg.Button('OK')]]
    nueva_ventana = sg.Window( 'Seleccionar archivo', layout= layout , finalize=True )
    
    while True:

        evento, valores = nueva_ventana.read()
        if evento == sg.WIN_CLOSED:
            break
        elif evento == 'OK':
            directorio_imagen = os.path.join (DIR_PROYECTO, 'imagenes_proyecto','imagenes_perfiles' )
            nueva_imagen = os.path.join ( directorio_imagen, valores['Browse'] )
            if len(valores['Browse']) >1:
                agregar_imagen.update(source= nueva_imagen )    
            else:
                nueva_imagen += '0.png'
                agregar_imagen.update(source= nueva_imagen )
            break

    nueva_ventana.close()
    return nueva_imagen


def controlador_datos ( evento,valores, ventana_actual ):
    """Esta funcion analiza si los datos ingresados son correctos"""
    
    correctos= True
    usuarios= informacion_json()
    evento = evento.split('-')[1]

    if evento == 'AGREGAR':
        edad= valores['-AGREGAR-EDAD-']
        nombre= valores['-AGREGAR-NOMBRE-']
        alias= valores['-AGREGAR-ALIAS-']
        if any(filter(lambda x: x['Alias'] == alias, usuarios)):
            ventana_actual['-AGREGAR-TEXTO_ALIAS-'].update('*El alias ingresado ya existe')
            correctos = False
    elif evento == 'EDITAR':
        edad= valores['-EDITAR-EDAD-']
        nombre= valores['-EDITAR-NOMBRE-']

    if not nombre.isalpha():
        ventana_actual['-AGREGAR-TEXTO_NOMBRE-'].update( '*Ingrese su nombre' )
        correctos = False
        
    if (not (edad.isdigit())) or (int(edad) <= 0) or (int(edad) >= 100):
        ventana_actual['-AGREGAR-TEXTO_EDAD-'].update ( '*Ingrese su edad' ) 
        correctos = False

    return correctos





def existe_archivo ( ruta ):
    """Si el archivo existe retorno True, en caso contrario retorno False"""
    if os.path.isfile(ruta):
        return True
    else:
        return False




def cargo_un_usuario (valores, imagen ):
    """Esta funcion agrega un usuario al archivo json"""

    ruta = os.path.join ( DIR_PROYECTO,'data', "datos_usuarios.json" )
    
    datos = { 
              'Alias'  : valores['-AGREGAR-ALIAS-' ] ,
              'Nombre' : valores['-AGREGAR-NOMBRE-'] ,
              'Edad'   : valores['-AGREGAR-EDAD-'  ] , 
              'Genero' : valores['-AGREGAR-COMBO-' ] ,
              'Imagen' : imagen
            }
    try:
        if existe_archivo (ruta):
            with open(ruta, 'r') as f:
                usuarios = json.load(f)
            if not datos['Alias'] in usuarios:
                usuarios.append(datos)
        else:
            usuarios = [datos]
    except PermissionError:
        sg.popup('No tiene permisos de escritura sobre el archivo. La aplicación finalizará')
    except FileNotFoundError:
        sg.popup('No se ha encontrado el archivo. La apliación finalizará.')
    except:
        sg.popup('Ups! Ha ocurrido un error. La aplicación finalizará.')
        
    funciones_mp.escribir_json(ruta, usuarios)

def informacion_json ():

    ruta_json = os.path.join(DIR_PROYECTO, 'data', 'datos_usuarios.json')

    return funciones_mp.leer_json(ruta_json)

def verifico_archivo_logs():
    ruta_logs= os.path.join(DIR_PROYECTO, 'data', 'logs_sistema.csv')
    if not funciones_mp.existe_archivo(ruta_logs):
        encabezado = ['Alias','Operacion','Fecha y hora', 'Valores', 'Texto']
        funciones_mp.crear_archivo_csv(encabezado,ruta_logs)

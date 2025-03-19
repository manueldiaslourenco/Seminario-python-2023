import PySimpleGUI as sg
import os
import io
from PIL import Image
import unlpimage.funcionalidad.funciones_menu_principal as f
from unlpimage.funcionalidad.paths import DIR_PROYECTO
import unlpimage.funcionalidad.paths as paths
import csv

def crear_ventana_principal(usuario):

    carpeta_menu = os.path.join(DIR_PROYECTO, "imagenes_proyecto", "imagenes_menu")
    rueda_configuracion = "Ruedita_de_configuracion.png"
    simbolo_ayuda = "Simbolo_ayuda.png"
    carpeta_perfiles = os.path.join(DIR_PROYECTO, "imagenes_proyecto", "imagenes_perfiles")
    ruta_perfil_imagen = os.path.join(carpeta_perfiles, usuario)
    imagen_perfil = Image.open(ruta_perfil_imagen)
    imagen_perfil.thumbnail((100,100))
    bio = io.BytesIO()
    imagen_perfil.save(bio, format="PNG")

    layout = [[sg.Button(image_source= bio.getvalue() , key="-PRINCIPAL-NICK-", tooltip= "Seleccione para editar datos del usuario actual.",size=(10, 2)),
               sg.Text(" ", expand_x=True, background_color="#000000"),
               sg.Button(image_source= os.path.join(carpeta_menu,rueda_configuracion), image_size=(64,64),border_width=0 ,key="-PRINCIPAL-CONFIG-",
                         tooltip= "Seleccione para entrar a la configuracion de la aplicacion.")],
                         [sg.Text("   ", expand_x=True, background_color="#000000"), sg.Button(image_source= os.path.join(carpeta_menu,simbolo_ayuda), image_size=(64,64),border_width=0 ,key = "-PRINCIPAL-AYUDA-")],
              
              [sg.Column([
                  [sg.Button("Etiquetar imagenes",key="-PRINCIPAL-ETIQUETAR-", tooltip= "Seleccione para poder agregar tags y descripciones a las imagenes.",size=(16, 4))],
                  [sg.Button("Generar Meme", key="-PRINCIPAL-MEME-", tooltip= "Seleccione para poder generar Memes con imagenes escogidas y luego almacenarlas.",size=(16, 4))],
                  [sg.Button("Generar Collage",key="-PRINCIPAL-COLLAGE-", tooltip= "Seleccione para generar Collage con imagenes escogidas y luego almacenarlas.",size=(16, 4))],
              [sg.Button("Salir", key="-PRINCIPAL-SALIR-",size=(16, 4))]],justification="center",background_color="#000000")]]
    
    return sg.Window("Menu principal", layout, finalize=True, size=(800, 600), resizable=True, background_color="#000000")

def crear_ventana_configuracion(texto_1, texto_2, texto_3):
    layout = [[sg.Text("   ", expand_x=True, background_color="#000000"), sg.Button("Volver", key="-CONFIGURACION-VOLVER-")],
             [sg.Column([
                [sg.Text("Selecciona una carpeta para el repositorio de imagenes:",background_color="#000000")], [sg.Input(default_text=texto_1), sg.FolderBrowse()], 
                [sg.Text("Selecciona una carpeta para almacenar tus collage generados:",background_color="#000000")],[sg.Input(default_text=texto_2),sg.FolderBrowse()],
                [sg.Text("Selecciona una carpeta para almacenar tus memes generados:",background_color="#000000")],[sg.Input(default_text=texto_3),sg.FolderBrowse()]]
                ,justification="center",background_color="#000000")],
               [sg.Text("   ", expand_x=True, background_color="#000000"),sg.Button("Guardar",key="-CONFIGURACION-GUARDAR-")]
                
                ]


    return sg.Window("Configuracion", layout, finalize=True, size=(800, 600), resizable=True, background_color="#000000")

def crear_ventana_ayuda():
    layout= [[sg.Column([[sg.Text("Para obtener información sobre la funcionalidad de cada botón, basta con colocar el cursor sobre el botón que se desea seleccionar. De esta manera, se mostrará una breve descripción o ayuda que proporciona detalles sobre el propósito o función del botón.",
                     size=(60, 5),justification="center",background_color="#000000")],
            [sg.Text("",expand_x=True,background_color="#000000"),sg.Button("Ok", key="-AYUDA-OK-", size=(10, 2)),sg.Text("",expand_x=True,background_color="#000000")]]
            ,justification="center", background_color="#000000")]]
    return sg.Window("Ayuda", layout, finalize=True, size=(800, 600), resizable=True,  background_color="#000000")

def crear_ventana_editar_perfil(usuario):

    columna1 = sg.Column (layout= [ [sg.Text("Alias",background_color="#000000")] , 
                          
                [sg.Input(key = "-EDITAR-ALIAS-", readonly=True, default_text= usuario['Alias'])] , 

                [sg.Text("Nombre", key="-EDITAR-TEXTO-NOMBRE-",background_color="#000000")] , 

                [sg.Input( key = "-EDITAR-NOMBRE-", default_text= usuario['Nombre'])]  ,
                
                [sg.Text("Edad", key="-EDITAR-TEXTO-EDAD-",background_color="#000000")] , [sg.Input ( key= "-EDITAR-EDAD-", default_text= usuario['Edad'])],

                [sg.Text("Genero autopercibido", background_color="#000000")] , 
                
                [sg.Combo( ["Masculino","Femenino" ] , key= "-EDITAR-COMBO-", size= (44,6), default_value=usuario['Genero']) ] ,

                [sg.Checkbox ( "Otro", key = "-EDITAR-OTRO-" ) ]  ,

                [sg.Input( key= '-EDITAR-TEXTO-OTRO-', default_text= 'Especifique el genero'  )] ,

                [sg.Button( "Guardar", key = "-EDITAR-GUARDAR-" )],

                [sg.Button("Volver", key="-EDITAR-VOLVER-")]

                ], background_color='#000000'

              )
    
    directorio_imagen = os.path.join ( DIR_PROYECTO, 'imagenes_proyecto','imagenes_perfiles' )
    imagen = os.path.join ( directorio_imagen,usuario['Imagen'] )
    columna2 = sg.Column (  

                layout= [                

                [sg.Image(filename=imagen, key='-EDITAR-IMAGEN-' , subsample=1  , size= ( 150,150) )  ] ,
 
                [sg.Button ( 'Seleccionar avatar', key= '-EDITAR-AVATAR-' , ) ] 
                             
                ], background_color='#000000'
                 
                )
    layout = [  [columna1, columna2]  ]
    
    return sg.Window("Editar Perfil", layout, finalize=True, size=(800, 600), resizable=True, background_color="#000000")
    
def crear_ventana_etiquetar_imagenes():
    try:
        carpeta_imagenes = paths.convertir_guardado_para_usar(f.informacion_archivo_json()[0], DIR_PROYECTO)
        imagenes = [elemento for elemento in os.listdir(carpeta_imagenes) if elemento.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        if len(imagenes)>=1:
            ok = True
        else:
            ok= False
    except FileNotFoundError:
        sg.popup("El sistema no pudo encontrar la ruta especificada, pruebe modificando la ruta del repositorio de imagenes en la configuracion de la aplicacion.")
        imagenes = []
        ok= False

    layout = [[sg.Text("Imágenes en la carpeta seleccionada:", background_color="#000000", expand_x=True),
               sg.Button("Volver", key= "-ETIQUETAR-VOLVER-")],
             [sg.Listbox(values= imagenes, size=(30, 10), key="-ETIQUETAR-SELECCION-IMAGEN-",enable_events=ok, tooltip="Listado de imagenes de la carpeta seleccionada.")],
             [sg.Column([
                        [sg.Text("Tag", background_color="#000000")],
                        [sg.Input(key="-ETIQUETAR-TAG-", disabled=True)],
                        [sg.Button("Agregar", key="-ETIQUETAR-AGREGAR-TAG-", disabled=True, tooltip="Presione para agregar una etiqueta."),
                        sg.Button("Eliminar", key="-ETIQUETAR-ELIMINAR-TAG-", disabled=True, tooltip="Presione para eliminar una etiqueta.")],
                        [sg.Text("Texto descriptivo", background_color="#000000")],
                        [sg.Input(key="-ETIQUETAR-DESCRIPCION-", disabled=True)],
                        [sg.Button("Agregar", key="-ETIQUETAR-AGREGAR-DESCRIPCION-", disabled=True, tooltip="Presione para agregar descripcion."),
                         sg.Button("Eliminar", key="-ETIQUETAR-ELIMINAR-DESCRIPCION-",disabled=True, tooltip="Presione para eliminar la descripcion.")]
                        ],size= (250,200), background_color="#000000")
             ,sg.Text(" ",expand_x=True, background_color="#000000"),
             sg.Column([[sg.Image(key="-IMAGEN-SELECCIONADA-", visible=False)],
                         [sg.Text("", key="-ETIQUETAR-DATOS-IMAGENES-", visible=False, background_color="#000000")]]
                         ,justification="right",size= (250,200), background_color="#000000")
             ], 
                        [sg.Text(" ",expand_x=True, background_color="#000000") ,sg.Text("", key="-ETIQUETAR-MOSTRAR-TAG-", background_color="#000000")],
                        [sg.Text(" ",expand_x=True, background_color="#000000"),sg.Text("", key="-ETIQUETAR-MOSTRAR-DESCRIPCION-",background_color="#000000")], 
                        [sg.Text(" ",expand_y=True, background_color="#000000")],
                        [sg.Text(" ",expand_x=True, background_color="#000000"), sg.Button("Guardar", key="-ETIQUETAR-GUARDAR-", disabled=True, tooltip="Presione para guardar cambios")]
             ]
    
    return sg.Window("Etiquetar imagenes", layout, finalize=True, size=(800, 600), resizable=True, background_color="#000000")

def crear_ventana_seleccionar_template():

    carpeta_imagenes = os.path.join(DIR_PROYECTO,'imagenes_proyecto', 'creacion_memes')
    templates= [elemento for elemento in os.listdir(carpeta_imagenes) if elemento.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    if len(templates)>=1:
        ok = True
    else:
        ok= False
        templates = []
    
    layout = [[sg.Text(" ", expand_x=True, background_color="#000000"), sg.Button("Volver", key= "-TEMPLATE-VOLVER-")],
              [sg.Text(" ", background_color="#000000")], #Dejo una linea.
              [sg.Text("seleccionar template: ", background_color="#000000"),sg.Text(" ", expand_x=True, background_color="#000000"),sg.Text("Previsualización", background_color= "#000000")],
              [sg.Listbox(values= templates, size=(30, 10), key="-TEMPLATE-SELECCION-IMAGEN-",enable_events=ok, tooltip="Listado de templates."),
               sg.Text(" ", expand_x=True, background_color= "#000000"),sg.Image(key="-TEMPLATE-SELECCIONADO-", visible=False)],
              [sg.Text(" ",expand_y=True, background_color="#000000")],
              [sg.Text(" ",expand_x=True, background_color="#000000"), sg.Button("Generar", key= "-TEMPLATE-GENERAR-",disabled=True,tooltip="Genera el template seleccionado para la finalizacion del meme.")],
              ]

    return sg.Window("Seleccionar Template", layout, finalize=True, size=(800,600), resizable=True, background_color="#000000")

def crear_ventana_generar_meme(cant):

    carpeta_fuentes = os.path.join(DIR_PROYECTO,'fuentes')
    opciones_fuente = [archivo[:-4] for archivo in os.listdir(carpeta_fuentes) if archivo.lower().endswith('.ttf')]


    layout = [[sg.Text(" ", expand_x=True, background_color="#000000"), sg.Button("Volver", key= "-MEME-VOLVER-")],
              [sg.Text("Seleccionar Fuente: ",background_color="#000000")],
              [sg.Combo(opciones_fuente, default_value=opciones_fuente[0], key='-MEME-FUENTE-',tooltip="Escoja la fuente que prefiera para la creacion del meme.")],
              [sg.Column([
              #Texto1
              [sg.Text("texto1: ", background_color="#000000")],
              [sg.Input(default_text="" ,key="-MEME-TEXTO1-",tooltip= "Ingrese el primer texto que se colocara en el meme.")],
            
              #Texto2
              [sg.Text("texto2: ", background_color="#000000",visible=f.Cumple(cant,2))],
              [sg.Input(default_text="" ,key="-MEME-TEXTO2-",tooltip= "Ingrese el segundo texto que se colocara en el meme.",visible=f.Cumple(cant,2))],

              #Texto3
              [sg.Text("texto3: ", background_color="#000000",visible=f.Cumple(cant,3))],
              [sg.Input(default_text="" ,key="-MEME-TEXTO3-",tooltip= "Ingrese el tercer texto que se colocara en el meme.",visible=f.Cumple(cant,3))],
              
              #Texto4
              [sg.Text("texto4: ", background_color="#000000",visible=f.Cumple(cant,4))],
              [sg.Input(default_text="" ,key="-MEME-TEXTO4-",tooltip= "Ingrese el cuarto texto que se colocara en el meme.", visible=f.Cumple(cant,4))],
              ],background_color="#000000"), sg.Text(" ",expand_x=True, background_color="#000000"),
              
              sg.Column([[sg.Image(key="-MEME-SELECCIONADO-")]],background_color="#000000")],
                
              [sg.Text(" ",expand_x=True, background_color="#000000"),sg.Text("Nombre del meme generado: ",background_color="#000000")],
              [sg.Text(" ",expand_x=True, background_color="#000000"), sg.Input(default_text="meme-generado.jpg", key="-MEME-NOMBRE-GUARDAR-",disabled=True,tooltip="Ingrese el nombre con el que el archivo se guardara.")],
              [sg.Button("Actualizar", key= "-MEME-ACTUALIZAR-",tooltip="Al oprimir este boton la imagen se actualizara con los textos ingresados en pantalla."),sg.Text(" ",expand_x=True, background_color="#000000"), 
               sg.Button("Guardar", key= "-MEME-GUARDAR-",disabled=True,tooltip="Presione para guardar el meme generado como un archivo.")]]

    return sg.Window("Generar Meme", layout, finalize=True, size=(800,600), resizable=True, background_color="#000000")


def crear_ventana_diseño_collage():
    """
    Esta ventana crea el layout de la ventana para seleccionar el diseño de collage
    """
    carpeta_imagenes_templates = os.path.join(DIR_PROYECTO, "imagenes_proyecto", "imagenes_diseño_collage")
    ruta_imagen_1 = os.path.join(carpeta_imagenes_templates, "imagen_template_1.png")
    ruta_imagen_2 = os.path.join(carpeta_imagenes_templates, "imagen_template_2.png")
    ruta_imagen_3 = os.path.join(carpeta_imagenes_templates, "imagen_template_3.png")
    ruta_imagen_4 = os.path.join(carpeta_imagenes_templates, "imagen_template_4.png")

    layout = [
        [sg.Text("Seleccione un diseño para su collage:", font=('Helvetica', 15), background_color="#000000", expand_x=True),
               sg.Button("Volver", key= "-DISEÑO-VOLVER-")],
        [sg.Column([
            [sg.Button(image_source=ruta_imagen_1, image_size=(220, 260), border_width=0, key="-DISEÑO-AVANZAR-1")],
            [sg.Button(image_source=ruta_imagen_3, image_size=(220, 260), border_width=0, key="-DISEÑO-AVANZAR-2")]
        ], element_justification='center', background_color="#000000"),
        sg.Column([
            [sg.Button(image_source=ruta_imagen_2, image_size=(220, 260), border_width=0, key="-DISEÑO-AVANZAR-3")],
            [sg.Button(image_source=ruta_imagen_4, image_size=(220, 260), border_width=0, key="-DISEÑO-AVANZAR-4")],
        ], element_justification='center', background_color="#000000")]  
    ]

    return sg.Window("Elegir formato Collage", layout, finalize=True, size=(800, 600), resizable=True, background_color="#000000")


def generar_collage(numero_diseño):
    """
        Esta función genera el collage con las imagenes y titulo que hayan seleccionado y retorna el collage actualizado
    """
    IMAGE_SIZE = (500, 500)
    collage = Image.new("RGB", IMAGE_SIZE)
    collage.thumbnail(IMAGE_SIZE)
    collage_path = "temp_collage.png"
    collage.save(collage_path, format="PNG")

    # Leer la configuración del archivo JSON

    ruta_imagenes_etiquetar = paths.convertir_guardado_para_usar(f.informacion_archivo_json()[0],DIR_PROYECTO)
    ruta_csv = os.path.join(DIR_PROYECTO, 'data', 'informacion_imagenes.csv')


    # Obtener descripciones desde el archivo csv de las imágenes etiquetadas que se encuentren en la carpeta configurada
    descripciones_imagenes = f.obtener_descripciones_imagenes(ruta_csv, ruta_imagenes_etiquetar)
    fuente = os.path.join(DIR_PROYECTO, 'fuentes', 'arial_narrow_7.ttf' )

    layout_izquierdo = [
        [sg.Text("Generar collage " + str(numero_diseño), font=(fuente, 12), key="-COLLAGE-DISEÑO-")],
        [
            sg.Text("Imagen 1:", font=(fuente, 12)),
            sg.Combo(descripciones_imagenes, key="-COLLAGE-ACTUALIZAR-1", size=(20, 6), default_value="", enable_events=True)
        ],
        [
            sg.Text("Imagen 2:", font=(fuente, 12)),
            sg.Combo(descripciones_imagenes, key="-COLLAGE-ACTUALIZAR-2", size=(20, 6), default_value="", enable_events=True)
        ],
        [
            sg.Text("Imagen 3:", font=(fuente, 12)),
            sg.Combo(descripciones_imagenes, key="-COLLAGE-ACTUALIZAR-3", size=(20, 6), default_value="", enable_events=True)
        ],
        [sg.Text("Agregar título:", font=(fuente, 12))],
        [sg.Input(key='-COLLAGE-TITULO-', size=(20, 1))],
        [sg.Button("Actualizar", key='-COLLAGE-ACTUALIZAR-TITULO', size=(15, 1))]
    ]

    layout_derecho = [
        [sg.Button("Volver", key="-COLLAGE-VOLVER-")],
        [sg.Image(key="-IMAGEN-COLLAGE-", filename=collage_path, size=IMAGE_SIZE)],
        [sg.Button("Guardar", key='-COLLAGE-GUARDAR-', size=(15, 1),disabled=True)]
    ]

    layout = [
        [
            sg.Column(layout_izquierdo, expand_x=True, expand_y=True, pad=(0, 0)),
            sg.Column(layout_derecho, expand_x=True, expand_y=True, pad=(0, 0))
        ]
    ]

    return sg.Window(f"Generar Collage - Diseño {numero_diseño}", layout, finalize=True, size=(800, 600),
                     resizable=True, background_color="#000000")
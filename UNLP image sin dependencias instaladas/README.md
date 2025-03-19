UNLPImage
Este es un proyecto que tiene como objetivo desarrollar una aplicación de escritorio denominada UNLPImage. Esta aplicación permitirá:

- Crear un collage con imágenes disponibles en nuestra computadora.
- Generar un meme a través de la combinación de imágenes con texto y emojis.
- Clasificar imágenes.

Requisitos previos
Antes de comenzar a utilizar UNLPIMAGE, asegúrate de tener los siguientes requisitos previos:

- Python 3.11 instalado en tu sistema.
- Pip instalado para gestionar las dependencias de Python.

Instalación
Sigue estos pasos para configurar el entorno de desarrollo de UNLPIMAGE:

- Clona el repositorio de UNLPIMAGE en tu máquina local.
    git clone git@gitlab.catedras.linti.unlp.edu.ar:python2023/code/grupo34.git
- Navega al directorio del proyecto.
    cd grupo34
- Crea un entorno virtual (opcional, pero se recomienda).
    python -m venv venv
- Activa el entorno virtual:
    En Windows: venv\Scripts\activate
    En Linux o macOS: source venv/bin/activate
Instala las dependencias utilizando el archivo requirements.txt.
    pip install -r requirements.txt

Para iniciar la aplicación, debes ejecutar el archivo unlpimage.py que se encuentra en el repositorio.
Al entrar en la aplicación debes crear tu perfil de usuario o seleccionar uno existente. 
Antes de comenzar a etiquetar imágenes, debes configurar las carpetas que contienen las imágenes a etiquetar. En la sección de configuración, podrás seleccionar la carpeta de origen de las imágenes y la carpeta de destino para los collages generados y los memes. Si no se selecciona ninguna carpeta, se utilizarán las carpetas por defecto.

Una vez configuradas las carpetas, podrás etiquetar las imágenes. Para cada imagen, podrás proporcionar una descripción y agregar palabras clave (tags). La descripción es importante para luego usarlas en la generación de collages.

Con UNLPImage, puedes seleccionar fotos o imágenes disponibles en tu computadora y crear un collage. La aplicación te brinda algunos diseños para organizar y combinar las imágenes, y también la posibilidad de agregar un título.

Además de los collages, UNLPImage te permite generar memes. Puedes seleccionar algunos templates predefinidos, agregar texto y emojis para crear memes personalizados.

Streamlit

Descripción de la aplicación:
Esta aplicación de Streamlit proporciona estadísticas sobre sobre la app de unlpimage. La aplicación mostrará diferentes gráficos y visualizaciones basadas en los datos de la aplicación original.

Sigue estos pasos para ejecutar la aplicación de Streamlit:

- Clona el repositorio de la aplicación desde Gitlab o copia los archivos en tu directorio local.

- Abre una ventana de terminal o línea de comandos.

- Navega hasta el directorio raíz de la aplicación en la terminal usando el siguiente comando:

    cd ruta/al/directorio

    Reemplaza "ruta/al/directorio" con la ruta real del directorio en tu sistema donde se encuentren los archivos de la aplicación.

- Una vez que estes dentro del directorio "analisis_datos", ejecuta el siguiente comando:

    streamlit run inicio.py

Después de ejecutar el comando anterior, se abrirá una ventana del navegador con la aplicación de Streamlit. Si no se abre automáticamente, puedes acceder a ella visitando la siguiente URL en tu navegador:

http://localhost:8501

Notas adicionales

Si deseas detener la ejecución de la aplicación en la terminal, simplemente presiona Ctrl + C en la ventana de la terminal.

Contribuidores

- Santiago Fierro
- Manuel Dias Lourenco
- Ramiro Milillo


Licencia
Este proyecto está licenciado bajo la licencia GNU GPL v3. Consulta el archivo LICENSE.md para más información.
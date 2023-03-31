import string

jupyter_info = """ JupyterLab is a web-based interactive development environment for Jupyter notebooks, 
code, and data. JupyterLab is flexible: configure and arrange the user 
interface to support a wide range of workflows in data science, scientific computing, and machine learning.
JupyterLab is extensible and
modular: write plugins that add new components and integrate with existing
ones.
"""

lista= jupyter_info.split()

letra=input('Ingrese una letra: ')

filtro = []

if letra in string.ascii_letters:
    for elem in lista:
        if elem.lower().split()[0].startswith(letra):
            filtro.append(elem)
    print(f"existen {len(filtro)} palabras que inician con la letra {letra}")
    for elem in filtro:
        print(elem)
else:
    print('ERROR. No se ingreso una letra.')
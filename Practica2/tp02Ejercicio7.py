texto = """
 El salario promedio de un hombre en Argentina es de $60.000, mientras que
el de una mujer es de $45.000. Además, las mujeres tienen menos
posibilidades de acceder a puestos de liderazgo en las empresas.
 """

listaChar = [char for char in texto]

listaPalabras = texto.split()

mayus=0
min=0
car=0
cant= 0

for elem in listaChar:
    if elem.isalpha():
        if elem.isupper():
            mayus += 1
        else:
            min += 1
    else:
        car+=1

print(f"La cantidad de mayusculas en la frase son: {mayus}\nLa cantidad de minusculas son: {min}\nLa cantidad de caracteres no letras son: {car}\nLa cantidad de palabras que contiene la frase es: {len(listaPalabras)}")
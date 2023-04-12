
heterograma = lambda palabra: len(set(filter(str.isalpha, palabra.lower()))) == len(list(filter(str.isalpha, palabra.lower())))

frase = input("Ingrese una palabra/frase: ")

if heterograma(frase):
    print("La frase/palabra es un Heterograma")
else:
    print("La frase/palabra no es un heterograma")


Oracion = input("Para la frase: ")

palabra = input("Palabra: ")

Oracion = Oracion.split()

if(palabra.lower() in Oracion):
    print(f'Resultado: {Oracion.count(palabra.lower())}')
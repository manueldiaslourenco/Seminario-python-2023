def calcularPromedio(elem):
    """Calcula el promedio de cada estudiante. """
    return round (((elem[1] + elem[2]) / (len(elem)-1)), 2)

def calcularPromedioCurso(lista):
    """Calcula el promedio general del curso, necesita como parametro una lista con los promedios de cada estudiante."""
    return round((sum(lista)/len(lista)),2)

def estudianteMasPromedio(lista,prom):
    """Devuelve al estudiante con la nota promedio más alta. Recibo como parametro una lista de los alumnos con sus respectivas notas y una lista con promedios de cada estudiante."""
    indice = prom.index(max(prom))
    return lista[indice]
    
nombres = ''' 'Agustin', 'Alan', 'Andrés', 'Ariadna', 'Bautista', 'CAROLINA', 'CESAR',
'David','Diego', 'Dolores', 'DYLAN', 'ELIANA', 'Emanuel', 'Fabián', 'Facundo',
'Francsica', 'FEDERICO', 'Fernanda', 'GONZALO', 'Gregorio', 'Ignacio', 'Jonathan',
'Joaquina', 'Jorge','JOSE', 'Javier', 'Joaquín' , 'Julian', 'Julieta', 'Luciana',
'LAUTARO', 'Leonel', 'Luisa', 'Luis', 'Marcos', 'María', 'MATEO', 'Matias',
'Nicolás', 'Nancy', 'Noelia', 'Pablo', 'Priscila', 'Sabrina', 'Tomás', 'Ulises',
'Yanina' '''

notas_1 = [81, 60, 72, 24, 15, 91, 12, 70, 29, 42, 16, 3, 35, 67, 10, 57, 11, 69,
12, 77, 13, 86, 48, 65, 51, 41, 87, 43, 10, 87, 91, 15, 44,
85, 73, 37, 42, 95, 18, 7, 74, 60, 9, 65, 93, 63, 74]

notas_2 = [30, 95, 28, 84, 84, 43, 66, 51, 4, 11, 58, 10, 13, 34, 96, 71, 86, 37,
64, 13, 8, 87, 14, 14, 49, 27, 55, 69, 77, 59, 57, 40, 96, 24, 30, 73,
95, 19, 47, 15, 31, 39, 15, 74, 33, 57, 10]

nombres = nombres.replace(",", " ").replace("\n", " ").replace("'", " ")

lista = nombres.split()

notas_1 = notas_1[0:len(lista)]

notas_2 = notas_2 [0:len(lista)]

lista = list(zip(lista, notas_1, notas_2))

lista_promedios = list(map(lambda x: calcularPromedio(x), lista)) #Calculo el promedio de notas de cada estudiante.

curso_prom= calcularPromedioCurso(lista_promedios) #Calculo el promedio general del curso.

estudiante_minimo = min(lista, key=lambda x: (x[1], x[2])) 

print("El estudiante con la nota promedio más alta: ", estudianteMasPromedio(lista,lista_promedios)) #Identificar al estudiante con la nota promedio más alta

print("El estudiante con la nota mas baja es: ", estudiante_minimo) #Identificar al estudiante con la nota más baja.
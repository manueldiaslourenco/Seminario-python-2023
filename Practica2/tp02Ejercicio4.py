evaluar = """ título: Experiences in Developing a Distributed Agent-based
Modeling Toolkit with Python
resumen: Distributed agent-based modeling (ABM) on high-performance
computing resources provides the promise of capturing unprecedented details
of large-scale complex systems. However, the specialized knowledge required
for developing such ABMs creates barriers to wider adoption and utilization.
Here we present our experiences in developing an initial implementation of
Repast4Py, a Python-based distributed ABM toolkit. We build on our
experiences in developing ABM toolkits, including Repast for High
Performance Computing (Repast HPC), to identify the key elements of a useful
distributed ABM toolkit. We leverage the Numba, NumPy, and PyTorch packages
and the Python C-API to create a scalable modeling system that can exploit
the largest HPC resources and emerging computing architectures.
"""

texto= evaluar.split("título: ")[1].split("resumen: ")

titulo = texto[0].strip().replace('\n',' ')
titulo = titulo.split()

resumen = texto[1].strip().replace('\n',' ')
resumen = resumen.split()

Oraciones = {"fáciles de leer": 0, "aceptables para leer": 0, "dificil de leer": 0, "muy difícil de leer": 0 }

cant = 0

for elem in resumen:
    if(not '.' in elem):
        cant += 1
    else:
        if(cant<=12):
            Oraciones["fáciles de leer"] += 1
        elif(cant<=17):
            Oraciones["aceptables para leer"] += 1
        elif(cant<=25):
            Oraciones["dificil de leer"] += 1
        elif(cant>25):
            Oraciones["muy difícil de leer"] += 1
        cant= 0


for elem in titulo:
    cant+= 1        

if 10 >= cant:
    print("titulo: Ok")
else:
    print("titulo: No cumple.")

print(Oraciones)
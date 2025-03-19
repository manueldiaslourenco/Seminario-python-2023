import os.path

DIR_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def convertir_para_guardar(path, path_proyecto):
    path_relativo = os.path.relpath(path, start=path_proyecto)
    path_generico = path_relativo.replace(os.path.sep, "/")
    return path_generico

def convertir_guardado_para_usar(path, path_proyecto):
    path_del_sistema = path.replace("/", os.path.sep)
    path_absoluto = os.path.abspath(os.path.join(path_proyecto ,path_del_sistema))
    return path_absoluto
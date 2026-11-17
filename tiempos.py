import time
import copy
import logica.Gauss_Seidel 

def medir_tiempo(funcion, A, b, repeticiones):
    """
    Mide el tiempo promedio de ejecución de una función y devuelve el tiempo total, promedio y resultados.

    Args:
        funcion (callable): La función a medir.
        A (list of list of float): Matriz de coeficientes.
        b (list of float): Vector de términos independientes.
        repeticiones (int): Número de veces que se ejecutará la función para obtener un promedio.

    Returns:
        dict: Un diccionario con el tiempo total, promedio y resultados.
    """
    tiempos = []
    resultado = None
    for _ in range(repeticiones):
        A_copia = copy.deepcopy(A)
        b_copia = copy.deepcopy(b)
        inicio = time.perf_counter()
        resultado = funcion(A_copia, b_copia)
        tiempos.append(time.perf_counter() - inicio)
    total = sum(tiempos)
    tiempo_promedio = total / repeticiones
    return {"total": tiempos, "promedio": tiempo_promedio, "resultado": resultado}

def comparar_tiempos(A, b, metodo_directo, x0, tol, max_iter, k):
    """
    Compara los tiempos de ejecución de un método directo (eliminiación Gaussiana) y el método de Gauss-Seidel.

    Args:
        A (list of list of float): Matriz de coeficientes.
        b (list of float): Lado derecho de la igualdad del sistema.
        metodo_directo (callable): Eliminación Gaussiana.
        x0 (list of float): Valor inicial para el método de Gauss-Seidel.
        tol (float): Tolerancia para la convergencia del método de Gauss-Seidel.
        max_iter (int): Número máximo de iteraciones para el método de Gauss-Seidel.
        k (int): Número de repeticiones para medir el tiempo.

    Returns:
        dict: Un diccionario con los tiempos y resultados de ambos métodos.
    """
    tiempo_directo = medir_tiempo(metodo_directo, A, b, k)
    tiempo_gauss_seidel = medir_tiempo(lambda A, b: logica.Gauss_Seidel.gauss_seidel(A, b, x0, tol, max_iter), A, b, k)

    if(float (tiempo_gauss_seidel["promedio"]) < float (tiempo_directo["promedio"])):
        mas_rapido, veces = "Gauss-Seidel", float (tiempo_directo["promedio"]) / float (tiempo_gauss_seidel["promedio"])
    else:
        mas_rapido, veces = "Eliminación Gaussiana", float (tiempo_gauss_seidel["promedio"]) / float (tiempo_directo["promedio"])

    return {
        "metodo_directo": tiempo_directo,
        "gauss_seidel": tiempo_gauss_seidel
    }

def modo_experimento(tamano, metodo_directo, tol, max_iter, k):
    """
    Genera un sistema para cada n compara ambos métodos y devuelve una fila por tamaño
    
    Args:
        tamano (int): Tamaño del sistema a generar.
        metodo_directo (callable): Eliminación Gaussiana.
        tol (float): Tolerancia para la convergencia del método de Gauss-Seidel.
        max_iter (int): Número máximo de iteraciones para el método de Gauss-Seidel.
        k (int): Número de repeticiones para medir el tiempo.
    """
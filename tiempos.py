import time
import copy
import random
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
    return {"total": total, "promedio": tiempo_promedio, "resultado": resultado}

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

    if(float (tiempo_gauss_seidel['promedio']) < float (tiempo_directo['promedio'])):
        mas_rapido, veces = "Gauss-Seidel", float (tiempo_directo['promedio']) / float (tiempo_gauss_seidel['promedio'])
    else:
        mas_rapido, veces = "Eliminación Gaussiana", float (tiempo_gauss_seidel["promedio"]) / float (tiempo_directo["promedio"])

    return {
        "metodo_directo": tiempo_directo,
        "gauss_seidel": tiempo_gauss_seidel,
        "mas_rapido": mas_rapido,
        "veces": veces
   }

def modo_experimento(tamano, metodo_directo, x0, tol, max_iter, k):
    """
    Usa un sistema generado para cada n, compara ambos métodos y devuelve una fila por tamaño
    
    Args:
        tamano (int): Tamaño del sistema a generar.
        metodo_directo (callable): Eliminación Gaussiana.
        tol (float): Tolerancia para la convergencia del método de Gauss-Seidel.
        max_iter (int): Número máximo de iteraciones para el método de Gauss-Seidel.
        k (int): Número de repeticiones para medir el tiempo.
    """
    A_, b_ = generar_sistema(tamano)
    return comparar_tiempos(A_, b_, metodo_directo, x0, tol, max_iter, k)

def generar_sistema(tamano):
    """
    Genera un sistema de ecuaciones lineales con una matriz diagonal dominante y un vector b.

    Args:
        tamano (int): Tamaño del sistema a generar.

    Returns:
        tuple: Una tupla que contiene la matriz A y el vector b.
    """
    A = [[0.0 for _ in range(tamano)] for _ in range(tamano)]
    b = [0.0 for _ in range(tamano)]

    for i in range(tamano):
        suma_fila = 0.0
        for j in range(tamano):
            if i != j:
                A[i][j] = float(random.uniform(-20,20))  # Valores arbitrarios para los elementos fuera de la diagonal
                suma_fila += abs(A[i][j])
        A[i][i] = 5.0 * suma_fila  # Hacer que la diagonal sea dominante
        b[i] = float(i + 1)  # Valores arbitrarios para el vector b

    return A, b

def gauss_provicional(A, b): #solo prueba
    return [0.0] * len(b)

def main():
    """
    Main de prueba para ejecutar el experimento de comparación de tiempos
    entre Gauss-Seidel y Eliminación Gaussiana (cuando se implemente).
    """
    print("Inicio del experimento")
    tamano = 10  # Tamaño del sistema a generar
    x0 = [0.0] * tamano  # Valor inicial para el método de Gauss-Seidel
    tol = 1e-8  # Tolerancia para la convergencia del método de Gauss-Seidel
    max_iter = 100  # Número máximo de iteraciones para el método de Gauss-Seidel
    k = 10  # Número de repeticiones para medir el tiempo

    resultado_experimento = modo_experimento(tamano, gauss_provicional, x0, tol, max_iter, k)

    #Pruebas en consola, los datos deben mostrarse en la interfaz de usuario
    print("----Resultados Gauss-Seidel vs Eliminación Gaussiana----\n")
    print("**Gauss-Seidel**")
    print(f"Tiempo total: {resultado_experimento['gauss_seidel']['total']} s")
    print(f"Tiempo promedio: {resultado_experimento['gauss_seidel']['promedio']} s")
    print(f"Iteraciones: {resultado_experimento['gauss_seidel']['resultado']['iteraciones']}")
    print(f"Convergió: {resultado_experimento['gauss_seidel']['resultado']['convergio']}")
    print(f"Solución: {resultado_experimento['gauss_seidel']['resultado']['x']}")

    print("\n**Eliminación Gaussiana**")
    print(f"Tiempo total: {resultado_experimento['metodo_directo']['total']}")
    print(f"Tiempo promedio: {resultado_experimento['metodo_directo']['promedio']}")
    print(f"Solución: {resultado_experimento['metodo_directo']['resultado']}\n")

    print(f"El método más rápido es: {resultado_experimento['mas_rapido']}, siendo {resultado_experimento['veces']:.2f} veces más rápido que el otro método.")
    print("\nFin del experimento")

if __name__ == "__main__":
    main()
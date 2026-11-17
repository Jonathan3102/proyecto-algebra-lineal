def gauss_seidel(A, b, x0, tol, max_iter):
    """ Solución de Gauss-Seidel para sistemas de ecuaciones lineales Ax = b.
    Args:
        A (List[List[float]]): Tamaño n x n de la matriz cuadrada.
        b (List[float]): Lado derecho de la igualdad del sistema.
        x0 (List[float] | None): Valor inicial de la iteración. Si es None, usa vector cero.
        tol (float): Valor de tolerancia para la convergencia.
        max_iter (int): Número máximo de iteraciones.

    Returns:
        dict:Diccionario con la solución aproximada, número de iteraciones realizadas, y estado de convergencia.
        x (List[float]): Solución aproximada del sistema.
        iteraciones (int): Número de iteraciones realizadas.
        convergio (bool): Indica si el método convergió dentro del número máximo de iteraciones.
    """
    n = len(A)
    ## Validaciones de entrada(dimensiones compatibles, matriz cuadrada, entradas diagonales no nulas)
    if len(b) != n:
        raise ValueError("La matriz A y el vector b deben tener dimensiones compatibles.")
    if any(len(filas) != n for filas in A):
        raise ValueError("A debe ser una matriz cuadrada.")
    if any(abs(A[i][i]) < 1e-12 for i in range(n)):
        raise ValueError("La matriz debe tener entradas diagonales no nulas para Gauss-Seidel.")

    x = x0.copy() if x0 is not None else [0.0 for _ in range(n)]
    if len(x) != n:
        raise ValueError("El valor inicial debe tener el mismo tamaño que el sistema.")

    iteraciones = 0
    convergio = False
    # Iteración de Gauss-Seidel
    for iteracion in range(1, max_iter + 1):
        x_nuevo = x.copy()

        for i in range(n):
            suma = sum(A[i][j] * x_nuevo[j] for j in range(n) if j != i)
            x_nuevo[i] = (b[i] - suma) / A[i][i]

        error = max(abs(x_nuevo[i] - x[i]) for i in range(n))
        print(f"Iteración {iteracion}: x = {x_nuevo}, mayor cambio = {error}")  # Debug: muestra el progreso de la iteración.
        x = x_nuevo

        if error < tol:
            iteraciones = iteracion
            convergio = True

    if(not convergio): # No convergió dentro del número máximo de iteraciones.
        iteraciones = max_iter
        convergio = False

    return {
        "x": x,
        "iteraciones": iteraciones,
        "convergio": convergio,
    }


def main ():
    print("Inicio")
    A = [
        [10, 1, 1],
        [1, 10, 1],
        [1, 1, 10],
    ]
    b = [12,12,12]
    x0 = [0, 0, 0]

    resultado = gauss_seidel(A, b, x0, 10**(-6), 10)
    if(not resultado["convergio"]):
        print("No se alzanzó la tolerancia. Aumente el máximo de iteraciones.")
        print(f"Última aproximación: {resultado["x"]}")
        print(f"Iteraciones realizadas: {resultado["iteraciones"]}")
    else:        
        print("\nSistema de ecuaciones resuelto con éxito.")
        print(f"Solución: {resultado["x"]}")
        print(f"Iteraciones: {resultado["iteraciones"]}")

main()
from fractions import Fraction


def _convertir_fraccion(valor):
    """Convierte un valor numérico a Fraction, por ejemplo, "1/3" a un tercio, 
       acepta enteros, decimales, fracciones y textos numéricos.
    """
    try:
        # Pasamos por str() para que decimales como 0.1 no tengan problemas por un float
        return Fraction(str(valor))
    except (ValueError, TypeError, ZeroDivisionError) as error:
        raise ValueError(f"Valor numérico no válido: {valor!r}.") from error


def _crear_matriz_ampliada(A, b):
    """Valida las dimensiones y construye una nueva matriz ampliada [A | b].

    A debe tener n filas y n columnas; b debe contener n valores.
    """
    n = len(A)
    if n == 0:
        raise ValueError("La matriz A no puede estar vacía.")
    if len(b) != n:
        raise ValueError("b debe tener un valor por cada fila de A.")

    matriz = []
    for indice, fila in enumerate(A):
        if len(fila) != n:
            raise ValueError("A debe ser cuadrada y todas sus filas deben medir lo mismo.")
        fila_ampliada = [_convertir_fraccion(valor) for valor in fila]
        # Pegamos el término independiente al final de cada fila: [fila de A | b_i]
        fila_ampliada.append(_convertir_fraccion(b[indice]))
        matriz.append(fila_ampliada)
    return matriz


def eliminar(matriz):
    """Transforma una matriz ampliada en forma escalonada mediante operaciones de filas.

    Devuelve dos listas: las operaciones descritas con texto y las posiciones
    de los pivotes finales.
    """
    n = len(matriz)
    pasos = []
    pivotes = []
    fila_pivote = 0

    for columna in range(n + 1):
        # Pivoteo parcial: buscamos el número más grande en valor absoluto para mayor estabilidad
        mejor_fila = fila_pivote
        for fila in range(fila_pivote + 1, n):
            if abs(matriz[fila][columna]) > abs(matriz[mejor_fila][columna]):
                mejor_fila = fila
        if matriz[mejor_fila][columna] == 0:
            # Columna toda en ceros de aquí para abajo, pasamos a la siguiente
            continue

        if mejor_fila != fila_pivote:
            # Subimos la fila con el mejor pivote a la posición actual
            matriz[fila_pivote], matriz[mejor_fila] = (
                matriz[mejor_fila], matriz[fila_pivote]
            )
            pasos.append(f"Intercambiar F_{fila_pivote + 1} con F_{mejor_fila + 1}")

        pivotes.append((fila_pivote, columna))
        for fila in range(fila_pivote + 1, n):
            # Calculamos por cuánto multiplicar la fila pivote para hacer cero debajo
            factor = matriz[fila][columna] / matriz[fila_pivote][columna]
            if factor == 0:
                continue
            # Aplicamos la resta a toda la fila (incluyendo b) para que la ecuación no cambie
            for indice in range(columna, n + 1):
                matriz[fila][indice] -= factor * matriz[fila_pivote][indice]
            pasos.append(
                f"F_{fila + 1} - ({factor}) * F_{fila_pivote + 1} -> F_{fila + 1}"
            )

        fila_pivote += 1
        if fila_pivote == n:
            # Ya se acomodaron pivotes en todas las filas, no hace falta seguir
            break

    return pasos, pivotes


def _calcular_rangos(matriz_escalonada, n):
    """Calcula el rango de A y el de su matriz ampliada, devolviéndolos en ese orden
    a partir de una matriz ya escalonada.

    Recibe el número de variables 'n' y asume que el escalonamiento ya se hizo
    (esta función no modifica ni escala la matriz). El rango refleja cuántas filas
    independientes no nulas hay en cada parte.
    """
    rango_A = 0
    hay_contradiccion = False
    for fila in matriz_escalonada:
        # fila[:n] son solo los coeficientes de A (sin la última columna que es b)
        if any(valor != 0 for valor in fila[:n]):
            rango_A += 1
        elif fila[n] != 0:
            # En A todo es cero, pero en b no: queda algo tipo 0 = 5 (contradicción)
            hay_contradiccion = True

    rango_ampliada = rango_A
    if hay_contradiccion:
        # Una fila 0 = algo_distinto_de_cero sube el rango de la ampliada en 1
        rango_ampliada += 1
    return rango_A, rango_ampliada


def _sustitucion_atras(matriz, pivotes, valores, homogeneo=False):
    """Resuelve por sustitución hacia atrás las variables con pivote en una matriz
    ya escalonada, partiendo de los valores dados para las variables libres.

    Devuelve una lista nueva con la solución (sin alterar 'valores'). Usa pivotes de
    A y, si homogeneo es True, resuelve Ax = 0 en lugar de usar b.
    """
    # Copiamos para no tocar la lista original que nos pasaron
    solucion = valores[:]
    n = len(solucion)
    # Vamos de abajo hacia arriba porque la última fila ya deja despejar rápido
    for fila, columna in reversed(pivotes):
        termino = Fraction(0) if homogeneo else matriz[fila][n]
        # Restamos lo que ya conocemos de las variables a la derecha del pivote
        suma = sum(matriz[fila][j] * solucion[j] for j in range(columna + 1, n))
        solucion[columna] = (termino - suma) / matriz[fila][columna]
    return solucion


def _calcular_Ax(matriz_inicial, solucion):
    """Calcula el producto A * x para una solución propuesta, usando los coeficientes
    originales guardados en la matriz ampliada inicial.

    Recibe la matriz ampliada de partida y la lista de valores propuestos para cada
    incógnita. Devuelve una lista con el resultado de cada ecuación para verificar
    si coincide con el vector b.
    """
    n = len(solucion)
    # range(n) deja fuera fila[-1] (que es b), multiplicando solo los coeficientes de A
    return [
        sum(fila[j] * solucion[j] for j in range(n))
        for fila in matriz_inicial
    ]


def _expresion_general(constante, coeficientes, parametros):
    """Arma el texto de una variable escrita en función de los parámetros
    (por ejemplo, "3 - 2*t_1 + t_2" a partir de constante=3, coeficientes=[-2, 1]
    y parámetros=["t_1", "t_2"]).

    Solo genera la expresión en texto; no calcula ni reemplaza valores de los parámetros.
    """
    expresion = str(constante) if constante != 0 else ""
    for coeficiente, parametro in zip(coeficientes, parametros):
        if coeficiente == 0:
            continue
        magnitud = abs(coeficiente)
        # Evitamos escribir "1*t_1" cuando el coeficiente es 1 o -1
        termino = parametro if magnitud == 1 else f"{magnitud}*{parametro}"
        if expresion:
            signo = " - " if coeficiente < 0 else " + "
            expresion += signo + termino
        else:
            expresion = ("-" if coeficiente < 0 else "") + termino
    return expresion or "0"


def resolver_sistema_completo(A, b):
    """Resuelve un sistema cuadrado y devuelve un diccionario con sus resultados.

    A contiene los coeficientes y b los términos independientes. El campo tipo
    indica "unica", "infinitas" o "ninguna". Siempre incluye matrices, pasos,
    pivotes, rangos y un mensaje, los demás campos dependen de la clasificacion.
    Las matrices y soluciones conservan sus números como objetos Fraction.
    """
    matriz_inicial = _crear_matriz_ampliada(A, b)
    # Trabajamos sobre una copia para conservar intacta la matriz inicial
    matriz_esc = [fila[:] for fila in matriz_inicial]
    pasos, pivotes = eliminar(matriz_esc)
    n = len(A)
    rango_A, rango_amp = _calcular_rangos(matriz_esc, n)
    # Ignoramos pivotes en la columna n porque esa columna corresponde a b, no a una variable
    columnas_pivote = [columna for fila, columna in pivotes if columna < n]

    resultado = {
        "matriz_escalonada": matriz_esc,
        "pasos": pasos,
        "rango_A": rango_A,
        "rango_ampliada": rango_amp,
        "matriz_inicial": matriz_inicial,
        "pivotes": pivotes,
        "columnas_pivote": columnas_pivote,
    }

    if rango_A < rango_amp:
        # Si la ampliada tiene más rango que A, hay contradicción -> no existe solución
        resultado["tipo"] = "ninguna"
        resultado["mensaje"] = "El sistema no tiene solución (Inconsistente)."
        return resultado

    ceros = [Fraction(0)] * n
    # Ponemos variables libres en 0 para sacar una solución base (o la única si no hay libres)
    solucion_base = _sustitucion_atras(matriz_esc, pivotes, ceros)

    if rango_A == n:
        # Hay pivote en cada variable: el sistema tiene una sola solución
        resultado["tipo"] = "unica"
        resultado["mensaje"] = "El sistema tiene solución única."
        resultado["solucion"] = solucion_base
        resultado["Ax"] = _calcular_Ax(matriz_inicial, solucion_base)
        resultado["comprobacion"] = resultado["Ax"] == [fila[-1] for fila in matriz_inicial]
        return resultado

    # Las columnas sin pivote son variables libres; les damos nombres t_1, t_2, ...
    variables_libres = [columna for columna in range(n) if columna not in columnas_pivote]
    parametros = [f"t_{indice + 1}" for indice in range(len(variables_libres))]
    vectores_parametros = []
    for columna in variables_libres:
        valores = [Fraction(0)] * n
        # Ponemos 1 en esta variable libre y 0 en las demás para ver cómo mueve al resto
        valores[columna] = Fraction(1)
        vector = _sustitucion_atras(matriz_esc, pivotes, valores, homogeneo=True)
        vectores_parametros.append(vector)

    solucion_general = []
    for columna in range(n):
        # Armamos cada x_i como: valor_base + coef_1*t_1 + coef_2*t_2 + ...
        coeficientes = [vector[columna] for vector in vectores_parametros]
        expresion = _expresion_general(solucion_base[columna], coeficientes, parametros)
        solucion_general.append(f"x_{columna + 1} = {expresion}")

    resultado.update({
        "tipo": "infinitas",
        "mensaje": "El sistema tiene infinitas soluciones.",
        "variables_libres": variables_libres,
        "nombres_parametros": parametros,
        "solucion_general": solucion_general,
        "solucion_base": solucion_base,
        "vectores_parametros": vectores_parametros,
    })
    return resultado


def obtener_solucion_particular(resultado, valores_parametros):
    """Evalúa la solución general con valores concretos para cada parámetro y comprueba
    que la solución resultante cumpla Ax = b.

    'resultado' debe venir de resolver_sistema_completo en un sistema de infinitas
    soluciones, y 'valores_parametros' debe dar un valor por cada parámetro en orden.
    No modifica 'resultado' y devuelve solucion, Ax, b y comprobacion.
    """
    if resultado["tipo"] != "infinitas":
        raise ValueError("Los parámetros se aplican a sistemas con infinitas soluciones.")
    if len(valores_parametros) != len(resultado["nombres_parametros"]):
        raise ValueError("Debes indicar un valor por cada parámetro.")

    # Partimos de la solución base y le sumamos cada parámetro multiplicado por su vector
    solucion = resultado["solucion_base"][:]
    for valor, vector in zip(valores_parametros, resultado["vectores_parametros"]):
        parametro = _convertir_fraccion(valor)
        for columna in range(len(solucion)):
            solucion[columna] += parametro * vector[columna]

    valores_Ax = _calcular_Ax(resultado["matriz_inicial"], solucion)
    valores_b = [fila[-1] for fila in resultado["matriz_inicial"]]
    return {
        "solucion": solucion,
        "Ax": valores_Ax,
        "b": valores_b,
        "comprobacion": valores_Ax == valores_b,
    }


#Pruebas
"""
def imprimir_resultado(resultado):
    print("=" * 50)
    print(resultado["mensaje"])
    print(f"Rango(A) = {resultado['rango_A']} | Rango([A|b]) = {resultado['rango_ampliada']}")

    print("\nPasos realizados:")
    for i, paso in enumerate(resultado["pasos"], start=1):
        print(f"  {i}. {paso}")

    print("\nMatriz escalonada [A|b]:")
    for fila in resultado["matriz_escalonada"]:
        fila_str = [str(valor) for valor in fila]
        print("  [" + ", ".join(fila_str[:-1]) + f" | {fila_str[-1]}]")

    if resultado["tipo"] == "unica":
        sol = [f"x_{i+1} = {val}" for i, val in enumerate(resultado["solucion"])]
        print("\nSolución única:", ", ".join(sol))
        print("Comprobación Ax:", [str(v) for v in resultado["Ax"]])
        print("¿Cumple Ax = b?:", resultado["comprobacion"])

    elif resultado["tipo"] == "infinitas":
        print("\nSolución general:")
        for ecuacion in resultado["solucion_general"]:
            print(f"  {ecuacion}")


# --- Ejemplo 1: Solución única ---
A1 = [[3, 2, 1], [1, 2, 1], [1, 1, 2]]
b1 = [48, 28, 31]
r1 = resolver_sistema_completo(A1, b1)
imprimir_resultado(r1)


# --- Ejemplo 2: Infinitas soluciones + particular con t_1 = 2 ---
A2 = [[1, 2, -1], [2, 4, -2], [1, 1, 1]]
b2 = [3, 6, 6]
r2 = resolver_sistema_completo(A2, b2)
imprimir_resultado(r2)

p2 = obtener_solucion_particular(r2, [2])
part_str = ", ".join(f"x_{i+1} = {val}" for i, val in enumerate(p2["solucion"]))
print(f"\nSolución particular (t_1 = 2): {part_str}")
print("Comprobación Ax:", [str(v) for v in p2["Ax"]], "| ¿Cumple Ax = b?:", p2["comprobacion"])


# --- Ejemplo 3: Sin solución ---
A3 = [[1, 1, 1], [2, 2, 2], [1, -1, 0]]
b3 = [1, 3, 0]
r3 = resolver_sistema_completo(A3, b3)
imprimir_resultado(r3)
"""
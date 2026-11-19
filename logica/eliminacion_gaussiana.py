from fractions import Fraction


def convertir_fraccion(valor):
    try:
        return Fraction(str(valor))
    except (ValueError, TypeError, ZeroDivisionError) as error:
        raise ValueError(f"Valor numerico no valido: {valor!r}.") from error


def crear_matriz_ampliada(A, b):
    n = len(A)
    if n == 0:
        raise ValueError("La matriz A no puede estar vacia.")
    if len(b) != n:
        raise ValueError("b debe tener un valor por cada fila de A.")

    matriz = []
    for indice, fila in enumerate(A):
        if len(fila) != n:
            raise ValueError("A debe ser cuadrada y todas sus filas deben medir lo mismo.")
        fila_ampliada = [convertir_fraccion(valor) for valor in fila]
        fila_ampliada.append(convertir_fraccion(b[indice]))
        matriz.append(fila_ampliada)
    return matriz


def eliminar(matriz):
    n = len(matriz)
    pasos = []
    matrices_pasos = []
    pivotes = []
    fila_pivote = 0

    for columna in range(n + 1):
        mejor_fila = fila_pivote
        for fila in range(fila_pivote + 1, n):
            if abs(matriz[fila][columna]) > abs(matriz[mejor_fila][columna]):
                mejor_fila = fila
        if matriz[mejor_fila][columna] == 0:
            continue

        if mejor_fila != fila_pivote:
            matriz[fila_pivote], matriz[mejor_fila] = (
                matriz[mejor_fila], matriz[fila_pivote]
            )
            pasos.append(f"Intercambiar F_{fila_pivote + 1} con F_{mejor_fila + 1}")
            matrices_pasos.append([fila[:] for fila in matriz])

        pivotes.append((fila_pivote, columna))
        for fila in range(fila_pivote + 1, n):
            factor = matriz[fila][columna] / matriz[fila_pivote][columna]
            if factor == 0:
                continue
            for indice in range(columna, n + 1):
                matriz[fila][indice] -= factor * matriz[fila_pivote][indice]
            pasos.append(
                f"F_{fila + 1} - ({factor}) * F_{fila_pivote + 1} -> F_{fila + 1}"
            )
            matrices_pasos.append([valores[:] for valores in matriz])

        fila_pivote += 1
        if fila_pivote == n:
            break

    return pasos, matrices_pasos, pivotes


def eliminacion_gaussiana(A, b):
    matriz = (A, b)
    pasos, _, _ = eliminar(matriz)
    return matriz, pasos


def calcular_rangos(matriz_escalonada, n):
    rango_A = 0
    hay_contradiccion = False
    for fila in matriz_escalonada:
        if any(valor != 0 for valor in fila[:n]):
            rango_A += 1
        elif fila[n] != 0:
            hay_contradiccion = True

    rango_ampliada = rango_A
    if hay_contradiccion:
        rango_ampliada += 1
    return rango_A, rango_ampliada


def sustitucion_atras(matriz, pivotes, valores, homogeneo=False):
    solucion = valores[:]
    n = len(solucion)
    for fila, columna in reversed(pivotes):
        termino = Fraction(0) if homogeneo else matriz[fila][n]
        suma = sum(matriz[fila][j] * solucion[j] for j in range(columna + 1, n))
        solucion[columna] = (termino - suma) / matriz[fila][columna]
    return solucion


def calcular_Ax(matriz_inicial, solucion):
    n = len(solucion)
    return [
        sum(fila[j] * solucion[j] for j in range(n))
        for fila in matriz_inicial
    ]


def expresion_general(constante, coeficientes, parametros):
    expresion = str(constante) if constante != 0 else ""
    for coeficiente, parametro in zip(coeficientes, parametros):
        if coeficiente == 0:
            continue
        magnitud = abs(coeficiente)
        termino = parametro if magnitud == 1 else f"{magnitud}*{parametro}"
        if expresion:
            signo = " - " if coeficiente < 0 else " + "
            expresion += signo + termino
        else:
            expresion = ("-" if coeficiente < 0 else "") + termino
    return expresion or "0"


def resolver_sistema_completo(A, b):
    matriz_inicial = (A, b)
    matriz_esc = [fila[:] for fila in matriz_inicial]
    pasos, matrices_pasos, pivotes = eliminar(matriz_esc)
    n = len(A)
    rango_A, rango_amp = calcular_rangos(matriz_esc, n)
    columnas_pivote = [columna for fila, columna in pivotes if columna < n]

    resultado = {
        "matriz_escalonada": matriz_esc,
        "pasos": pasos,
        "rango_A": rango_A,
        "rango_ampliada": rango_amp,
        "matriz_inicial": matriz_inicial,
        "matrices_pasos": matrices_pasos,
        "pivotes": pivotes,
        "columnas_pivote": columnas_pivote,
    }

    if rango_A < rango_amp:
        resultado["tipo"] = "ninguna"
        resultado["mensaje"] = "El sistema no tiene solución (Inconsistente)."
        return resultado

    ceros = [Fraction(0)] * n
    solucion_base = sustitucion_atras(matriz_esc, pivotes, ceros)

    if rango_A == n:
        resultado["tipo"] = "unica"
        resultado["mensaje"] = "El sistema tiene solución única."
        resultado["solucion"] = solucion_base
        resultado["Ax"] = calcular_Ax(matriz_inicial, solucion_base)
        resultado["comprobacion"] = resultado["Ax"] == [fila[-1] for fila in matriz_inicial]
        return resultado

    variables_libres = [columna for columna in range(n) if columna not in columnas_pivote]
    parametros = [f"t_{indice + 1}" for indice in range(len(variables_libres))]
    vectores_parametros = []
    for columna in variables_libres:
        valores = [Fraction(0)] * n
        valores[columna] = Fraction(1)
        vector = sustitucion_atras(matriz_esc, pivotes, valores, homogeneo=True)
        vectores_parametros.append(vector)

    solucion_general = []
    for columna in range(n):
        coeficientes = [vector[columna] for vector in vectores_parametros]
        expresion = expresion_general(solucion_base[columna], coeficientes, parametros)
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
    if resultado["tipo"] != "infinitas":
        raise ValueError("Los parametros se aplican a sistemas con infinitas soluciones.")
    if len(valores_parametros) != len(resultado["nombres_parametros"]):
        raise ValueError("Debes indicar un valor por cada parámetro.")

    solucion = resultado["solucion_base"][:]
    for valor, vector in zip(valores_parametros, resultado["vectores_parametros"]):
        parametro = convertir_fraccion(valor)
        for columna in range(len(solucion)):
            solucion[columna] += parametro * vector[columna]

    valores_Ax = calcular_Ax(resultado["matriz_inicial"], solucion)
    valores_b = [fila[-1] for fila in resultado["matriz_inicial"]]
    return {
        "solucion": solucion,
        "Ax": valores_Ax,
        "b": valores_b,
        "comprobacion": valores_Ax == valores_b,
    }


def formatear_matriz(matriz):
    return [[str(valor) for valor in fila] for fila in matriz]

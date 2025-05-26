from utils import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tabulate import tabulate
import pandas as pd
import numpy as np
import math

funciones = [{
    "asciimath": "x^4 * sqrt(3 + 2x^2) / 3",
    "fx": lambda x: (x**4 * math.sqrt(3 + 2 * x**2)) / 3
}, {
    "asciimath": "x^5 / root(5)(x^2 + 4)",
    "fx": lambda x: x**5 / math.pow(x**2 + 4, 1/5)
}]


def metodo_romberg(f, a, b, decimals):
    epsilon = 10**(-decimals)
    xi = [a, b]
    h = b - a
    estimaciones_trapecio = [h/2 * (f(a) + f(b))]
    tabla_romberg = [
        [h, estimaciones_trapecio[0]]
    ]

    encabezado = ["h", "Regla del trapecio\nO(h^2)"]

    j = 1
    while True:
        h /= 2
        
        encabezado.append(f"O(h^{2*(j + 1)})")

        integral = estimaciones_trapecio[-1]/2
        sum = 0
        for k in range(1, 2**(j - 1) + 1):
            mid = (xi[2*k - 1] + xi[2*k - 2]) / 2
            xi.insert(2*k - 1, mid)
            sum += f(mid)
        
        integral += h * sum
        estimaciones_trapecio.append(integral)
        tabla_romberg.append([h, integral])
        
        for i in range(j):
            last = tabla_romberg[j][-1]
            bef_last = tabla_romberg[j-1][i + 1]
            denominador = 4**(i + 1) - 1
            tabla_romberg[j].append(last + (last - bef_last) / denominador)

        if abs(tabla_romberg[-1][-1] - tabla_romberg[-1][-2]) < epsilon:
            break;
        j += 1

    caja_titulo_3("RESULTADOS")
    caja_titulo_4("Tabla de extrapolación de Romberg")
    print("[bold]OBSERVACIÓN:[/bold] En caso de no visualizar la tabla completa, ajuste el tamaño de su terminal o de la fuente y vuelva a intentar.")
    print(tabulate(tabla_romberg, headers=encabezado, tablefmt="grid", floatfmt=f".{decimals+2}f"))

    return tabla_romberg[-1][-1]


def menu_programa4():
    while True:
        limpiar_pantalla()
        caja_titulo_2("INTEGRACIÓN NUMÉRICA")
        print()

        i = 1
        for f in funciones:
            print(f"{i}. Integrar f(x) = {f["asciimath"]} en un intervalo")
            i+=1
        print(f"{i}. Regresar al menú principal")
        opcion = int(input(f"\n\u27A5 Ingrese la opción de su preferencia: "))

        if opcion == i:
            break
        if opcion < 1 or opcion > i:
            print("Opcion INVALIDA, seleccione otra opcion.")
            continue

        print("\u27A5 Ingrese el intervalo de integración [x0, xn]:")
        x0 = float(input(f"\tx0 = "))
        xn = float(input(f"\txn = "))
        
        while True:
            digitos_precision = int(input("\u27A5 Ingrese el número de digitos de precisión (entre 1 y 10): "))
            if digitos_precision < 1 or digitos_precision > 10:
                print("ERROR. Ingrese un número válido de digitos.")
            else:
                break
        
        if x0 != xn:
            estimacion = metodo_romberg(funciones[opcion - 1]["fx"], x0, xn, digitos_precision)
        else:
            estimacion = 0
        
        print()
        caja_titulo_4("Estimación obtenida")
        print(f"\u222B_({x0})^({xn}) {funciones[opcion - 1]["asciimath"]} = {estimacion}")

        input("\nPresione enter para volver a mostrar el menú...")

import numpy as np
from tabulate import tabulate
from utils import *
from rich import print


# Algunas utilidades básicas
# Función para calcular la norma espectral
def norm_esp(vec):
    return max(map(lambda x: abs(x), vec))


# Función para leer una toleracia valida
def leer_tolerancia():
    tol = float(input("\u27A5 Ingrese la tolerancia: "))

    while tol <= 0:
        print("La tolerancia debe ser mayor que cero.")
        tol = float(input("\u27A5 Ingrese la tolerancia: "))

    return tol


# Función para leer un numero máximo de iteraciones valido
def leer_max_iteraciones():
    max_iter = int(input("\u27A5 Ingrese el numero maximo de iteraciones: "))

    while max_iter <= 0:
        print("El numero de iteraciones debe ser mayor que cero.")
        max_iter = int(input("\u27A5 Ingrese el numero maximo de iteraciones: "))

    return max_iter


"""
Colección de sistemas de ecuaciones no lineales solicitados.

Estructura de cada sistema:
- "vars": Tupla con los nombres de las variables del sistema.
- "ecuaciones_texto": Representación textual de las ecuaciones.
- "fx": Función lambda que evalúa el sistema de ecuaciones.
           - Recibe los valores de las variables como argumentos.
           - Retorna un array de NumPy con los valores de las funciones.
- "jx": Función lambda que calcula la matriz jacobiana.
           - Recibe los valores de las variables como argumentos.
           - Retorna una matriz de NumPy con las derivadas parciales.

Ejemplo de uso:
    sistema = sistemas[0]  # Primer sistema de 2 variables
    variables = sistema["vars"]  # ("x", "y")
    valor_sistema = sistema["fx"](1, 2)  # Evalúa el sistema en x=1, y=2
    jacobiano = sistema["jx"](1, 2)  # Calcula el jacobiano en x=1, y=2
"""

sistemas = [{
    "vars": ("x", "y"),
    "ecuaciones_texto": (
        "f_1(x,y) = x^2 + x y + 2 y^2 - 5 = 0",
        "f_2(x,y) = 5y - 2 x y^2 + 3 = 0"
    ),
    "fx": lambda x, y: np.array([
        [x**2 + x * y + 2 * y**2 - 5],
        [5 * y - 2 * x * y**2 + 3]
    ]),
    "jx": lambda x, y: np.matrix([
        [2 * x + y, x + 4 * y],
        [-2 * y**2, 5 - 4 * x * y]
    ])
}, {
    "vars": ("x", "y"),
    "ecuaciones_texto": (
        "f_1(x,y) = x^2 - 3y^2 - 10 = 0",
        "f_2(x,y) = 2y^2 - 3xy + 1 = 0"
    ),
    "fx": lambda x, y: np.array([
        [x**2 - 3 * y**2 - 10],
        [2 * y**2 - 3 * x * y + 1]
    ]),
    "jx": lambda x, y: np.matrix([
        [2 * x, -6 * y],
        [-3 * y, 4 * y - 3 * x]
    ])
}, {
    "vars": ("x", "y", "z"),
    "ecuaciones_texto": (
        "f_1(x,y,z) = 3x^2 + y^2 - 8y + 2z^2 - 5 = 0",
        "f_2(x,y,z) = -2x^2 - 12x + y^2 - 3z^2 + 10 = 0",
        "f_3(x,y,z) = - x + 2y + 5z = 0"
    ),
    "fx": lambda x, y, z: np.array([
        [3 * x**2 + y**2 - 8 * y + 2 * z**2 - 5],
        [-2 * x**2 - 12 * x + y**2 - 3 * z**2 + 10],
        [-x + 2 * y + 5 * z]
    ]),
    "jx": lambda x, y, z: np.matrix([
        [6 * x, 2 * y - 8, 4 * z],
        [-4 * x - 12, 2 * y, -6 * z],
        [-1, 2, 5]
    ])
}, {
    "vars": ("x", "y", "z"),
    "ecuaciones_texto": (
        "f_1(x,y,z) = x^2 + y^2 - 2z + 3 = 0",
        "f_2(x,y,z) = x + y + z - 5 = 0",
        "f_3(x,y,z) = x^2 - y^2 + z^2 - 9 = 0"
    ),
    "fx": lambda x, y, z: np.array([
        [x**2 + y**2 - 2 * z + 3],
        [x + y + z - 5],
        [x**2 - y**2 + z**2 - 9]
    ]),
    "jx": lambda x, y, z: np.matrix([
        [2 * x, 2 * y, -2],
        [1, 1, 1],
        [2 * x, -2 * y, 2 * z]
    ])
}]


# Función para leer el vector inicial con variables vars
def lectura_vector_inicial(vars):
    x0 = []
    print("Ingrese las componentes del vector inicial:")
    for var in vars:
        component = float(input(f"{var}^(0) = "))
        x0.append([component])

    return np.array(x0)


# Función que implementa el método de Broyden
def metodo_broyden(sistema, x0, tol, max_iter):
    k = 1
    xk_prev = x0
    fxk_prev = sistema["fx"](*xk_prev.flatten())

    try:
        ak_prev = np.linalg.inv(sistema["jx"](*xk_prev.flatten()))
    except np.linalg.LinAlgError:
        print("¡ERROR!")
        print("La matriz jacobiana es singular en el vector inicial.")
        print("No se pudo utilizar el método de Newton en la primer iteración.")
        print("Intente probando con otros valores iniciales.")
        return
    
    tol_alcanzada = False
    xk = None
    error = None

    table = []
    headers = ["k", "X^(k-1)", "f(X^(k-1))", "A^(k-1)", "X^(k)", "f(X^(k))", "Error"]
    while k <= max_iter:
        xk = np.array(xk_prev - ak_prev * sistema["fx"](*xk_prev.flatten()))
        fxk = sistema["fx"](*xk.flatten())
        delta_xk = xk - xk_prev
        delta_fxk = fxk - fxk_prev
        error= norm_esp(fxk)

        table.append(
            list(map(str, [k, xk_prev, fxk_prev, ak_prev, xk, fxk, error])))

        if error < tol:
            tol_alcanzada = True
            break

        ak = ak_prev + (delta_xk - ak_prev * delta_fxk) * delta_xk.T * ak_prev / (delta_xk.T * ak_prev * delta_fxk)

        xk_prev = xk
        fxk_prev = fxk
        ak_prev = ak

        k += 1

    print(tabulate(table, headers, tablefmt="fancy_grid"))
    print()
    if tol_alcanzada:
        print(f"\u27A4 La tolerancia fue alcanzada en la iteración k = {k} (última mostrada):")
        print(f"\u27A4 La solución encontrada con un error de {error} es: X^T = ", xk.T)
    else:
        print("\u27A4 La solución no converge, el número máximo de iteraciones fue alcanzado pero NO la tolerancia.")
        print(f"\u27A4 La mejor aproximación encontrada con un error de {error} es: X^T = ", xk.T)


def menu_otro_calculo():
    while True:
        print("1. Probar otros datos iniciales")
        print("2. Elegir otro sistema")
        print("3. Regresar al menú principal")
        
        opcion = int(input("\u27A5 Ingrese una opcion: "))
        if 1 <= opcion <= 3:
            return opcion

        print("Opcion invalida, vuelva a intentar.\n")


def menu_programa1():
    opcion_otro_calculo = 0
    while True:
        limpiar_pantalla()
        caja_titulo_2("SISTEMAS DE ECUACIONES NO LINEALES")
        print()
        i = 1
        for sistema in sistemas:
            print(f"{i}. " + "\n   ".join(sistema["ecuaciones_texto"]))
            print()
            i += 1
        print(f"{i}. Regresar al menu principal")

        opcion = int(input("\n\u27A5 Seleccione una opción: "))
        if opcion == 5:
            break
        if opcion < 1 or opcion > 5:
            print("Opcion INVALIDA, seleccione otra opcion.")
            continue

        # Sistema elegido por el usuario
        sistema = sistemas[opcion - 1]
        while True:
            print("\nDatos iniciales:\n")
            # Lectura del vector inicial, tolerancia y máximo número de iteraciones
            x0 = lectura_vector_inicial(sistema["vars"])
            print()
            tol = leer_tolerancia()
            print()
            max_iter = leer_max_iteraciones()

            # Ejecución del método de Broyden con los valores dados
            metodo_broyden(sistema, x0, tol, max_iter)
            
            # Opciones adicionales para el usuario
            input("\nPresione Enter para continuar...\n")
            opcion_otro_calculo = menu_otro_calculo()
            if opcion_otro_calculo > 1:
                break

        if opcion_otro_calculo == 3:
            break

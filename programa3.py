from utils import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tabulate import tabulate
import pandas as pd
import numpy as np
import csv
from pathlib import Path

DECIMALES = 8
SPLINE_HEADERS = ("i", "x_i", "f(x_i)", "h_i", "f_0^[1]", "S_i", "a_i", "b_i", "c_i", "d_i")

def leer_csv():
    limpiar_pantalla()
    caja_titulo_4("CAPTURA DE PUNTOS POR ARCHIVO CSV")

    print("[bold]Notas:[/bold]") 
    print("◆ El CSV debe tener 2 columnas de la forma (x_i, f(x_i)) sin encabezados.")
    print("◆ Se agrego 'prueba.csv' como ejemplo en la carpeta del programa.")
    print("\n[bold]Ejemplo:[/bold]")
    print("0.95, -1.1\n1.73, 0.27\n2.23, -0.29\n2.77, 0.56\n2.99, 1.0")

    while True:
        ruta = Path(input("\n➥ Ingrese la ruta del archivo CSV: "))
        if ruta.is_file() and ruta.suffix == ".csv":
            break
        else:
            print("El archivo no existe o no es un CSV. Intente nuevamente.")
    
    return ruta

def leer_puntos():
    limpiar_pantalla()
    caja_titulo_4("CAPTURA DE PUNTOS POR CONSOLA")
    while True:
        try:
            m = int(input("➥ ¿Cuántos puntos (x_i, y_i) desea ingresar? ").strip())
            if m <= 0:
                print("Debe ingresar al menos un punto.")
                continue
            break
        except ValueError:
            print("Por favor, ingrese un número entero válido.")

    puntos = []
    print(f"\n➥ Ingrese {m} puntos en el formato: x_i y_i (separados por espacio, por ejemplo: 3.45 4.4)")
    for i in range(m):
        while True:
            entrada = input(f"➤ Punto {i}: ").strip()
            partes = entrada.split()
            if len(partes) != 2:
                print("Debe ingresar exactamente dos valores separados por espacio.")
                continue
            try:
                x = float(partes[0])
                y = float(partes[1])
                puntos.append((x, y))
                break
            except ValueError:
                print("Ambos valores deben ser números válidos.")

    # Ordena los puntos por el valor de x
    puntos.sort(key=lambda p: p[0])
    # Imprime los puntos ingresados
    puntos_correctos = False
    while not puntos_correctos:
        print("\nPuntos ingresados ordenados:")
        tabla = [[i, x, y] for i, (x, y) in enumerate(puntos)]
        print(tabulate(tabla, headers=["i", "x_i", "y_i"], tablefmt="fancy_grid"))

        puntos_correctos = ("s" == input("¿Los puntos son correctos? (s/n): ").strip().lower())

        if puntos_correctos:
            break
        
        while True:
            try:
                i = int(input(f"\n➥ Ingrese el índice del punto a modificar (0 a {m-1}): ").strip())
                if 0 <= i < m:
                    break
                print(f"El índice debe estar entre 0 y {m-1}")
            except ValueError:
                print("Por favor, ingrese un número entero válido.")

        punto = input(f"Punto {i}: ").strip()
        x, y = punto.split()
        puntos[i] = (float(x), float(y))
        puntos.sort(key=lambda p: p[0])
        

    # Escribe los puntos en un archivo llamado 'puntos.csv'
    with open("puntos.csv", "w", newline="") as archivo:
        escritor = csv.writer(archivo)
        for x, y in puntos:
            escritor.writerow([x, y])
    
    print("\n\u26A0\uFE0F  Los puntos han sido guardados en 'puntos.csv' en el mismo directorio de este programa por si los utiliza en futuro.")
    input("Presione enter para continuar...")
    return Path("puntos.csv")


# Realiza los calculos correspondientes para el método
# Recibe el path de un archivo CSV con los puntos a utilizar
def generar_tabla(file):
    df = pd.read_csv(file, header=None, names=['x_i', 'f(x_i)'])
    df.index.name = 'i'
    n = len(df) - 1

    df['h_i'] = df['x_i'].diff().shift(-1) # Calcula las diferencias entre los x_i
    df['f_0^[1]'] = df['f(x_i)'].diff().shift(-1) / df['h_i'] # Calcula la primer diferencia dividida

    # Contruye la matriz del sistema a resolver para calcular las S_i (Ax = b)
    A = np.zeros((n - 1, n + 1))
    for i in range(0, n - 1):
        A[i][i] = df['h_i'][i]
        A[i][i + 2] = df['h_i'][i + 1]
        A[i][i + 1] = 2*(A[i][i] + A[i][i + 2])
    A = np.delete(A, [0, -1], 1) # Elimina la primer y última columna (S_0 y S_n)

    # Contruye el vector independiente
    b = np.zeros((n - 1, 1))
    for i in range(0, n - 1):
        b[i][0] = 6 * (df['f_0^[1]'][i + 1] - df['f_0^[1]'][i])

    # Resuelve el sistema y obtiene los valores S_i
    S = np.linalg.solve(A, b)
    S = np.insert(S, 0, 0)
    S = np.append(S, 0)
    df['S_i'] = S.flatten()

    # Aplica las fórmulas para los coeficientes
    df['a_i'] = df['S_i'].diff().shift(-1)/(6 * df['h_i'])
    df['b_i'] = df['S_i']/2
    df.loc[n, 'b_i'] = np.nan
    df['c_i'] = df['f_0^[1]'] - df['h_i'] * (df['S_i'].shift(-1) + 2 * df['S_i']) / 6
    df['d_i'] = df['f(x_i)']
    df.loc[n, 'd_i'] = np.nan

    return df

def splines_graficas(df, decimals=10):
    # Propuestas personal para los colores de los splines
    COLORS = ['black', 'red', 'cyan', 'limegreen', 'darkorange', 'blue', 'fuchsia', 'purple', 'deepskyblue', 'gold', 'chocolate', 'slategray', 'darkorchid', 'brown', 'lightpink', 'indigo', 'beige', 'darkcyan']

    # Configuración inicial de la gráfica
    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots(figsize=(10, 10))

    n = len(df) - 1
    for i in range(n):
        # Obtiene los coeficientes e intervalo para el indice actual
        ai = df['a_i'].iloc[i]
        bi = df['b_i'].iloc[i]
        ci = df['c_i'].iloc[i]
        di = df['d_i'].iloc[i]
        xi, xi_sig = df['x_i'].iloc[i], df['x_i'].iloc[i + 1]

        # Información para el spline
        x = np.linspace(xi, xi_sig, 100) # Dominio
        y = ai * (x - xi)**3 + bi * (x - xi)**2 + ci * (x - xi) + di # Regla de correspondencia
        ax.plot(x, y, linewidth=2.0, color=COLORS[i % len(COLORS)], label=f"g_{i}(x)") # Agrega a la gráfica

        # Redondea los valores a cierta cantidad de decimales (10 por defecto)
        (ai, bi, ci, di) = tuple(map(lambda x: np.format_float_positional(x, precision=decimals), (ai, bi, ci, di)))
        # Imprime el spline
        print(f"➤ Para x \u2208 [{xi}, {xi_sig}]")
        print(f"g_{i}(x) = {ai} * (x - ({xi}))^3 + ({bi}) * (x - ({xi}))^2 + ({ci}) * (x - ({xi})) + ({di}), {xi} <= x <= {xi_sig}")


    # Configuración final de la gráfica e impresión con todo lo cargado
    x0, xn = df['x_i'].iloc[0], df['x_i'].iloc[-1]
    ax.set(
        xlim=(np.floor(x0 - 1), np.ceil(xn + 1)),
        xticks=np.arange(np.floor(x0 - 1), np.ceil(xn + 1), 1),
        ylim=(np.floor(df['f(x_i)'].min() - 1), np.ceil(df['f(x_i)'].max() + 1)),
        yticks=np.arange(np.floor(df['f(x_i)'].min() - 1), np.ceil(df['f(x_i)'].max() + 1), 1),
        xlabel='x',
        ylabel='f(x)',
    )
    ax.set_title('Ajuste de splines cúbicos', fontsize=16)
    ax.grid(True, which='major', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.tick_params(axis='both', which='major', labelsize=12)
    # Ejes en razón 1:1
    ax.set_aspect('equal')

    # Ajuste de leyendas para evitar solapamientos
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    # Ajustar el diseño para dejar espacio para la leyenda
    plt.tight_layout()
    plt.subplots_adjust(right=0.8)  # Reducir el ancho para dejar espacio

    # Agrega los puntos a la gráfica
    ax.scatter(df['x_i'], df['f(x_i)'], s=100, zorder=5)  # s controla el tamaño

    # Guarda la gràfica como png
    plt.savefig("grafica.png", bbox_inches='tight', dpi=300)

    print("\n\u26A0\uFE0F  La gráfica de los polinomios ha sido guardada como 'grafica.png' en el mismo directorio de este programa")
    input("Presione enter para continuar...")


def menu_programa3():
    tabla = None
    ruta = None
    while True:
        limpiar_pantalla()
        caja_titulo_2("APROXIMACIÓN POLINOMIAL")

        print("1. Capturar tabla de valores")
        print("2. Mostrar resultados")
        print("3. Regresar al menú principal")
        opcion_principal = int(input("Seleccione una opción: ").strip())

        if opcion_principal == 3:
            break
        
        if opcion_principal < 1 or opcion_principal > 3:
            print("\nOpcion INVALIDA, seleccione otra opcion.")
            input("Presione enter para continuar...")
            continue
        
        if opcion_principal == 1:
            while True:
                limpiar_pantalla()
                caja_titulo_3("CAPTURA DE VALORES")
                print("¿Cómo desea capturar los datos?")
                print("1. Desde un archivo CSV")
                print("2. Desde la consola")
                print("3. Regresar al menú anterior")

                opcion_captura = int(input("Ingrese la opción de su preferencia: ").strip())

                if 1 <= opcion_captura <= 3:
                    break
                else:
                    print("\nOpcion INVALIDA, seleccione otra opcion.")
                    input("Presione enter para continuar...")

            if opcion_captura == 3:
                continue
            
            if opcion_captura == 1:
                ruta = leer_csv()
            else:
                ruta = leer_puntos()
            tabla = generar_tabla(ruta)
            continue
            
        # Opción 2
        if ruta == None:
            print("\nNo ha ingresado los valores para realizar el ajuste")
            input("Presione enter para continuar...")
            continue

        limpiar_pantalla()
        caja_titulo_3("RESULTADOS")
        print(f"[bold]OBSERVACIÓN:[/bold] Todos los valores siguientes fueron redondeados a {DECIMALES} decimales para una mejor visualización.\n")

        # Imprime la tabla de con los valores obtenidos después de realizar los cálculos
        tabla_imp = tabla.round(DECIMALES)
        tabla_imp = tabla_imp.fillna('')
        caja_titulo_4("TABLA DE SPLINE CÚBICO")
        print("[bold]OBSERVACIÓN:[/bold] En caso de no visualizar la tabla correctamente, ajuste el tamaño de su terminal o de la fuente y vuelva a intentar.")
        print(tabulate(tabla_imp, headers=SPLINE_HEADERS, tablefmt="fancy_grid"))

        # Imprime los splines (usando 4 decimales) y genera la gráfica
        print()
        caja_titulo_4("POLINOMIOS")
        print("[bold]OBSERVACIÓN:[/bold] Los polinomios fueron impresos en este formato para que puedan ser copiados y pegados fácilmente a GeoGebra y se grafiquen en el intevalo correcto.")
        splines_graficas(tabla, decimals=DECIMALES)

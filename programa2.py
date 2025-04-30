from tabulate import tabulate
from utils import *
import numpy as np
from rich import print
import copy

# Función para obtener los datos de la tabla y verificar si
def obtener_datos(registros):
  datos = []

  while True:
    x0 = float(input("⮞ Ingrese el valor de x_0: "))
    xn = float(input("⮞ Ingrese el valor de x_n: "))
    if xn <= x0:
      print("Error. El valor de x_n debe ser mayor que x_0.\n")
    else:
      break

  h = (xn - x0) / (registros - 1)

  # Se llenan los datos de la tabla
  xi = x0
  print("⮞ Ingrese los valores de f(x_i) para cada x_i")
  for i in range(registros):
    f_xi = float(input(f"  👉 x_{i} = {xi}, f(x_{i}) = "))
    datos.append([i, xi, f_xi])
    # Si la siguiente iteración es la última toma el valor de x_n para evitar error de redondeo
    if i == registros - 2:
      xi = xn
    else:
      xi += h

  return datos


# Metodo progresivo
def metodo_progresivo(tabla, x):
  n = len(tabla) - 1
  Pn = tabla[0][2]
  fac = 1
  
  s = (x - tabla[0][1]) / (tabla[1][1] - tabla[0][1])

  s_prod = 1
  for i in range(n):
    s_prod *= (s - i)
    fac *= (i + 1)
    Pn += (tabla[0][i + 3] * s_prod) / fac

  return Pn


# Metodo regresivo
def metodo_regresivo(tabla, x):
  n = len(tabla) - 1
  Pn = tabla[-1][2]
  fac = 1
  
  s = (x - tabla[-1][1]) / (tabla[1][1] - tabla[0][1])

  s_prod = 1
  for i in range(n):
    s_prod *= (s + i)
    fac *= (i + 1)
    Pn += (tabla[n - 1 - i][i + 3] * s_prod) / fac

  return Pn


# Funcion del método de Diferencias de Newton
def metodo_newton(datos, punto, grado):
  n = len(datos) - 1

  Fx = copy.deepcopy(datos)

  # Comienza el método de diferencias divididas
  for diferencia in range(1, n + 1):
    for i in range(n + 1 - diferencia):
        Fx[i].append(Fx[i + 1][-1] - Fx[i][-1])

  # Imprime la tabla de diferencias
  encabezado = ["i", "x_i", "f(x_i)", "Δ f(x_i)"]
  for i in range(2, n + 1):
    encabezado.append(f"Δ^{i} f(x_i)")

  print("[bold]TABLA DE DIFERENCIAS[/bold]")
  print(tabulate(Fx, headers=encabezado, tablefmt="grid"))

  # Resultado numerico de la interpolacion
  # Encuentra el índice del punto más cercano para determinar si usar progresivo o regresivo
  intervalo = 0
  for i in range(n):
    if punto >= Fx[i][1]:
      intervalo = i
    else:
      break
  
  # Determinar qué método usar según el grado solicitado
  max_grado_progresivo = n - intervalo
  max_grado_regresivo = intervalo + 1

  if grado <= max_grado_progresivo:
    print(f"Se usó el [bold]método progresivo[/bold] desde la fila {intervalo} hasta la fila {intervalo + grado}")
    Fx = Fx[intervalo:intervalo+grado+1]
    pn = metodo_progresivo(Fx, punto)
    print(f"✅ El resultado de interpolar el punto {punto} bajo un polinomio de grado {grado} es {pn}")
  elif grado <= max_grado_regresivo:
    print(f"Se usó el [bold]método regresivo[/bold] desde la fila {intervalo - grado + 1} hasta la fila {intervalo + 1}")
    Fx = Fx[intervalo - grado + 1:intervalo + 2]
    pn = metodo_regresivo(Fx, punto)
    print(f"✅ El resultado de interpolar el punto {punto} bajo un polinomio de grado {grado} es {pn}")
  else:
    print("⚠️ [bold]No se puedo interpolar el punto dado con los datos ingresados, ya que el grado del polinomio es mayor al número de puntos disponibles en la tabla para la ubicación del punto[/bold] ⚠️")


def menu_programa2():
  while True:
    limpiar_pantalla()
    caja_titulo_2("INTERPOLACIÓN Y AJUSTE DE CURVAS")

    ## 1. Leer la tabla de valores
    # 1.1 Solicitar número de puntos en la tabla
    while True:
        registros = int(input("⮞ Ingrese el número de puntos de la tabla: "))
        if registros <= 1:
          print("Error. Ingrese valor mayor que uno para poder realizar el método.\n")
        else:
          break
      
    # 1.2 Leer los puntos (xi,yi)
    # 1.4 Verifique que los datos sean equidistantes y que estén ordenados, sino ordenarlos. (No se implementó pero se forzo)
    tabla = obtener_datos(registros)

    # 1.3 Preguntar ¿Son correctos los datos? En caso de NO solicitar la fila del valor a corregir, en caso de SI, continuar
    print("\nLa [bold]tabla ingresada[/bold] es la siguiente:")
    print(tabulate(tabla, headers=["i", "x_i", "f(x_i)"], tablefmt="grid"))

    opcion = input("\n⮞ ¿Los datos son correctos? (S/N): ")
    while opcion.strip().lower() == "n":
        fila = int(input(f"\n⮞ Ingrese la fila del valor a corregir (en [0, {registros})): "))
        if fila < 0 or fila >= registros:
          print("Error. Ingrese fila válida.")
        else:
          tabla[fila][2] = float(input(f"⮞ Ingrese el nuevo valor para f(x_{fila}): "))
          print("\nLa [bold]tabla corregida[/bold] es:")
          print(tabulate(tabla, headers=["i", "x_i", "f(x_i)"], tablefmt="grid"))
          opcion = (input("\n⮞ ¿Los datos son correctos? (S/N): "))


    # 2. Leer datos para la interpolación
    while True:
      # 2.1 Solicitar punto a interpolar. Verifique que el punto esté dentro del intervalo de la tabla, [x_0,x_n]
      while True:
        p_interpolar = float(input("\n⮞ Ingrese el punto a interpolar: "))
        if p_interpolar < tabla[0][1] or p_interpolar > tabla[registros - 1][1]:
            print("Error. El valor ingresado NO está dentro del intervalo de la tabla.")
        else:
            break
        
      # 2.2 Leer grado del polinomio. Comprobar que los puntos de la tabla son suficientes para el grado del polinomio solicitado.
      while True:
        grado = int(input("\n⮞ Ingrese grado del polinomio: "))
        if grado <= 0:
            print("Error. Ingrese valor mayor que cero.")
        elif grado > (registros - 1):
            print("Error. Los puntos de la tabla no son suficientes para un polinomio de grado ", grado)
        else:
            break

      limpiar_pantalla()
      caja_titulo_2("INTERPOLACIÓN Y AJUSTE DE CURVAS")
      print("[bold]DATOS FINALES INGRESADOS[/bold]")
      print("1. TABLA DE VALORES")
      print(tabulate(tabla, headers=["i", "x_i", "f(x_i)"], tablefmt="grid"))
      print(f"2. PUNTO A INTERPOLAR: {p_interpolar}")
      print(f"3. GRADO DEL POLINOMIO: {grado}")


      # 3. Presentar tabla de diferencias y el resultado.
      print()
      metodo_newton(tabla, p_interpolar, grado)


      # 4. Preguntar: ¿Desea interpolar otro punto con la misma tabla? 
      op = input("\n⮞ ¿Desea interpolar otro punto con la misma tabla (S/N)? ")
      # 4.1 En caso de SI regresar a (2)
      if op.strip().lower() == "n":
        break
    
    # 4.2 En caso de NO, preguntar ¿Desea cambiar la tabla [Regresar a (1) lectura de datos] o regresar al menú principal (termina la ejecución del módulo de interpolación)?

    # Si dice que no
    op_2 = int(input("Si desea cambiar la tabla, digite '1', si desea regresar al menú principal (terminar ejecición del programa), digite cualquier otro dígito: "))
    if op_2 != 1:
        break

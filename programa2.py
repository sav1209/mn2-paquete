#Programa 2

#Imprimir tabla
def imprime_tabla(tabla):
  print("| Ren |     x      |     y      |")
  print("|-----|------------|------------|")
  for i in range(len(tabla)):
    print(f"|  {i+1}  |  {tabla[i][0]:.6f}  |  {tabla[i][1]:.6f}  |")
  return

# Función para obtener los datos de la tabla y verificar si
def obtener_datos(registros):
  datos = []
  aux = 0

  # Se leen los datos y se agregan a la "tabla"
  for i in range(registros):
    print("Ingrese datos del registro", i + 1)
    # Llenar registro
    x = float(input("x = "))
    f_x = float(input("f(x) = "))
    datos.append([x, f_x])

  # Ordena datos
  ordena = sorted(datos, key=lambda elemento: elemento[0])
  return ordena

#Funcion del método de diferencias divididas
def metodo_diferencias(a,punto,grado_pol):
  n=len(a)-1
  Fx = [[0] * (n+2) for _ in range(n+1)] #Se asigna la dimensión de la matriz Fx=Fij además almacenara los resultados de la interpolacion
  for i in range(n+1): # Las primeras dos columnas se llenan con los valores de x e f(x)=y
    Fx[i][0]= a[i][0] #Valores de x
    Fx[i][1]= a[i][1] #Valores de y=f(x)
  #Comienza el método de diferencias divididas
  for j in range(1, n + 1):
    for i in range(n - j + 1):
        Fx[i][j + 1] = ( Fx[i][j]- Fx[i + 1][j]) / (Fx[i][0] - Fx[i + j][0])
  #Se imprime Fx que es la tabla de las diferencias divididas
  print(" x\t|\ty\t|\tfi[1]\t|\tfi[2]\t|\tfi[3]\t|\tfi[4]")
  for fila in Fx:
        print('\t'.join(f'{datos:.6f}' for datos in fila))
  #Resultado numerico de la interpolacion
  Pn = Fx[0][1]
  producto = 1
  for elem in range(2, grado_pol+ 2):
    producto *= (punto - Fx[elem-2][0])
    Pn+= Fx[0][elem] * producto
  print(f"El resultado de interpolar el punto {p_interpolar} bajo un polinomio de grado {grado} es {Pn:.6f}")


while True:
  print("Integrantes del equipo:")
  print(" - Moctezuma Isidro Michelle")
  print(" - Villeda Lopez Saul")
  print(" * * * Programa 2. Interpolación polinomial * * * \n")
  ## Leer datos de la tabla
  while True:
    registros = int(input("Ingrese el número de puntos de la tabla: "))
    if registros <= 0:
      print("Error. Ingrese valor mayor que cero.\n")
    elif registros == 1:
      print("Error. Ingrese valor mayor que uno para poder realizar el método.\n")
    else:
      break
  tabla = obtener_datos(registros)
  print("\nLa tabla ingresada es la siguiente:")
  imprime_tabla(tabla)
  opcion = (input("\n¿Los datos son correctos? (S/N): "))
  while opcion.lower() == 'n':
    fila = int(input("\nIngrese la fila del valor a corregir: "))
    if fila <= 0 or fila > registros:
      print("Error. Ingrese fila válida.")
    else:
      tabla[fila - 1][0] = float(input("Ingrese nuevo valor para x: "))
      tabla[fila - 1][1] = float(input("Ingrese nuevo valor para y: "))
      # Ordena datos de nuevo
      tabla = sorted(tabla, key=lambda elemento: elemento[0])
      print("\nLa tabla es:")
      imprime_tabla(tabla)
      opcion = (input("\n¿Los datos son correctos? (S/N): "))

  ## Leer datos para la interpolación
  while True:
    while True:
      p_interpolar = float(input("\nIngrese el punto a interpolar: "))
      if p_interpolar < tabla[0][0] or p_interpolar > tabla[registros - 1][0]:
        print("Error. El valor ingresado NO está dentro del intervalo de la tabla.")
      else:
        break

    while True:
      grado = int(input("\nIngrese grado del polinomio: "))
      if grado <= 0:
        print("Error. Ingrese valor mayor que cero.")
      elif grado > (registros - 1):
        print("Error. Los puntos de la tabla no son suficientes para un polinomio de grado ", grado)
      else:
        break

    print("El punto a interpolar es ", p_interpolar, " con un polinomio de grado ", grado)

    #Función que llama al método
    metodo_diferencias(tabla,p_interpolar,grado)

    op=(input("\nQuieres interpolar otro valor con la misma tabla?(S/N)"))
    if op.lower()=='n':
      break

  # Si dice que no
  op_2 = int(input("Si desea cambiar la tabla, digite '1', si desea regresar al menú principal (terminar ejecición del programa), digite cualquier otro dígito: "))
  if op_2 == 1:
    print("\nNueva tabla\n")
  else:
    break
from programa1 import menu_programa1
from programa2 import menu_programa2
from programa3 import menu_programa3
from programa4 import menu_programa4
from utils import *
import textwrap
from rich import print
from rich.console import Console
from rich.table import Table
from rich import box


def crear_pantalla_bienvenida():
    titulo = "PAQUETE DE PROGRAMAS (PARTE 2)"
    mensaje = [
        "Asignatura: Método numéricos II",
        "Profesora: Teresa Carrillo Ramirez",
        "Integrantes: ",
        "\u29BF Moctezuma Isidro Michelle",
        "\u29BF Villeda Lopez Saul"
    ]

    caja = Table(box=box.DOUBLE, expand=True)

    titulo_decorado = f":glowing_star: {titulo} 🚀"
    caja.add_column(titulo_decorado, justify="center")

    pie = f"\n:fire: Presiona Enter para comenzar ⚡"
    caja.add_row("\n" + "\n".join(mensaje + [pie]))

    Console().print(caja)
    
    # Esperar entrada del usuario
    input()

# Ejecutar la aplicación
if __name__ == "__main__":
    # Crear pantalla de bienvenida
    crear_pantalla_bienvenida()

    # Ejecutar el menú principal
    while(True):
        limpiar_pantalla()
        caja_titulo_1("MENU PRINCIPAL")
        print("1. Solucion de sistemas de ecuaciones no lineales (Broyden)")
        print("2. Interpolación y ajuste de curvas")
        print("3. Aproximación polinomial")
        print("4. Integración numérica")
        print("5. Salir")
        opcion = int(input("Seleccione una opcion: "))
        
        if opcion == 1:
            menu_programa1()
        elif opcion == 2:
            menu_programa2()
        elif opcion == 3:
            menu_programa3()
        elif opcion == 4:
            menu_programa4()
        elif opcion == 5:
            print("🫶 Adios, vuelva pronto 🫰")
            break
        else:
            print("Opcion INVALIDA, seleccione otra opcion.")

from programa1 import menu_programa1
from utils import *
import textwrap


def crear_pantalla_bienvenida(titulo, mensaje_multilinea):
    """
    Crea una pantalla de bienvenida personalizable con múltiples líneas.

    :param titulo: Título principal de la pantalla
    :param mensaje_multilinea: Lista de líneas de mensaje
    """
    # Iconos por defecto si no se proporcionan
    iconos = {
        "cohete": "🚀",
        "estrella": "✨", 
        "rayo": "⚡", 
        "fuego": "🔥"
    }

    # Ancho de la pantalla
    ancho = 70

    # Líneas de decoración
    linea_superior = "╔" + "═" * ancho + "╗"
    linea_intermedia = "║" + " " * ancho + "║"
    linea_inferior = "╚" + "═" * ancho + "╝"

    # Imprimir marco superior
    print(linea_superior)
    print(linea_intermedia)

    # Título centrado con iconos
    titulo_decorado = f"{iconos['estrella']} {titulo} {iconos['cohete']}"
    print(f"║{titulo_decorado:^{ancho}}║")

    print(linea_intermedia)

    # Imprimir mensaje multilínea
    for linea in mensaje_multilinea:
        # Ajustar líneas largas
        lineas_ajustadas = textwrap.wrap(linea, width=ancho-4)
        for linea_ajustada in lineas_ajustadas:
            print(f"║ {linea_ajustada:<{ancho-2}}║")

    print(linea_intermedia)

    # Pie de página
    pie = f"{iconos['fuego']} Presiona Enter para comenzar {iconos['rayo']}"
    print(f"║{pie:^{ancho}}║")

    print(linea_intermedia)
    print(linea_inferior)

    # Esperar entrada del usuario
    input()

# Ejecutar la aplicación
if __name__ == "__main__":
    # Mensaje de bienvenida con múltiples líneas
    mensaje_bienvenida = [
        "Asignatura: Método numéricos II",
        "Profesora: Teresa Carrillo Ramirez",
        "Integrantes: ",
        "\u29BF Moctezuma Isidro Michelle",
        "\u29BF Villeda Lopez Saul"
    ]

    # Crear pantalla de bienvenida
    crear_pantalla_bienvenida(
        "PAQUETE DE PROGRAMAS (PARTE 1)", 
        mensaje_bienvenida
    )

    # Ejecutar el menú principal
    while(True):
        limpiar_pantalla()
        caja_titulo_1("MENU PRINCIPAL")
        print("1. Solucion de sistemas de ecuaciones no lineales (Broyden)")
        print("2. Salir")
        opcion = int(input("Seleccione una opcion: "))
        
        if opcion == 1:
            menu_programa1()
        elif opcion == 2:
            print("Adios, vuelva pronto")
            break
        else:
            print("Opcion INVALIDA, seleccione otra opcion.")

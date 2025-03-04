from programa1 import menu_programa1
import time
import sys

def portada():
    
    print("MÉTODOS NUMÉRICOS II")
    print("°*°*°PROGRAMA 1 (Metodo de Broyden)°*°*°")
    print("Profesora: Teresa Carrillo Ramirez")
    print("Integrantes: ")
    print("- Moctezuma Isidro Michelle")
    print("- Villeda Lopez Saul")
    input("Presione Enter para ver el menu principal...\n")

import time
import sys
import textwrap

def imprimir_lento(texto, velocidad=0.03):
    """Imprime texto letra por letra para efecto dramático."""
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()
        time.sleep(velocidad)
    print()

def crear_pantalla_bienvenida(titulo, mensaje_multilinea, iconos=None):
    """
    Crea una pantalla de bienvenida personalizable con múltiples líneas.

    :param titulo: Título principal de la pantalla
    :param mensaje_multilinea: Lista de líneas de mensaje
    :param iconos: Diccionario de iconos personalizados (opcional)
    """
    # Iconos por defecto si no se proporcionan
    if iconos is None:
        iconos = {
            "cohete": "🚀",
            "estrella": "✨", 
            "rayo": "⚡", 
            "fuego": "🔥"
        }

    # Ancho de la pantalla
    ancho = 70

    # Limpiar pantalla
    print("\033[H\033[J", end="")

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

    # Personalizar iconos (opcional)
    iconos_personalizados = {
        "cohete": "🌟",
        "estrella": "💡", 
        "rayo": "🔧", 
        "fuego": "📊"
    }

    # Crear pantalla de bienvenida
    crear_pantalla_bienvenida(
        "PAQUETE DE PROGRAMAS (PARTE 1)", 
        mensaje_bienvenida,
        iconos_personalizados
    )

    
    # Ejecutar el menú principal
    while(True):
        print("MENU PRINCIPAL")
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

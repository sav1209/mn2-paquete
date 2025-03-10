import platform
from tabulate import tabulate
import os

def limpiar_pantalla():
    """
    Limpia la pantalla de forma multiplataforma.
    Funciona en Windows, Linux y macOS.
    """
    # Detecta el sistema operativo
    sistema = platform.system()
    
    # Comando para limpiar pantalla según el sistema
    if sistema == 'Windows':
        os.system('cls')
    else:  # Para Unix/Linux/macOS
        os.system('clear')

def caja_titulo_1(texto):
    print(tabulate([[texto]], tablefmt="double_outline"))

def caja_titulo_2(texto):
    print(tabulate([[texto]], tablefmt="heavy_grid"))

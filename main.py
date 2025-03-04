from programa1 import menu_programa1

def portada():
    print("MÉTODOS NUMÉRICOS II")
    print("°*°*°PROGRAMA 1 (Metodo de Broyden)°*°*°")
    print("Profesora: Teresa Carrillo Ramirez")
    print("Integrantes: ")
    print("- Moctezuma Isidro Michelle")
    print("- Villeda Lopez Saul")
    input("Presione Enter para ver el menu principal...\n")




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
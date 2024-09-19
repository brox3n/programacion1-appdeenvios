#Función que será utilizada para arrancar el programa
####IMPORTS
import os 

##FUNCIONES

def nombresparticipantes():
    print("Bienvenido a nuestra app de envíos!!!!!!")
    print("----------------------------------------------------")
    print("los creadores de esta app son los siguientes: ")
    print("----------------------------------------------------")
    print("* Bruno Forastiero")
    print("----------------------------------------------------")
    print("* Matías Laino")
    print("----------------------------------------------------")
    print("* Santiago Peralta")
    print("----------------------------------------------------")
    print("* Francisco Pettis")
    print("----------------------------------------------------")
    print("* Pedro Marzano")
    print("----------------------------------------------------")
    print("Espero que disfrutes mucho la app!!")
    print("----------------------------------------------------")
    input()

def descripcion():
    print("----------------------------------------------------")
    print("Esta es una app de envios realizada por estudiantes de  la carrera licenciatura en gestion de la Tecnología de la información. La cual es capaz de realizar la gestion de envíos y pedidos entre los usuarios y los comercios gastronómicos. Esperamos que esta app sea de su agrado y pueda disfrutarla al máximo!!")
    print("----------------------------------------------------")
    input()

def menu():
    repetir=True
    while repetir:
        os.system("cls")
        print("1 - Equipo")
        print("2 - Descripción del proyecto")
        print("3 - Ejecutar")
        print("4 - Salir")
        try:
            activar=int(input("Ingrese un número: "))
        
            if activar==1: 
                nombresparticipantes()
            elif activar==2: 
                descripcion()
            elif activar==3:
                def ejecutar():
                    pass
            elif activar==4:
                repetir==False
            else:
                print("Número Erroneo ")
                input()
        except:
            print("error ")
            input()

def ejecutar():
    envios = []

    def crear_envio():
        destino = input("Ingrese el destino del envío: ")
        peso = float(input("Ingrese el peso del envío (en kg): "))
        fecha = input("Ingrese la fecha del envío (YYYY-MM-DD): ")
        
        nuevo_envio = {
            'id': len(envios) + 1,  
            'destino': destino,
            'peso': peso,
            'fecha': fecha
        }
        envios.append(nuevo_envio)  
        print(f"Envío creado: {nuevo_envio}")

    def obtener_envios():
        if envios:
            for envio in envios:
                print(envio)
        else:
            print("No hay envíos registrados")


    def obtener_envio_por_id():
        id_envio = int(input("Ingrese el ID del envío que desea buscar: "))
        for envio in envios:
            if envio['id'] == id_envio:
                print(envio)
                return
        print("Envío no encontrado")

    def actualizar_envio():
        id_envio = int(input("Ingrese el ID del envío que desea actualizar: "))
        for envio in envios:
            if envio['id'] == id_envio:
                nuevo_destino = input("Ingrese el nuevo destino del envío: ")
                nuevo_peso = float(input("Ingrese el nuevo peso del envío (en kg): "))
                nueva_fecha = input("Ingrese la nueva fecha del envío (YYYY-MM-DD): ")
                
                envio['destino'] = nuevo_destino
                envio['peso'] = nuevo_peso
                envio['fecha'] = nueva_fecha
                print(f"Envío actualizado: {envio}")
                return
        print("Envío no encontrado")

    def eliminar_envio():
        id_envio = int(input("Ingrese el ID del envío que desea eliminar: "))
        for envio in envios:
            if envio['id'] == id_envio:
                envios.remove(envio)
                print(f"Envío con ID {id_envio} eliminado")
                return
        print(f"No se encontró ningún envío con ID {id_envio}")

    def menu():
        activo = True  
        while activo:
            os.system("cls")  
            print("\n=== Sistema de Gestión de Envíos ===")
            print("1. Crear un nuevo envío")
            print("2. Ver todos los envíos")
            print("3. Buscar un envío por ID")
            print("4. Actualizar un envío por ID")
            print("5. Eliminar un envío por ID")
            print("6. Salir")
            
            opcion = input("Seleccione una opción (1-6): ")
            
            if opcion == '1':
                crear_envio()
            elif opcion == '2':
                obtener_envios()
            elif opcion == '3':
                obtener_envio_por_id()
            elif opcion == '4':
                actualizar_envio()
            elif opcion == '5':
                eliminar_envio()
            elif opcion == '6':
                print("Saliendo del programa...")
                activo = False  
            else:
                print("Opción no válida. Inténtelo de nuevo.")
            input() 


    menu()

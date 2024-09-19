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



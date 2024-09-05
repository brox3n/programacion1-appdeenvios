#Función que será utilizada para arrancar el programa
####IMPORTS
import os 
import modulo_funciones as f 

##FUNCIONES

def nombresparticipantes():
    print("bienvenido a nuestra app de envios!!!!!!")
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
    print("Esta es una app de envios realizada por estudiantes de  la carrera licenciatura en gestion de la tecnologia de la informacion. la cual es capaz de realizar la gestion de envios y pedidos entre los usuarios y los comercios gastronomicos. Esperamos que esta app sea de su agrado y pueda disfrutarla al maximo!!")
    print("----------------------------------------------------")
    input()

def menu():
    repetir=True
    while repetir:
        os.system("cls")
        print("1 - equipo")
        print("2 - descripcion del proyecto")
        print("3 - ejecutar")
        print("4 - salir")
        try:
            activar=int(input("ingrese un numero: "))
        
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
                print("numero erroneo ")
                input()
        except:
            print("error ")
            input()


#### PROGRAMA PRINCIPAL
def main():
    menu()
    nombresparticipantes()   





if __name__=="__main__":
    main()

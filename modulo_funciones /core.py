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


def menu():
    repetir=True
    while repetir:
        os.system("cls")
        print("1 - equipo")
        print("2 - sistemas")
        print("3 - ejecutar")
        print("4 - salir")
        try:
            activar=int(input("ingrese un numero: "))
        
            if activar==1: 
                nombresparticipantes()
            elif activar==2: 
                def mostrardescripcion():
                    pass
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

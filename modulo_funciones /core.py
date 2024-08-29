#Función que será utilizada para arrancar el programa

import os 
import modulo_funciones as f 

def main():
    pass



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
                def mostrarequipo():
                    pass
            elif activar==2: 
                def mostrarsistema():
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

    
    if __name__=="__main__":
    main()

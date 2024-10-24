import json
import os
import datetime

CLAVE_ADMIN_PREDEFINIDA = "supersecret123"


ROJO = '\033[91m'
VERDE = '\033[92m'
AMARILLO = '\033[93m'
AZUL = '\033[94m'
BLANCO = '\033[97m'
RESET = '\033[0m'

def cargarUsuarios():
    try:
        with open("usuarios.json", "r") as archivo:
            datos = json.load(archivo)
            return datos["usuarios"]
    except FileNotFoundError:
        return []

def guardarUsuarios(usuarios):
    with open("usuarios.json", "w") as archivo:
        json.dump({"usuarios": usuarios}, archivo, indent=4)

def registrarUsuario():
    usuarios = cargarUsuarios()
    
    nombre = input(f"{AZUL}Introduce el nombre de usuario: {RESET}")
    
    for u in usuarios:
        if u["nombre"] == nombre:
            print(f"{ROJO}El nombre de usuario ya existe. Elige otro.{RESET}")
            input()
            return None  
    
    password = input(f"{AZUL}Introduce la contraseña: {RESET}")
    rol = input(f"{AZUL}¿Quieres ser 'admin' o 'cliente'? {RESET}").lower()
    
    if rol == "admin":
        claveAdmin = input(f"{AZUL}Introduce la clave de administrador: {RESET}")
        if claveAdmin != CLAVE_ADMIN_PREDEFINIDA:
            print(f"{ROJO}Clave de administrador incorrecta. Registro fallido.{RESET}")
            input()
            return None  

    nuevoUsuario = {
        "nombre": nombre,
        "password": password,
        "rol": rol
    }
    usuarios.append(nuevoUsuario)
    guardarUsuarios(usuarios)
    print(f"{VERDE}Registro exitoso. Te has registrado como {rol}.{RESET}")
    input()
    return nuevoUsuario


def login():
    usuarios = cargarUsuarios()
    
    usuario = input(f"{AZUL}Nombre de usuario: {RESET}")
    password = input(f"{AZUL}Contraseña: {RESET}")
    
    for u in usuarios:
        if u["nombre"] == usuario and u["password"] == password:
            return u 
    print(f"{ROJO}Usuario o contraseña incorrectos.{RESET}")
    return None  

def mostrarOpciones(usuario):
    if usuario["rol"] == "admin":
        print(f"{AMARILLO}Bienvenido administrador. Puedes gestionar todos los envíos.{RESET}")
        input()
    elif usuario["rol"] == "cliente":
        print(f"{VERDE}Bienvenido {usuario['nombre']}. Puedes gestionar tus envíos.{RESET}")
        input()

def cargarEnviosDesdeArchivo():
    envios = []
    try:
        with open("registro_envios.txt", "r") as archivo:
            for linea in archivo:
                idEnvio, destino, peso, fecha = linea.strip().split(',')
                envios.append({
                    'id': int(idEnvio),
                    'destino': destino,
                    'peso': float(peso),
                    'fecha': fecha
                })
    except FileNotFoundError:
        pass  
    return envios

def guardarEnArchivo(envios):
    with open("registro_envios.txt", "w") as archivo:
        for envio in envios:
            archivo.write(f"{envio['id']},{envio['destino']},{envio['peso']},{envio['fecha']}\n")

def ejecutar(usuario):
    envios = cargarEnviosDesdeArchivo()  

    def crearEnvio():
        destino = input("Ingrese el destino del envío: ")

        
        pesoValido = False
        while not pesoValido:
            try:
                peso = float(input("Ingrese el peso del envío (en kg, máximo 25 kg): "))
                if 0 < peso <= 25:
                    pesoValido = True
                else:
                    print("El peso debe ser mayor a 0 y menor o igual a 25 kg.")
            except ValueError:
                print("Por favor, ingrese un número válido para el peso.")

        
        fechaValida = False
        while not fechaValida:
            fecha = input("Ingrese la fecha del envío (YYYY-MM-DD): ")
            partes = fecha.split('-')
            
            if len(partes) == 3 and partes[0].isdigit() and partes[1].isdigit() and partes[2].isdigit():

                anio = int(partes[0])
                mes = int(partes[1])
                dia = int(partes[2])

                
                anioActual =  datetime.date.today().year
                mesActual =  datetime.date.today().month
                diaActual =  datetime.date.today().day

                
                if anio >= anioActual:
                    
                    if 1 <= mes <= 12:
                        
                        if mes in [1, 3, 5, 7, 8, 10, 12]:
                            max_dias = 31
                        elif mes in [4, 6, 9, 11]:
                            max_dias = 30
                        elif mes == 2:
                            
                            if (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0):
                                max_dias = 29
                            else:
                                max_dias = 28
                        
                        
                        if 1 <= dia <= max_dias:
                            
                            if anio > anioActual or (anio == anioActual and (mes > mesActual or (mes == mesActual and dia >= diaActual))):
                                fechaValida = True
                            else:
                                print("Ingrese una fecha válida.")
                        else:
                            print(f"El mes {mes} no tiene {dia} días.")
                    else:
                        print("El mes debe estar entre 1 y 12.")
                else:
                    print("El año debe ser 2024 o posterior.")
            else:
                print("Formato de fecha incorrecto. Use YYYY-MM-DD.")

        nuevoEnvio = {
            'id': len(envios) + 1,
            'destino': destino,
            'peso': peso,
            'fecha': fecha
        }
        envios.append(nuevoEnvio)
        print(f"Envío creado: {nuevoEnvio}")
        guardarEnArchivo(envios)


    def obtenerEnvios():
        if envios:
            for envio in envios:
                print(f"{AMARILLO}{envio}{RESET}")
        else:
            print(f"{AMARILLO}No hay envíos registrados{RESET}")

    def obtenerEnvioPorId():
        idEnvio = int(input(f"{AZUL}Ingrese el ID del envío que desea buscar: {RESET}"))
        for envio in envios:
            if envio['id'] == idEnvio:
                print(f"{AMARILLO}{envio}{RESET}")
                return
        print(f"{ROJO}Envío no encontrado{RESET}")


    def actualizarEnvio():
        idEnvio = int(input(f"{AZUL}Ingrese el ID del envío que desea actualizar: {RESET}"))
        for envio in envios:
            if envio['id'] == idEnvio:
                nuevoDestino = input(f"{AZUL}Ingrese el nuevo destino del envío: {RESET}")
                nuevoPeso = float(input(f"{AZUL}Ingrese el nuevo peso del envío (en kg): {RESET}"))
                nuevaFecha = input(f"{AZUL}Ingrese la nueva fecha del envío (YYYY-MM-DD): {RESET}")
                
                envio['destino'] = nuevoDestino
                envio['peso'] = nuevoPeso
                envio['fecha'] = nuevaFecha
                print(f"{VERDE}Envío actualizado: {envio}{RESET}")
                guardarEnArchivo(envios)  
                return
        print(f"{ROJO}Envío no encontrado{RESET}")

    def eliminarEnvio():
        idEnvio = int(input(f"{AZUL}Ingrese el ID del envío que desea eliminar: {RESET}"))
        for envio in envios:
            if envio['id'] == idEnvio:
                envios.remove(envio)
                print(f"{ROJO}Envío con ID {idEnvio} eliminado{RESET}")
                guardarEnArchivo(envios)  
                return
        print(f"{ROJO}No se encontró ningún envío con ID {idEnvio}{RESET}")

    def menuEnvios():
        activo = True
        while activo:
            os.system("clear")  # os.system("clear") para mac
            print(f"\n{BLANCO}=== Sistema de Gestión de Envíos ==={RESET}")
            print(f"{AZUL}1. Crear un nuevo envío{RESET}")
            if usuario["rol"] == "admin":
                print(f"{AZUL}2. Ver todos los envíos{RESET}")
            print(f"{AZUL}3. Buscar un envío por ID{RESET}")
            print(f"{AZUL}4. Actualizar un envío por ID{RESET}")
            print(f"{AZUL}5. Eliminar un envío por ID{RESET}")
            print(f"{ROJO}6. Salir{RESET}")
            
            opcion = input(f"{AZUL}Seleccione una opción (1-6): {RESET}")
            
            if opcion == '1':
                crearEnvio()
            elif opcion == '2' and usuario["rol"] == "admin":
                obtenerEnvios()
            elif opcion == '3':
                obtenerEnvioPorId()
            elif opcion == '4':
                actualizarEnvio()
            elif opcion == '5':
                eliminarEnvio()
            elif opcion == '6':
                print(f"{AMARILLO}Saliendo del programa...{RESET}")
                activo = False
            else:
                print(f"{ROJO}Opción no válida o sin permisos. Inténtelo de nuevo.{RESET}")
            input()

    menuEnvios()

def menu():
    repetir = True
    while repetir:
        os.system("clear")  # os.system("clear") para mac
        print(f"{BLANCO}1 - Equipo{RESET}")
        print(f"{BLANCO}2 - Descripción del proyecto{RESET}")
        print(f"{BLANCO}3 - Ejecutar{RESET}")
        print(f"{ROJO}4 - Salir{RESET}")
        try:
            activar = int(input(f"{AZUL}Ingrese un número: {RESET}"))
        
            if activar == 1: 
                nombresparticipantes()
            elif activar == 2: 
                descripcion()
            elif activar == 3:
                opcionSesion = input(f"\n{AZUL}Elija una opción:\n1. Registrarse\n2. Iniciar sesión\nSeleccione (1-2): {RESET}")
                
                if opcionSesion == "1":
                    usuarioRegistrado = registrarUsuario()
                    if usuarioRegistrado:
                        mostrarOpciones(usuarioRegistrado)
                        ejecutar(usuarioRegistrado)
                elif opcionSesion == "2":
                    usuarioLogeado = login()
                    if usuarioLogeado:
                        mostrarOpciones(usuarioLogeado)
                        ejecutar(usuarioLogeado)
                    else:
                        print(f"{ROJO}Error al iniciar sesión.{RESET}")
                        input()
                else:
                    print(f"{ROJO}Opción inválida.{RESET}")
                    input()
            elif activar == 4:
                repetir = False 
            else:
                print(f"{ROJO}Número Erróneo{RESET}")
                input()
        except:
            print(f"{ROJO}Error{RESET}")
            input()

def nombresparticipantes():
    print("----------------------------------------------------")
    print("los creadores de esta app son los siguientes: ")
    print("----------------------------------------------------")
    print("* Bruno Forastiero")
    print("* Santiago Peralta")
    print("* Francisco Pettis")
    print("* Pedro Marzano")
    print("----------------------------------------------------")
    input()

def descripcion():
    print("----------------------------------------------------")
    print("Esta es una app de envíos realizada por estudiantes de la UADE.")
    print("La app permite gestionar el envío de paquetes, y llevar un control de todos los registros de envíos realizados.")
    print("Incluye funcionalidades para crear, buscar, modificar y eliminar envíos.")
    print("----------------------------------------------------")
    input()

if __name__ == "__main__":
    menu()

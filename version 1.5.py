

import json
import os

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
            return None  
    
    password = input(f"{AZUL}Introduce la contraseña: {RESET}")
    rol = input(f"{AZUL}¿Quieres ser 'admin' o 'cliente'? {RESET}").lower()
    
    if rol == "admin":
        claveAdmin = input(f"{AZUL}Introduce la clave de administrador: {RESET}")
        if claveAdmin != CLAVE_ADMIN_PREDEFINIDA:
            print(f"{ROJO}Clave de administrador incorrecta. Registro fallido.{RESET}")
            return None  

    nuevoUsuario = {
        "nombre": nombre,
        "password": password,
        "rol": rol
    }
    usuarios.append(nuevoUsuario)
    guardarUsuarios(usuarios)
    print(f"{VERDE}Registro exitoso. Te has registrado como {rol}.{RESET}")
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
    elif usuario["rol"] == "cliente":
        print(f"{VERDE}Bienvenido {usuario['nombre']}. Puedes gestionar tus envíos.{RESET}")

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
        destino = input(f"{AZUL}Ingrese el destino del envío: {RESET}")
        peso = float(input(f"{AZUL}Ingrese el peso del envío (en kg): {RESET}"))
        fecha = input(f"{AZUL}Ingrese la fecha del envío (YYYY-MM-DD): {RESET}")
        
        nuevoEnvio = {
            'id': len(envios) + 1,
            'destino': destino,
            'peso': peso,
            'fecha': fecha
        }
        envios.append(nuevoEnvio)
        print(f"{VERDE}Envío creado: {nuevoEnvio}{RESET}")
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
                else:
                    print(f"{ROJO}Opción inválida.{RESET}")
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
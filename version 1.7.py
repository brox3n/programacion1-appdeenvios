import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import datetime

CLAVE_ADMIN_PREDEFINIDA = "supersecret123"


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
    nombre = simpledialog.askstring("Registro", "Introduce el nombre de usuario:")
    if not nombre:
        return
    
    usuarios = cargarUsuarios()
    for u in usuarios:
        if u["nombre"] == nombre:
            messagebox.showerror("Error", "El nombre de usuario ya existe.")
            return
    
    password = simpledialog.askstring("Registro", "Introduce la contraseña:", show="*")
    
    
    rol = None
    while rol not in ["admin", "cliente"]:
        rol = simpledialog.askstring("Registro", "¿Quieres ser 'admin' o 'cliente'?").lower()
        if rol not in ["admin", "cliente"]:
            messagebox.showerror("Error", "Rol no válido. Por favor, ingresa 'admin' o 'cliente'.")

    
    if rol == "admin":
        claveAdmin = simpledialog.askstring("Registro", "Introduce la clave de administrador:", show="*")
        if claveAdmin != CLAVE_ADMIN_PREDEFINIDA:
            messagebox.showerror("Error", "Clave de administrador incorrecta.")
            return

    nuevoUsuario = {
        "nombre": nombre,
        "password": password,
        "rol": rol,
        "envios": []  
    }
    usuarios.append(nuevoUsuario)
    guardarUsuarios(usuarios)
    messagebox.showinfo("Éxito", f"Te has registrado como {rol}.")
    
def login():
    global usuario_actual
    nombre = simpledialog.askstring("Login", "Introduce el nombre de usuario:")
    password = simpledialog.askstring("Login", "Introduce la contraseña:", show="*")
    
    usuarios = cargarUsuarios()
    for u in usuarios:
        if u["nombre"] == nombre and u["password"] == password:
            usuario_actual = u  
            messagebox.showinfo("Bienvenido", f"Iniciaste sesión como {u['rol']}.")
            ventana_bienvenida.destroy()  
            mostrarVentanaPrincipal()
            return
    messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

def crearEnvio():
    destino = 0
    while destino not in range(1, 16):
        try:
            destino = int(simpledialog.askstring("Destino", "¿A qué comuna desea enviar el paquete?"))
            if destino not in range(1, 16):
                messagebox.showerror("Error", "Comuna no válida")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido")
    
    if not destino:
        return
    try:
        peso = float(simpledialog.askstring("Nuevo Envío", "Ingrese el peso en kg (máximo 25 kg):"))
        if peso <= 0 or peso > 25:
            messagebox.showerror("Error", "El peso debe ser mayor a 0 y máximo 25 kg.")
            return
    except ValueError:
        messagebox.showerror("Error", "Peso inválido.")
        return
    
    fecha = simpledialog.askstring("Nuevo Envío", "Ingrese la fecha (YYYY-MM-DD):")
    if not validarFecha(fecha):
        messagebox.showerror("Error", "Formato de fecha inválido. Usa YYYY-MM-DD.")
        return
    
    nuevoEnvio = {
        'id': len(usuario_actual['envios']) + 1,
        'destino': destino,
        'peso': peso,
        'fecha': fecha
    }
    
    usuario_actual['envios'].append(nuevoEnvio)  
    
    
    usuarios = cargarUsuarios()
    for u in usuarios:
        if u["nombre"] == usuario_actual["nombre"]:
            u["envios"] = usuario_actual["envios"]
    guardarUsuarios(usuarios)
    
    messagebox.showinfo("Éxito", f"Envío a comuna {destino} creado correctamente.")

def verEnvios():
    if usuario_actual is None:
        messagebox.showerror("Error", "Debes iniciar sesión para ver los envíos.")
        return

    usuarios = cargarUsuarios()
    if usuario_actual["rol"] == "admin":
        envios_text = ""
        for usuario in usuarios:
            envios_text += f"Usuario: {usuario['nombre']}\n"
            if "envios" in usuario and usuario["envios"]:
                envios_text += "\n".join(
                    [f"  ID: {envio['id']}, Destino: {envio['destino']}, Peso: {envio['peso']}kg, Fecha: {envio['fecha']}"
                     for envio in usuario["envios"]]
                )
            else:
                envios_text += "  No tiene envíos registrados.\n"
            envios_text += "\n"
        messagebox.showinfo("Lista de Envíos (Admin)", envios_text)
    else:
        '''''
        Si es cliente, muestra solo sus propios envíos
        '''''
        if usuario_actual.get("envios"):
            envios_text = "\n".join(
                [f"ID: {envio['id']}, Destino: {envio['destino']}, Peso: {envio['peso']}kg, Fecha: {envio['fecha']}"
                 for envio in usuario_actual["envios"]]
            )
            messagebox.showinfo("Tus Envíos", envios_text)
        else:
            messagebox.showinfo("Tus Envíos", "No tienes envíos registrados.")


def eliminarEnvio():
    if usuario_actual is None or usuario_actual["rol"] != "admin":
        messagebox.showerror("Acceso Denegado", "Solo los administradores pueden eliminar envíos.")
        return

    try:
        usuarios = cargarUsuarios()
        idEnvio = int(simpledialog.askstring("Eliminar Envío", "Ingrese el ID del envío a eliminar:"))

        
        envio_encontrado = False
        for usuario in usuarios:
            if "envios" in usuario:
                envio = next((envio for envio in usuario["envios"] if envio['id'] == idEnvio), None)
                if envio:
                    usuario["envios"].remove(envio)
                    envio_encontrado = True

        if envio_encontrado:
            guardarUsuarios(usuarios)
            messagebox.showinfo("Eliminación", f"Envío(s) con ID {idEnvio} eliminado(s).")
        else:
            messagebox.showerror("Error", "Envío no encontrado.")
    except ValueError:
        messagebox.showerror("Error", "ID inválido.")

def validarFecha(fecha):
    try:
        fecha_ingresada = datetime.datetime.strptime(fecha, "%Y-%m-%d")
        hoy = datetime.datetime.today()
        if fecha_ingresada >= hoy:
            return True
        else:
            messagebox.showerror("Error", "La fecha debe ser la de hoy o una fecha futura.")
            return False
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha inválido. Usa el formato YYYY-MM-DD.")
        return False

def mostrarVentanaPrincipal():
    app = tk.Tk()
    app.title("App de Envíos")
    app.geometry("400x400")

    tk.Button(app, text="Crear Envío", command=crearEnvio, width=30).pack(pady=5)
    tk.Button(app, text="Ver Envíos", command=verEnvios, width=30).pack(pady=5)
    if usuario_actual["rol"] == "admin":
        tk.Button(app, text="Eliminar Envío", command=eliminarEnvio, width=30).pack(pady=5)
    tk.Button(app, text="Ver Equipo", command=mostrarEquipo, width=30).pack(pady=5)
    tk.Button(app, text="Descripción del Proyecto", command=descripcionProyecto, width=30).pack(pady=5)

    app.mainloop()

def mostrarVentanaBienvenida():
    global ventana_bienvenida
    ventana_bienvenida = tk.Tk()
    ventana_bienvenida.title("Bienvenido")
    ventana_bienvenida.geometry("300x200")

    tk.Label(ventana_bienvenida, text="Bienvenido a la App de Envíos", font=("Arial", 14)).pack(pady=10)
    tk.Button(ventana_bienvenida, text="Registrar Usuario", command=registrarUsuario, width=25).pack(pady=5)
    tk.Button(ventana_bienvenida, text="Iniciar Sesión", command=login, width=25).pack(pady=5)

    ventana_bienvenida.mainloop()

def mostrarEquipo():
    equipo = "Bruno Forastiero\nSantiago Peralta\nFrancisco Pettis\nPedro Marzano"
    messagebox.showinfo("Equipo", equipo)

def descripcionProyecto():
    descripcion = ("Esta es una app de envíos realizada por estudiantes de la UADE.\n"
                   "Permite gestionar el envío de paquetes y controlar los registros de envíos.")
    messagebox.showinfo("Descripción del Proyecto", descripcion)

envios = []
usuario_actual = None

mostrarVentanaBienvenida()

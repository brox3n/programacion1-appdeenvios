import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import datetime

CLAVE_ADMIN_PREDEFINIDA = "supersecret123"
COSTO_POR_COMUNA = 100  


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

    comuna = 0
    while comuna not in range(1, 16): 
        try:
            comuna = int(simpledialog.askstring("Registro", "Introduce tu número de comuna (1-15):"))
            if comuna not in range(1, 16):
                messagebox.showerror("Error", "Comuna no válida")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido para la comuna")

    nuevoUsuario = {
        "nombre": nombre,
        "password": password,
        "rol": rol,
        "comuna": comuna,
        "envios": []
    }
    usuarios.append(nuevoUsuario)
    guardarUsuarios(usuarios)
    messagebox.showinfo("Éxito", f"Te has registrado como {rol} en la comuna {comuna}.")


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


def calcularCostoEnvio(origen, destino, peso, costo=0):
    
    costo_por_kg = 10 
    distancia_costo = abs(origen - destino) * COSTO_POR_COMUNA  
    
    
    costo_total = distancia_costo + (peso * costo_por_kg)
    return costo_total


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

    comuna_origen = usuario_actual["comuna"]
    costo_envio = calcularCostoEnvio(comuna_origen, destino, peso)

    nuevoEnvio = {
        'id': len(usuario_actual['envios']) + 1,
        'origen': comuna_origen,
        'destino': destino,
        'peso': peso,
        'fecha': fecha,
        'costo': costo_envio
    }

    usuario_actual['envios'].append(nuevoEnvio)

    usuarios = cargarUsuarios()
    for u in usuarios:
        if u["nombre"] == usuario_actual["nombre"]:
            u["envios"] = usuario_actual["envios"]
    guardarUsuarios(usuarios)

    messagebox.showinfo("Éxito", f"Envío a comuna {destino} creado correctamente. Costo del envío: ${costo_envio}")


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
                    [f"  ID: {envio['id']}, Origen: {envio['origen']}, Destino: {envio['destino']}, "
                     f"Peso: {envio['peso']}kg, Fecha: {envio['fecha']}, Costo: ${envio['costo']}"
                     for envio in usuario["envios"]]
                )
            else:
                envios_text += "  No tiene envíos registrados.\n"
            envios_text += "\n"
        messagebox.showinfo("Lista de Envíos (Admin)", envios_text)
    else:
        if usuario_actual.get("envios"):
            envios_text = "\n".join(
                [f"ID: {envio['id']}, Origen: {envio['origen']}, Destino: {envio['destino']}, "
                 f"Peso: {envio['peso']}kg, Fecha: {envio['fecha']}, Costo: ${envio['costo']}"
                 for envio in usuario_actual["envios"]]
            )
            messagebox.showinfo("Tus Envíos", envios_text)
        else:
            messagebox.showinfo("Tus Envíos", "No tienes envíos registrados.")


def modificarUsuario():
    nueva_comuna = 0
    while nueva_comuna not in range(1, 16):  
        try:
            nueva_comuna = int(simpledialog.askstring("Modificar Comuna", "Ingrese su nueva comuna (1-15):"))
            if nueva_comuna not in range(1, 16):
                messagebox.showerror("Error", "Comuna no válida")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido para la comuna")

    usuario_actual["comuna"] = nueva_comuna
    usuarios = cargarUsuarios()
    for u in usuarios:
        if u["nombre"] == usuario_actual["nombre"]:
            u["comuna"] = nueva_comuna
    guardarUsuarios(usuarios)
    messagebox.showinfo("Modificación", "Comuna actualizada correctamente.")


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
            messagebox.showinfo("Eliminación", f"Envío con ID {idEnvio} eliminado correctamente.")
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


def verEquipo():
    messagebox.showinfo("Equipo de Desarrollo", "App creada por el equipo de desarrollo.")


def mostrarVentanaPrincipal():
    app = tk.Tk()
    app.title("App de Envíos")
    app.geometry("400x400")

    tk.Button(app, text="Crear Envío", command=crearEnvio, width=30).pack(pady=5)
    tk.Button(app, text="Ver Envíos", command=verEnvios, width=30).pack(pady=5)
    if usuario_actual["rol"] == "admin":
        tk.Button(app, text="Eliminar Envío", command=eliminarEnvio, width=30).pack(pady=5)
    tk.Button(app, text="Modificar Comuna", command=modificarUsuario, width=30).pack(pady=5)
    tk.Button(app, text="Ver Equipo", command=verEquipo, width=30).pack(pady=5)
    tk.Button(app, text="Salir", command=app.destroy, width=30).pack(pady=5)

    app.mainloop()



ventana_bienvenida = tk.Tk()
ventana_bienvenida.title("Inicio de Sesión")
ventana_bienvenida.geometry("300x200")
tk.Button(ventana_bienvenida, text="Registrar", command=registrarUsuario, width=30).pack(pady=10)
tk.Button(ventana_bienvenida, text="Iniciar Sesión", command=login, width=30).pack(pady=10)
ventana_bienvenida.mainloop()

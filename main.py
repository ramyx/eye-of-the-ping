#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox
from plyer import notification
from utils.storage import load_devices, save_devices
from utils.network import monitor_device, get_mac, find_ip_by_mac

# Intervalo de monitoreo en milisegundos (10 segundos por defecto)
MONITOR_INTERVAL = 10000

# Variables globales
devices = load_devices()
device_status = {device["ip"]: False for device in devices}  # Estado inicial


# Función para agregar un dispositivo
def add_device(name, ip):
    if name and ip:
        mac = get_mac(ip)  # Obtener MAC automáticamente
        if mac:
            devices.append({"name": name, "mac": mac.lower(), "ip": ip})
            device_status[ip] = False  # Inicialmente desconectado
            save_devices(devices)
            update_table()
        else:
            messagebox.showerror(
                "Error",
                "Failed to detect MAC address for the provided IP. Please check the IP.",
            )
    else:
        messagebox.showerror("Error", "Name and IP are required!")


# Función para eliminar un dispositivo
def delete_device():
    selected_items = tree.selection()  # Obtenemos los elementos seleccionados
    if not selected_items:
        messagebox.showerror("Error", "No device selected for deletion.")
        return

    for selected_item in selected_items:
        try:
            # Obtener datos del elemento seleccionado
            item_data = tree.item(selected_item)
            ip = item_data["values"][1]  # Columna de IP
            # Eliminar el dispositivo de la lista y del estado
            devices[:] = [d for d in devices if d["ip"] != ip]
            device_status.pop(ip, None)
            tree.delete(selected_item)  # Eliminar del Treeview
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete device: {e}")

    # Guardar los cambios en el almacenamiento
    save_devices(devices)
    update_table()


# Función para actualizar la tabla
def update_table():
    for item in tree.get_children():
        tree.delete(item)
    for device in devices:
        status = "Online" if device_status.get(device["ip"], False) else "Offline"
        tree.insert(
            "", "end", values=(device["name"], device["ip"], device["mac"], status)
        )


# Función para monitorear dispositivos
def monitor_network():
    for device in devices:
        ip = device["ip"]
        mac = device["mac"]

        # 1. Verificar si la IP responde al ping
        is_online = monitor_device(ip)

        if is_online:
            # Confirmar la MAC para la IP
            current_mac = get_mac(ip)
            if current_mac and current_mac.lower() != mac:
                # MAC no coincide, posiblemente la IP cambió
                new_ip = find_ip_by_mac(mac)
                if new_ip:
                    device["ip"] = new_ip
                    save_devices(devices)
                    notification.notify(
                        title="IP Updated",
                        message=f"{device['name']}'s IP has changed to {new_ip}.",
                        app_name="Eye of the Ping",
                    )
            else:
                # Confirmación de conexión
                if not device_status[ip]:
                    notification.notify(
                        title="Device Connected",
                        message=f"{device['name']} ({ip}) is now online.",
                        app_name="Eye of the Ping",
                    )
        else:
            # 2. Si la IP no responde, buscar la MAC en otra IP
            new_ip = find_ip_by_mac(mac)
            if new_ip and new_ip != ip:
                device["ip"] = new_ip
                save_devices(devices)
                notification.notify(
                    title="IP Updated",
                    message=f"{device['name']}'s IP has changed to {new_ip}.",
                    app_name="Eye of the Ping",
                )
            elif device_status[ip]:
                notification.notify(
                    title="Device Disconnected",
                    message=f"{device['name']} ({ip}) has disconnected.",
                    app_name="Eye of the Ping",
                )

        # Actualizar el estado del dispositivo
        device_status[ip] = monitor_device(device["ip"])

    # Actualizar la tabla y reintentar según MONITOR_INTERVAL
    update_table()
    root.after(MONITOR_INTERVAL, monitor_network)


# Crear ventana principal
root = tk.Tk()
root.title("Eye of the Ping")

# Formulario para agregar dispositivos
form_frame = tk.Frame(root)
form_frame.pack(pady=10)
name_label = tk.Label(form_frame, text="Name:")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(form_frame)
name_entry.grid(row=0, column=1)

ip_label = tk.Label(form_frame, text="IP Address:")
ip_label.grid(row=1, column=0)
ip_entry = tk.Entry(form_frame)
ip_entry.grid(row=1, column=1)

add_button = tk.Button(
    form_frame,
    text="Add Device",
    command=lambda: add_device(name_entry.get(), ip_entry.get()),
)
add_button.grid(row=2, columnspan=2, pady=5)

# Tabla de dispositivos
table_frame = tk.Frame(root)
table_frame.pack(pady=10)

tree = ttk.Treeview(
    table_frame, columns=("Name", "IP", "MAC", "Status"), show="headings", height=10
)
tree.heading("Name", text="Name")
tree.heading("IP", text="IP Address")
tree.heading("MAC", text="MAC Address")
tree.heading("Status", text="Status")
tree.pack()

# Botón para eliminar dispositivos
delete_button = tk.Button(
    root,
    text="Delete Selected Device",
    command=delete_device,  # Sin paréntesis ni argumentos
)
delete_button.pack(pady=5)

update_table()
monitor_network()
root.mainloop()

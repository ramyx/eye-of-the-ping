import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from plyer import notification
import pygame  # Importar pygame para la reproducción de audio
from utils.storage import load_devices, save_devices
from utils.network import monitor_device, get_mac, find_ip_by_mac

# Inicializar pygame para audio
pygame.mixer.init()

# Variables globales
devices = load_devices()
device_status = {device["ip"]: False for device in devices}  # Estado inicial


# Función para agregar un dispositivo
def add_device(name, ip, audio_path, play_sound):
    if name and ip:
        mac = get_mac(ip)  # Obtener MAC automáticamente
        if mac:
            devices.append({
                "name": name,
                "mac": mac.lower(),
                "ip": ip,
                "audio": audio_path,
                "play_sound": play_sound,
            })
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
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showerror("Error", "No device selected for deletion.")
        return

    for selected_item in selected_items:
        try:
            ip = tree.item(selected_item)["values"][1]
            devices[:] = [d for d in devices if d["ip"] != ip]
            device_status.pop(ip, None)
            tree.delete(selected_item)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete device: {e}")

    save_devices(devices)
    update_table()


# Función para actualizar la tabla
def update_table():
    for item in tree.get_children():
        tree.delete(item)
    for device in devices:
        status = "Online" if device_status.get(device["ip"], False) else "Offline"
        tree.insert("", "end", values=(device["name"], device["ip"], device["mac"], status))


# Función para monitorear dispositivos
def monitor_network():
    for device in devices:
        ip = device["ip"]
        mac = device["mac"]
        audio = device.get("audio")
        play_sound = device.get("play_sound", False)

        # Verificar si la IP responde al ping
        is_online = monitor_device(ip)

        if is_online and not device_status[ip]:
            notification.notify(
                title="Device Connected",
                message=f"{device['name']} ({ip}) is now online.",
                app_name="Eye of the Ping",
            )
            if play_sound and audio:
                try:
                    pygame.mixer.music.load(audio)  # Cargar archivo de audio
                    pygame.mixer.music.play()  # Reproducir audio
                except Exception as e:
                    print(f"Error playing sound: {e}")
        elif not is_online and device_status[ip]:
            notification.notify(
                title="Device Disconnected",
                message=f"{device['name']} ({ip}) has disconnected.",
                app_name="Eye of the Ping",
            )

        # Actualizar el estado del dispositivo
        device_status[ip] = is_online

    update_table()
    root.after(5000, monitor_network)  # 5 segundos de intervalo


# Crear ventana principal
root = tk.Tk()
root.title("Eye of the Ping")

# Formulario para agregar dispositivos
form_frame = tk.Frame(root)
form_frame.pack(pady=10)

# Campos del formulario
name_label = tk.Label(form_frame, text="Name:")
name_label.grid(row=0, column=0)
name_entry = tk.Entry(form_frame)
name_entry.grid(row=0, column=1)

ip_label = tk.Label(form_frame, text="IP Address:")
ip_label.grid(row=1, column=0)
ip_entry = tk.Entry(form_frame)
ip_entry.grid(row=1, column=1)

audio_label = tk.Label(form_frame, text="Audio File:")
audio_label.grid(row=2, column=0)
audio_path = tk.StringVar()
audio_entry = tk.Entry(form_frame, textvariable=audio_path, state="readonly")
audio_entry.grid(row=2, column=1)
browse_button = tk.Button(
    form_frame, text="Browse", command=lambda: audio_path.set(filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")]))
)
browse_button.grid(row=2, column=2)

play_sound_var = tk.BooleanVar()
play_sound_checkbox = tk.Checkbutton(form_frame, text="Enable Sound", variable=play_sound_var)
play_sound_checkbox.grid(row=3, columnspan=3)

# Botón para agregar dispositivo
add_button = tk.Button(
    form_frame,
    text="Add Device",
    command=lambda: add_device(name_entry.get(), ip_entry.get(), audio_path.get(), play_sound_var.get()),
)
add_button.grid(row=4, columnspan=3, pady=5)

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
    command=delete_device,
)
delete_button.pack(pady=5)

# Inicializar tabla y monitoreo
update_table()
monitor_network()

# Ejecutar aplicación
root.mainloop()

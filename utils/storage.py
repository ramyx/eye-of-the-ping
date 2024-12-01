import json
import os

CONFIG_FILE = "devices.json"


def load_devices():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return []


def save_devices(devices):
    with open(CONFIG_FILE, "w") as file:
        json.dump(devices, file, indent=4)

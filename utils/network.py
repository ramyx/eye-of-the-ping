import subprocess


def monitor_device(ip):
    """Verifica si el dispositivo responde a un ping."""
    try:
        output = subprocess.check_output(
            ["ping", "-c", "1", ip], stderr=subprocess.DEVNULL, universal_newlines=True
        )
        return "1 received" in output
    except subprocess.CalledProcessError:
        return False


def get_mac(ip):
    """Obtiene la MAC asociada a una IP usando el comando arp."""
    try:
        output = subprocess.check_output(["arp", "-n", ip], stderr=subprocess.DEVNULL)
        for line in output.decode("utf-8").splitlines():
            if ip in line:
                return line.split()[2]
        return None
    except Exception:
        return None


def find_ip_by_mac(mac):
    """Busca una IP en la red local asociada a una MAC específica."""
    try:
        output = subprocess.check_output(["arp", "-n"], stderr=subprocess.DEVNULL)
        for line in output.decode("utf-8").splitlines():
            if mac.lower() in line.lower():
                return line.split()[0]  # La primera columna es la IP
        return None
    except Exception:
        return None

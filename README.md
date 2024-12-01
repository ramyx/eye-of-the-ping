# Eye of the Ping

**Eye of the Ping** is a Python application with a Tkinter-based interface that monitors devices on your local network. The app detects when devices connect or disconnect, notifies the user, and optionally plays a custom audio file for each device.

---

## **Features**
- Monitor devices using their IP address and dynamically resolve their MAC addresses.
- Notify the user when a device connects or disconnects.
- Optionally play a custom audio file when devices connect.
- Update a device's IP address automatically if it changes.
- Simple interface for adding, removing, and viewing monitored devices.

---

## **Requirements**
- **Python 3.10 or higher**
- Required Python libraries:
  - `pygame`
  - `plyer`
  - `tkinter` (usually pre-installed in Python distributions)

Install dependencies using `pip`:
```bash
pip install -r requirements.txt
```

For Ubuntu, make sure the following system packages are installed:
```bash
sudo apt update
sudo apt install python3 python3-tk python3-pip
```

---

## **Installation**

### **1. Clone this repository**
```bash
git clone https://github.com/yourusername/eye-of-the-ping.git
cd eye-of-the-ping
```

### **2. Install Python dependencies**
```bash
pip install -r requirements.txt
```

---

## **Usage**
1. Run the application:
   ```bash
   python3 main.py
   ```
2. Add devices:
   - Enter the device's **name** and **IP address**.
   - Optionally select a custom audio file to play when the device connects.
   - Enable or disable sound playback using the checkbox.
3. The app will monitor these devices, detect their MAC addresses, and notify you of their connection status.

---

## **File Structure**
- **`main.py`**: Main application script.
- **`utils/network.py`**: Functions for monitoring devices and resolving IP/MAC.
- **`utils/storage.py`**: Functions for loading and saving device data.
- **`requirements.txt`**: List of required Python libraries.
- **`README.md`**: Documentation.
- **`.gitignore`**: Files and directories to ignore in Git.

---

## **Known Issues**
- Scapy-based MAC resolution and monitoring require elevated permissions. Run the application with `sudo` or configure Python with the following command:
  ```bash
  sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)
  ```

- If audio does not play, ensure that the selected file is a supported format (e.g., MP3, WAV).

---

## **Contributing**
We welcome contributions! Please:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature description"
   ```
4. Push to the branch and create a pull request.

---

## **License**
This project is licensed under the [MIT License](LICENSE).

---

## **Author**
Developed by **Ramiro Daniel Martinez**.

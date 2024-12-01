# Eye of the Ping

**Eye of the Ping** is a Python application with a Tkinter-based interface that monitors devices on your local network. The app detects when devices connect or disconnect, notifies the user, and provides options to manage monitored devices.

---

## **Features**
- Monitor devices using their IP address and dynamically resolve their MAC addresses.
- Notify the user when a device connects or disconnects.
- Update a device's IP address automatically if it changes.
- Simple interface for adding, removing, and viewing monitored devices.

---

## **Requirements**
- **Python 3.10 or higher**
- Required Python libraries:
  - `tkinter`
  - `plyer`

---

## **Installation**

### **1. Install system dependencies (Ubuntu)**
On Ubuntu, make sure to install the required system packages using `apt`:
```bash
sudo apt update
sudo apt install python3 python3-tk python3-pip
```

### **2. Clone this repository**
```bash
git clone https://github.com/yourusername/eye-of-the-ping.git
cd eye-of-the-ping
```

### **3. Install Python dependencies(Other than Ubuntu)**
Use `pip` to install the required Python libraries:
```bash
pip install -r requirements.txt
```

---

## **Usage**
1. Run the application:
   ```bash
   python3 main.py
   ```
2. Add devices by entering their **name** and **IP address** in the interface.
3. The app will monitor these devices, detect their MAC addresses, and notify you of their status.

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
- For accurate monitoring of devices and network operations, ensure the application has appropriate network permissions.

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

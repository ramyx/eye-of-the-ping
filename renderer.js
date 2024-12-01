const { fs, path, exec, generateAudio, buffer } = window.api;

const deviceFilePath = path.join(window.api.dirname, "monitoredDevices.json");

const deviceForm = document.getElementById("device-form");
const nameInput = document.getElementById("name-input");
const phoneInput = document.getElementById("phone-input");
const macInput = document.getElementById("mac-input");
const ipInput = document.getElementById("ip-input");
const soundInput = document.getElementById("sound-input");
const deviceList = document.getElementById("device-list");
const statusElement = document.getElementById("status");

let monitoredDevices = [];
let deviceStatus = {}; // Estado actual de los dispositivos (conectado/desconectado)

// Cargar los dispositivos desde el archivo al iniciar
function loadDevices() {
    if (fs.exists(deviceFilePath)) {
        monitoredDevices = JSON.parse(fs.readFile(deviceFilePath));
        monitoredDevices.forEach((device) => {
            deviceStatus[device.mac] = false; // Inicialmente desconectados
        });
        updateDeviceList();
    } else {
        fs.writeFile(deviceFilePath, JSON.stringify([]));
        monitoredDevices = [];
    }
}

// Guardar los dispositivos en el archivo
function saveDevices() {
    fs.writeFile(deviceFilePath, JSON.stringify(monitoredDevices, null, 2));
}

// Actualizar la lista de dispositivos en la tabla
function updateDeviceList() {
    deviceList.innerHTML = ""; // Limpia la tabla
    monitoredDevices.forEach((device, index) => {
        const row = document.createElement("tr");

        row.innerHTML = `
      <td>${device.name}</td>
      <td>${device.phone}</td>
      <td>${device.mac}</td>
      <td>${device.ip}</td>
      <td class="${deviceStatus[device.mac] ? "connected" : "disconnected"}">
        ${deviceStatus[device.mac] ? "Connected" : "Disconnected"}
      </td>
      <td><button class="delete-btn" data-index="${index}">Delete</button></td>
    `;

        deviceList.appendChild(row);
    });

    // Agregar eventos a los botones de eliminar
    document.querySelectorAll(".delete-btn").forEach((button) => {
        button.addEventListener("click", (event) => {
            const index = event.target.dataset.index;
            monitoredDevices.splice(index, 1); // Elimina el dispositivo
            saveDevices(); // Guarda los cambios
            updateDeviceList(); // Actualiza la tabla
        });
    });
}

// Evento para agregar un nuevo dispositivo
deviceForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const name = nameInput.value.trim();
    const phone = phoneInput.value.trim();
    const mac = macInput.value.trim();
    const ip = ipInput.value.trim();
    const soundFile = soundInput.files[0]; // Archivo seleccionado

    if (!soundFile) {
        alert("Please select a sound file.");
        return;
    }

    if (name && phone && mac && ip && !monitoredDevices.find((d) => d.mac === mac)) {
        const soundPath = window.api.path.join(window.api.dirname, soundFile.name);
        const reader = new FileReader();
        reader.onload = function () {
            // Usa window.api.buffer.from para convertir los datos
            window.api.fs.writeFile(soundPath, window.api.buffer.from(new Uint8Array(this.result)));
            console.log(`Archivo de sonido guardado en: ${soundPath}`);

            // Agregar el dispositivo a la lista
            monitoredDevices.push({ name, phone, mac, ip, sound: soundPath });
            deviceStatus[mac] = false; // Inicialmente desconectado
            updateDeviceList();
            saveDevices(); // Guarda el nuevo dispositivo
        };
        reader.readAsArrayBuffer(soundFile);
    }

    nameInput.value = ""; // Limpia los campos
    phoneInput.value = "";
    macInput.value = "";
    ipInput.value = "";
    soundInput.value = ""; // Limpia el campo del archivo
});

// Monitorear la red periódicamente usando la tabla ARP
function checkNetwork() {
    window.api.exec("arp -a", (err, stdout) => {
        if (err) {
            statusElement.innerText = "Error reading ARP table.";
            statusElement.style.color = "red";
            console.error("Error ejecutando arp:", err);
            return;
        }

        monitoredDevices.forEach((device) => {
            const macDetected = stdout.toLowerCase().includes(device.mac.toLowerCase());
            const ipDetected = stdout.includes(device.ip);

            if (macDetected || ipDetected) {
                if (!deviceStatus[device.mac]) {
                    console.log(`Dispositivo ingresó: ${device.name}`);
                    new Notification("Eye of the Ping", {
                        body: `Welcome ${device.name}! Your device is now connected.`,
                    });

                    if (device.sound) {
                        const audio = new Audio(device.sound);
                        audio.play();
                    }
                }
                deviceStatus[device.mac] = true;
            } else {
                if (deviceStatus[device.mac]) {
                    console.log(`Dispositivo salió: ${device.name}`);
                    new Notification("Eye of the Ping", {
                        body: `${device.name}, your device has disconnected.`,
                    });
                }
                deviceStatus[device.mac] = false;
            }
        });

        updateDeviceList();
        updateGeneralStatus();
    });
}

// Función para actualizar el estado general en la interfaz
function updateGeneralStatus() {
    if (Object.values(deviceStatus).some((status) => status)) {
        statusElement.innerText = "One or more devices are connected.";
        statusElement.style.color = "green";
    } else {
        statusElement.innerText = "No monitored devices connected.";
        statusElement.style.color = "orange";
    }
}

// Cargar los dispositivos al iniciar
loadDevices();

// Ejecuta el monitoreo cada 10 segundos
setInterval(checkNetwork, 10000); // Cada 10 segundos

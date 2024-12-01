const { app, BrowserWindow } = require("electron");
const path = require("path");

let mainWindow;

// Función para crear la ventana principal
function createMainWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, "preload.js"), // Ruta al archivo preload.js
            contextIsolation: true, // Aislar el contexto para seguridad
            nodeIntegration: false, // Desactiva integración de Node.js en el renderizador
            sandbox: false, // Desactivar el sandbox si es necesario
        },
    });

    mainWindow.loadFile("index.html"); // Cargar el archivo HTML principal

    mainWindow.on("closed", () => {
        mainWindow = null; // Limpia la referencia a la ventana
    });
}

// Evento cuando la aplicación está lista
app.whenReady().then(() => {
    createMainWindow();

    app.on("activate", () => {
        // Recrear la ventana si no hay ninguna abierta
        if (BrowserWindow.getAllWindows().length === 0) {
            createMainWindow();
        }
    });
});

// Evento cuando todas las ventanas están cerradas
app.on("window-all-closed", () => {
    // Salir de la aplicación, excepto en macOS
    if (process.platform !== "darwin") {
        app.quit();
    }
});

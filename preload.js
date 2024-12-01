const { contextBridge } = require("electron");
const fs = require("fs");
const path = require("path");
const { exec } = require("child_process"); // Importar exec desde child_process

contextBridge.exposeInMainWorld("api", {
    exec: (command, callback) => exec(command, callback), // Ahora exec está definido
    fs: {
        readFile: (filePath) => fs.readFileSync(filePath, "utf-8"),
        writeFile: (filePath, data) => fs.writeFileSync(filePath, data, "utf-8"),
        exists: (filePath) => fs.existsSync(filePath),
    },
    path: {
        join: (...args) => path.join(...args),
    },
    dirname: __dirname, // Esto expone correctamente __dirname
    buffer: {
        from: (data) => Buffer.from(data), // Exponer Buffer
    },
});

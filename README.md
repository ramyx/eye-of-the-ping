# Eye of the Ping

**Eye of the Ping** is an application built with [Electron](https://www.electronjs.org/) that monitors devices connected to your local network. When a device joins or leaves the network, the app sends a notification and plays a custom audio file assigned to the device.

## **Features**
- Monitor devices in your local network using their MAC or IP address.
- Receive notifications when a device connects or disconnects.
- Assign and play custom audio files for each device.
- Modern and simple interface with a device status table.

## **Requirements**
- Node.js (version 16 or higher recommended)
- npm or yarn
- A compatible operating system (Windows, macOS, or Linux)

## **Installation**
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/eye-of-the-ping.git
   ```
2. Navigate to the project directory:
   ```bash
   cd eye-of-the-ping
   ```
3. Install dependencies:
   ```bash
   npm install
   ```

## **Usage**
1. Start the application:
   ```bash
   npm start
   ```
2. Configure the devices you want to monitor:
   - Enter the owner's name, phone number, MAC address, IP address, and upload a custom audio file for each device.
3. The app will automatically start monitoring the network.

## **Project Structure**
- **`/src`**: Application source code.
  - **`main.js`**: Main Electron process.
  - **`preload.js`**: Secure bridge configuration for exposing features to the renderer process.
  - **`renderer.js`**: Renderer logic.
- **`/assets`**: Static assets such as icons and audio files.
- **`/dist`**: Compiled files (ignored in `.gitignore`).

## **Additional Features**
- Custom audio files are stored locally in the project root folder.
- Notifications are triggered automatically when devices connect or disconnect.

## **Contributing**
We welcome contributions! To contribute:
1. Fork the project.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature/new-feature
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add new feature"
   ```
4. Submit a pull request.

## **License**
This project is licensed under the GNU General Public License v3.0.
See the [LICENSE](LICENCE) file for more details.

## **Author**
Developed by **Ramiro Daniel Martinez**.


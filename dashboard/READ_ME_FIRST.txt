RESQMESH — READY-TO-RUN OFFLINE DASHBOARD
=======================================

Mac:
1. Unzip the folder.
2. Install Python 3 if it is not installed.
3. Double-click START_DASHBOARD.command (or right-click > Open if macOS blocks it).
4. Wait for your browser to open the dashboard. Use 'Generate demo SOS' to test without hardware.
5. Connect the gateway ESP32 to USB. Close Arduino Serial Monitor.
6. Double-click START_GATEWAY_READER.command. It lists available serial ports.
7. Enter the gateway port, such as /dev/cu.usbserial-0001.
8. Press SOS on your transmitter. The incident appears on the dashboard automatically.

Windows:
Use START_DASHBOARD_WINDOWS.bat and START_GATEWAY_READER_WINDOWS.bat instead.

First launch needs internet to install Python packages. After that the app and its SQLite database run offline.
The dashboard expects the gateway firmware to output lines like:
RESQMESH_EVENT,NODE_01-1,NODE_01,SOS,1,VILLAGE_A_SCHOOL,-65,9.50

The serial reader must stay running to collect live gateway events. Only one app can open the serial port at once; close Arduino Serial Monitor first.

Data is saved in resqmesh.db next to the app. The demo buttons create records labeled Demo.

This is a prototype, not a certified emergency response service.

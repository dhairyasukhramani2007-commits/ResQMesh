#!/bin/bash
cd "$(dirname "$0")"
if [ ! -d .venv ]; then echo 'Run START_DASHBOARD.command once first.'; read -r; exit 1; fi
source .venv/bin/activate
python -m serial.tools.list_ports
printf '\nEnter the USB serial port of the GATEWAY (example: /dev/cu.usbserial-0001): '
read -r PORT
if [ -z "$PORT" ]; then echo 'No port entered'; read -r; exit 1; fi
python serial_reader.py --port "$PORT"

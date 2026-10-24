import argparse
import time
import serial
from serial.tools import list_ports
from database import init, add

BAUD = 115200

def ports():
    return [(p.device, p.description) for p in list_ports.comports()]

def parse(line):
    if not line.startswith('RESQMESH_EVENT,'):
        return False
    f = line.strip().split(',')
    if len(f) != 8:
        print('Invalid event field count:',line,flush=True)
        return False
    try:
        _,packet,node,kind,priority,location,rssi,snr=f
        added=add(packet,node,kind,int(priority),location,int(rssi),float(snr))
        print(('NEW ALERT: ' if added else 'Already saved: ')+packet,flush=True)
        return added
    except ValueError:
        print('Invalid event values:',line,flush=True)
        return False

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--port',help='Serial device (e.g. /dev/cu.usbserial-0001 or COM3)')
    args=parser.parse_args()
    init()
    print('Available ports:',ports(),flush=True)
    if not args.port:
        print('No port specified. Start using: python serial_reader.py --port YOUR_PORT',flush=True)
        return
    while True:
        try:
            print('Connecting to',args.port,flush=True)
            with serial.Serial(args.port,BAUD,timeout=1) as s:
                print('Connected. Waiting for RESQMESH_EVENT messages...',flush=True)
                while True:
                    line=s.readline().decode('utf-8',errors='replace').strip()
                    if line:
                        print(line,flush=True)
                        parse(line)
        except (serial.SerialException,OSError) as exc:
            print('Connection issue:',exc,'— retrying in 3 seconds',flush=True)
            time.sleep(3)

if __name__=='__main__':
    main()

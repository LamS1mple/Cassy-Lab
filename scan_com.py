import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

ports = sorted(ports)
nameCom = []

for port, desc, hwid in sorted(ports):
    nameCom.append(port)

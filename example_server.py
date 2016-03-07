#!/usr/bin/env python

import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

# Connection variables
az = 0
el = 0

conn, addr = s.accept()
print('Received connection from:', addr)
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print("received data:", data)
    # Parse string
    pdata = data.split(",")
    try:
        az = float(pdata[0])
    except ValueError:
        print("Error parsing Azimuth: '",pdata[0],"'")
        break
    try:
        el = float(pdata[1])
    except ValueError:
        print("Error parsing Elevation: '",pdata[1],"'")
        break
    print("AZ: ",az)
    print("EL: ",el)
conn.close()

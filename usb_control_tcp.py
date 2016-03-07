#!python3

import threading
import socket
import time
import sys

## TCP Configuration
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20

# lock to serialize console output
print_lock = threading.Lock()

# Connection variables
az = 0
el = 0

def tcp_listen():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
        conn, addr = s.accept()
        with print_lock:
            print('Received connection from:', addr)
        while 1:
            data = conn.recv(BUFFER_SIZE)
            if not data: break
            # Parse string
            pdata = data.decode("utf-8").split(",")
            try:
                az = float(pdata[0])
            except ValueError:
                with print_lock:
                    print("Error parsing Azimuth: '",pdata[0],"'")
                break
            try:
                el = float(pdata[1])
            except ValueError:
                with print_lock:
                    print("Error parsing Elevation: '",pdata[1],"'")
                break
            with print_lock:
                print("AZ: ",az)
                print("EL: ",el)
        conn.close()

def usb_control():
    while True:
        

tcp_listener = threading.Thread(target=tcp_listen)
tcp_listener.daemon = True
tcp_listener.start()

while 1:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
          sys.exit()

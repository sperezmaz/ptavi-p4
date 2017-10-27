#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""
import sys
import socket

# Constantes. Dirección IP del servidor y contenido a enviar
try:
    SERVER = sys.argv[1]
    PUERTO = int(sys.argv[2])
    REGISTER = sys.argv[3]
    SIP_ADDRESS = sys.argv[4]
    EXPIRES_VALUE = sys.argv[5]

except:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")
    
line1 = REGISTER.upper() + " sip:" + SIP_ADDRESS + ' SIP/2.0\r\n'    
line = line1 + 'Expires: ' + EXPIRES_VALUE + '\r\n\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PUERTO))
    print("Enviando:", line)
    my_socket.send(bytes(line, 'utf-8')) #lo pasamos a bytes
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8')) #pasa a string los bytes

print("Socket terminado.")

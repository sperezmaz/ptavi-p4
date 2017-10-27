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
    PORT = int(sys.argv[2])
    TYPE_MESSAGES = sys.argv[3]
    ADDRESS_REGIST = sys.argv[4]

except ValueError:
    sys.exit("Error: Puerto solo puede ser entero")

line = TYPE_MESSAGES.upper() + " sip:" + ADDRESS_REGIST + ' SIP/2.0\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    print("Enviando:", line)
    my_socket.send(bytes(line, 'utf-8')) #lo pasamos a bytes
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8')) #pasa a string los bytes

print("Socket terminado.")

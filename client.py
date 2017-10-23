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
    LINE = " ".join(sys.argv[3:])
except ValueError:
    sys.exit("Error: Puerto solo puede ser entero")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket: 
    my_socket.connect((SERVER, PORT))
    print("Enviando:", LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n') #lo pasamos a bytes
    #tambien b'\r\n' pasa a bytes
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8')) #pasa a string los bytes

print("Socket terminado.")

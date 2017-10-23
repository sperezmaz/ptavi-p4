#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        #fichero imaginario de escritura en bytes
        self.wfile.write(b"Hemos recibido tu peticion")
        for line in self.rfile:
            Puerto_Client = self.client_address[1];
            print("La IP del cliente es: " + str(self.client_address[0]) + 
            ", el puerto del cliente es: " + str(Puerto_Client) + 
            " y nos manda:", line.decode('utf-8'))
        
if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    #va a estar escuchando en este puerto
    #PORT_ = int(sys.argv[1])
    serv = socketserver.UDPServer(('', int(sys.argv[1])), EchoHandler) 
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever() #espera en un bucle
    except KeyboardInterrupt: # ^C
        print("Finalizado servidor")

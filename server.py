#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc = {}
    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        #fichero imaginario de escritura en bytes
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        IP_Client = self.client_address[0];
        Port_Client = self.client_address[1];
        print("La IP del cliente es: " + str(IP_Client) +
              ", el puerto del cliente es: " + str(Port_Client))
        for line in self.rfile:
            message = line.decode('utf-8').split()
            type_messages = message[0]
            address_reg = message[1]
        if type_messages == "REGISTER":
            self.dicc[address_reg] = str(IP_Client)
            print(self.dicc)
        
if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    PORT_SERV = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT_SERV), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever() #espera en un bucle
    except KeyboardInterrupt: # ^C
        print("Finalizado servidor")

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
        Puerto_Client = self.client_address[1];
        print("La IP del cliente es: " + str(IP_Client) +
              ", el puerto del cliente es: " + str(Puerto_Client))
              
        line = self.rfile.read()
        message = line.decode('utf-8').split()
        register = message[0]
        sip_address = message[1]
        print(message)
        if int(message[4].split('/')[0]) >= 0:
            time = int(message[4].split('/')[0])
        else: 
            time = 0
        if register == "REGISTER":
            self.dicc[sip_address] = str(IP_Client)
        if time == 0:
            del self.dicc[sip_address]
        print(self.dicc)
        
if __name__ == "__main__":
    # Calls the EchoHandler class to manage the request
    PORT_SERV = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT_SERV), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever() #espera en un bucle
    except KeyboardInterrupt: # ^C
        print("Finalizado servidor")

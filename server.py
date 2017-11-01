#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Servidor (UDP) Register SIP utilizando fichero json
"""

import socketserver
import sys
import json
import time

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class.
    """
    list_users = []

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.json2registered()
        # fichero imaginario de escritura en bytes
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        
        IP_Client = self.client_address[0]
        Puerto_Client = self.client_address[1]
        print("La IP del cliente es: " + str(IP_Client) +
              ", el puerto del cliente es: " + str(Puerto_Client))

        line = self.rfile.read()
        message = line.decode('utf-8').split()
        register = message[0]
        sip_address = message[1][4:]
        for user_address in self.list_users:
            if user_address[1]["expires"] <= time.strftime('%Y-%m-%d %H:%M:%S',
                                                           time.gmtime(
                                                           time.time() 
                                                           + 3600)):
                self.list_users.remove(user_address)
                self.register2json()
        
        if int(message[4].split('/')[0]) >= 0:
            time_exp = int(message[4].split('/')[0])
        else:
            time_exp = 0
            
        t_tot = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(
                              time.time() + 3600 + time_exp))
        if register == "REGISTER":
            user = [sip_address, {"address": str(IP_Client), "expires": t_tot}]
            self.list_users.append(user)
        if time_exp == 0:
            self.list_users.remove(user)
            for user in self.list_users:
                if user[0] == sip_address:
                    self.list_users.remove(user)
        print(self.list_users)
        self.register2json()
        
    def register2json(self):
        json.dump(self.list_users, open('registered.json', 'w'), indent=4)
        
    def json2registered(self):
        try:
            with open('registered.json') as in_file:
                self.list_users = json.load(in_file)
        except:
            self.register2json()
            
if __name__ == "__main__":
    try:
        PORT_SERV = int(sys.argv[1])
    except:
        sys.exit("Usage: client.py <puerto>")
    serv = socketserver.UDPServer(('', PORT_SERV), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()  # espera en un bucle
    except KeyboardInterrupt:  # ^C
        print("Finalizado servidor")

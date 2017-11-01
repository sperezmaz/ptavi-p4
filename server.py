#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Servidor (UDP) Register SIP utilizando fichero json."""

import socketserver
import sys
import json
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """Echo server class."""

    list_users = []

    def handle(self):
        """handle method of the server class."""
        self.json2registered()
        # fichero imaginario de escritura en bytes
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

        ip_client = self.client_address[0]
        puerto_client = self.client_address[1]
        print("La IP del cliente es: " + str(ip_client) +
              ", el puerto del cliente es: " + str(puerto_client))

        line = self.rfile.read()
        message = line.decode('utf-8').split()
        register = message[0]
        sip_address = message[1][4:]
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time() + 3600))
        for user_address in self.list_users:
            if user_address[1]["expires"] <= t:
                self.list_users.remove(user_address)
                self.register2json()

        if int(message[4].split('/')[0]) >= 0:
            time_exp = int(message[4].split('/')[0])
        else:
            time_exp = 0

        t_tot = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(
                              time.time() + 3600 + time_exp))
        if register == "REGISTER":
            user = [sip_address, {"address": str(ip_client), "expires": t_tot}]
            self.list_users.append(user)
        if time_exp == 0:
            self.list_users.remove(user)
            for user in self.list_users:
                if user[0] == sip_address:
                    self.list_users.remove(user)
        print(self.list_users)
        self.register2json()

    def register2json(self):
        """Imprime en fichero registered.json informacion sobre el usuario."""
        json.dump(self.list_users, open('registered.json', 'w'), indent=4)

    def json2registered(self):
        """Leer contenido y usarlo para usuarios registrados."""
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

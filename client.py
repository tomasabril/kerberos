#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Tomás Abril
"""

import socket

class Client():

    def __init__(self):
        pass

    def connectto(self, port=50007, host='localhost'):
        self.serverHost = host
        self.serverPort = port
        # Criamos o socket e o conectamos ao servidor
        self.sockobj = socket.socket(AF_INET, SOCK_STREAM)
        self.sockobj.socket.connect((serverHost, serverPort))

    def send_msg(self, msg):
        # Menssagem a ser mandada condificada em bytes
        menssagem = msg.encode()

        # Mandamos a menssagem linha por linha
        for linha in menssagem:
            self.sockobj.send(linha)

            # Depois de mandar uma linha esperamos uma resposta
            # do servidor
            data = self.sockobj.recv(1024)
            print('Cliente recebeu:', data)

    def close_conection(self):
        # Fechamos a conexão
        self.sockobj.close()

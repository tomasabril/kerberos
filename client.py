#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Tomás Abril
"""

import socket


class Client():

    def __init__(self):
        pass

    def connectto(self, port=50001, host='localhost'):
        # Criamos o socket e o conectamos ao servidor
        self.sockobj = socket.socket()
        self.sockobj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockobj.connect((host, port))

    def send_msg(self, msg):
        # Menssagem a ser mandada condificada em bytes

        data = b''
        # Mandamos a menssagem linha por linha
        for letra in msg:
            lb = letra.encode()
            self.sockobj.send(lb)

            # Depois de mandar uma linha esperamos uma resposta
            # do servidor
            data += self.sockobj.recv(1024)
        print('Cliente recebeu:', data.decode())
        return data

    def close_conection(self):
        # Fechamos a conexão
        self.sockobj.close()

if __name__ == "__main__":
    clt = Client()
    clt.connectto()
    clt.send_msg("ola ola")
    clt.send_msg("testando segunda linha")
    clt.send_msg("mensagem muito comprida e com 2 caracteres estanhos = " +
                 "★ & £ aa\npulei linha!")
    clt.close_conection()

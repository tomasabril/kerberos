#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Tomás Abril
"""


import time
import socket

class As():

    def __init__(self, host='localhost', port=50001):
        # Cria o nome do host
        self.meuHost = host

        # Utiliza este número de porto
        self.minhaPort = port

        # Cria um objeto socket. As duas constantes referem-se a:
        # Familia do endereço (padrão é socket.AF_INET)
        # Se é stream (socket.SOCK_STREAM, o padrão)
        # ou datagram (socket.SOCK_DGRAM)
        # E o protocolo (padrão é 0)
        # Da maneira como configuramos:
        # AF_INIT == Protocolo de endereço de IP
        # SOCK_STREAM == Protocolo de transferência TCP
        # Combinação = Server TCP/IP
        self.sockobj = socket.socket()
        self.sockobj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Vincula o servidor ao número de porto
        self.sockobj.bind((self.meuHost, self.minhaPort))

    def listenFor(self, qte=5):
        # O socket começa a esperar por clientes limitando a
        # 5 conexões por vez
        self.sockobj.listen(qte)

        while True:
            # Aceita uma conexão quando encontrada e devolve a
            # um novo socket conexão e o endereço do cliente
            # conectado
            c_socket, addr = self.sockobj.accept()
            print('Server conectado por', addr)

            while True:
                # Recebe data enviada pelo cliente
                # até 1024 bytes
                data = c_socket.recv(1024)

                # Se não receber nada paramos o loop
                if not data:
                    break

                # O servidor manda de volta uma resposta
                c_socket.send(data)

            # Fecha a conexão criada depois de responder o
            # cliente
            c_socket.close()

if __name__ == "__main__":
    auth_server = As()
    auth_server.listenFor()


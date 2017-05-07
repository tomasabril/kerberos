#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Tomás Abril
"""

import os
import time
import socket
import pickle
import shelve
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# random data size
tam = 3


class Service1():


    # para o AES
    backend = default_backend()
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
#    ct = encryptor.update(b"a secret message") + encryptor.finalize()
#    decryptor = cipher.decryptor()
#    decryptor.update(ct) + decryptor.finalize()

    def __init__(self, host='localhost', port=50003):
        self.k_s = hashlib.sha512(b'123').hexdigest()


        self.meuHost = host
        self.minhaPort = port

        self.sockobj = socket.socket()
        # pra nao dar erro se não der .close()
        self.sockobj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Vincula o servidor ao número de port
        self.sockobj.bind((self.meuHost, self.minhaPort))
        print('Service 1 started at {} port {}'.format(host, port))


    def listenFor(self, qte=5):
        # O socket começa a esperar por clientes limitando a
        # 5 conexões por vez
        self.sockobj.listen(qte)
        print('Esperando conexão. Numero máximo = {}'.format(qte))

        while True:
            # Aceita uma conexão quando encontrada e devolve a
            # um novo socket conexão e o endereço do cliente
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
                data_str = data.decode()
#                print('recebi {}'.format(data_str))
                recebido = data_str.split(':')
                n3 = recebido[3]

                m6 = self.generatem6(n3).encode()
                c_socket.send(m6)

            # Fecha a conexão criada depois de responder o cliente
            c_socket.close()


    def generatem6(self, n3):
        resp = 'pode usar que deu tudo certo'
        parte1 = '{}:{}'.format(resp, n3)
        m6 = '{}'.format(parte1)
        return m6


if __name__ == "__main__":

    s1 = Service1()
    s1.listenFor()












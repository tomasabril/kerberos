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


class As():

    db_file = 'auth_server_db.shelve'

    # dicionario com os usuarios
    # id: hash_senha
    user_db = {}

    # para o AES
    backend = default_backend()
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
#    ct = encryptor.update(b"a secret message") + encryptor.finalize()
#    decryptor = cipher.decryptor()
#    decryptor.update(ct) + decryptor.finalize()

    def __init__(self, host='localhost', port=50001):
        self.k_tgs = hashlib.sha512(b'chave do tgs').hexdigest()

        # carregando dicionario do arquivo
        with shelve.open(self.db_file) as db:
            self.user_db = db['0']
        print('my registered users')
        u_list = list(self.user_db.keys())
        print(u_list)

        self.meuHost = host
        self.minhaPort = port

        self.sockobj = socket.socket()
        # pra nao dar erro se não der .close()
        self.sockobj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Vincula o servidor ao número de port
        self.sockobj.bind((self.meuHost, self.minhaPort))
        print('Authentication Server started at {} port {}'.format(host, port))

        self.create_user()

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
                user_id = recebido[0]
                t_r = recebido[2]
                n1 = recebido[3]
                if self.user_in_db(str(user_id)):
                    m2 = self.generatem2(user_id, t_r, n1).encode()
                    c_socket.send(m2)
                else:
                    c_socket.send(b'Usuario nao encontrado.')

            # Fecha a conexão criada depois de responder o cliente
            c_socket.close()

    def user_in_db(self, user_id):
        users = list(self.user_db.keys())
        if str(user_id) in users:
            return 1
        else:
            return 0

    def generatem2(self, id_c, t_r, n1):
        k_c_tgs = int.from_bytes(os.urandom(tam), byteorder="big")
        t_c_tgs = '{}:{}:{}'.format(id_c, t_r, k_c_tgs)
        m2 = '{}:{}:{}'.format(k_c_tgs, n1, t_c_tgs)
        return m2

    def create_user(self):
        while input('create new user?'):
            u_id = input('New user ID: ')
            senha = hashlib.sha512(input("senha: ").encode()).hexdigest()
            if not self.user_in_db(u_id):
                self.user_db[u_id] = senha
            else:
                print('Este id já está cadastrado')
            # salvando dicionario no arq
            with shelve.open(self.db_file) as db:
                db['0'] = self.user_db

if __name__ == "__main__":

    auth_server = As()
    auth_server.listenFor()

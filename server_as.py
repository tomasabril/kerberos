#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Tomás Abril
"""

import os
import socket
import shelve
import hashlib
import my_aes

# random data size
tam = 3


class As():

    db_file = 'auth_server_db.shelve'

    # dicionario com os usuarios
    # id: hash_senha
    user_db = {}

    def __init__(self, host='localhost', port=50001):
        self.k_tgs = hashlib.sha512(b'chave do tgs').hexdigest()[:32]

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

                data_split = data.split(b'::-+-::')
                user_id_b = data_split[0]
                crip_bin = data_split[1]
                user_id = user_id_b.decode()

                if self.user_in_db(str(user_id)):
                    # descriptografando
                    m1_dcrypt = my_aes.decrypt(crip_bin, self.user_db[user_id])
                    m1_dcrypt_split = m1_dcrypt.split(':')
                    t_r = m1_dcrypt_split[1]
                    n1 = m1_dcrypt_split[2]

                    m2 = self.generatem2(user_id, t_r, n1)
                    c_socket.send(m2)
                else:
                    c_socket.send(b'Usuario nao encontrado.' + b'::-+-::' + b'.')

            # Fecha a conexão criada depois de responder o cliente
            c_socket.close()

    def user_in_db(self, user_id):
        users = list(self.user_db.keys())
        if str(user_id) in users:
            return 1
        else:
            return 0

    def generatem2(self, id_c, t_r, n1):
        k_c_tgs = os.urandom(tam)
        k_c_tgs = hashlib.sha512(k_c_tgs).hexdigest()[:32]

        t_c_tgs = '{}:{}:{}'.format(id_c, t_r, k_c_tgs)
        t_c_tgs_crypt = my_aes.crypt(t_c_tgs, self.k_tgs)

        parte1 = '{}:{}'.format(k_c_tgs, n1)
        parte1_crypt = my_aes.crypt(parte1, self.user_db[id_c])

        m2 = parte1_crypt + b'::-+-::' + t_c_tgs_crypt
        return m2

    def create_user(self):
        while input('create new user? '):
            u_id = input('New user ID: ')
            senha = hashlib.sha512(input("senha: ").encode()).hexdigest()[:32]
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

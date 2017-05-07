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


class Tgs():

    db_file = 'tg_server_db.shelve'

    # dicionario com os usuarios
    # id: [hash_senha, max_time]
    service_db = {}

    # para o AES
    backend = default_backend()
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
#    ct = encryptor.update(b"a secret message") + encryptor.finalize()
#    decryptor = cipher.decryptor()
#    decryptor.update(ct) + decryptor.finalize()

    def __init__(self, host='localhost', port=50002):
        self.k_tgs = hashlib.sha512(b'chave do tgs').hexdigest()

        # carregando dicionario do arquivo
        with shelve.open(self.db_file) as db:
            self.service_db = db['0']
        print('my registered services')
        s_list = list(self.service_db.keys())
        print(s_list)

        self.meuHost = host
        self.minhaPort = port

        self.sockobj = socket.socket()
        # pra nao dar erro se não der .close()
        self.sockobj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Vincula o servidor ao número de port
        self.sockobj.bind((self.meuHost, self.minhaPort))
        print('Ticket Granting Server started at {} port {}'.format(host, port))

        self.create_service()

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
                service_id = recebido[1]
                user_id = recebido[0]
                t_r = recebido[2]
                n2 = recebido[3]
                if self.service_in_db(str(service_id)):
                    m4 = self.generatem4(user_id, t_r, n2, service_id).encode()
                    c_socket.send(m4)
                else:
                    c_socket.send(b'Servico nao encontrado.')

            # Fecha a conexão criada depois de responder o cliente
            c_socket.close()

    def service_in_db(self, service_id):
        services = list(self.service_db.keys())
        if str(service_id) in services:
            return 1
        else:
            return 0

    def generatem4(self, id_c, t_r, n2, id_s):
        if t_r > self.service_db[id_s][1]:
            t_a = self.service_db[id_s][1]
        else:
            t_a = t_r
        k_c_s = int.from_bytes(os.urandom(tam), byteorder="big")
        parte1 = '{}:{}'.format(k_c_s, n2)
        parte2 = '{}:{}:{}'.format(id_c, t_a, k_c_s)
        m4 = '{}:{}'.format(parte1, parte2)
        return m4

    def create_service(self):
        while input('create new service?'):
            u_id = input('New service ID: ')
            senha = hashlib.sha512(input("Senha: ").encode()).hexdigest()
            maxtime = input('Tempo maximo a ser permitido: ')
            if not self.service_in_db(u_id):
                self.service_db[u_id] = [senha, maxtime]
            else:
                print('Este id já está cadastrado')
            # salvando dicionario no arq
            with shelve.open(self.db_file) as db:
                db['0'] = self.service_db

if __name__ == "__main__":

    tgs = Tgs()
    tgs.listenFor()s

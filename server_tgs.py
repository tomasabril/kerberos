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


class Tgs():

    db_file = 'tg_server_db.shelve'

    # dicionario com os usuarios
    # id: [hash_senha, max_time]
    service_db = {}

    def __init__(self, host='localhost', port=50002):
        self.k_tgs = hashlib.sha512(b'chave do tgs').hexdigest()[:32]

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
                data_split = data.split(b'::-+-::')
                t_c_tgs_cryp = data_split[1]
                t_c_tgs = my_aes.decrypt(t_c_tgs_cryp, self.k_tgs)
                t_c_tgs = t_c_tgs.split(':')

                id_c = t_c_tgs[0]
                t_r = t_c_tgs[1]
                k_c_tgs = t_c_tgs[2]

                m3p1 = my_aes.decrypt(data_split[0], k_c_tgs).split(':')
                c_id_c = m3p1[0]
                id_s = m3p1[1]
                c_t_r = m3p1[2]
                n2 = m3p1[3]
                if c_id_c != id_c:
                    c_socket.send(b'Client id missmatch.' + b'::-+-::' + b'.')
                else:
                    if self.service_in_db(str(id_s)):
                        m4 = self.generatem4(id_c, t_r, n2, id_s, k_c_tgs)
                        c_socket.send(m4)
                    else:
                        c_socket.send(b'Servico nao encontrado.' + b'::-+-::' + b'.')

            # Fecha a conexão criada depois de responder o cliente
            c_socket.close()

    def service_in_db(self, service_id):
        services = list(self.service_db.keys())
        if str(service_id) in services:
            return 1
        else:
            return 0

    def generatem4(self, id_c, t_r, n2, id_s, k_c_tgs):
        if t_r > self.service_db[id_s][1]:
            t_a = self.service_db[id_s][1]
        else:
            t_a = t_r
        k_c_s = os.urandom(tam)
        k_c_s = hashlib.sha512(k_c_s).hexdigest()[:32]
        parte1 = '{}:{}'.format(k_c_s, n2)
        t_c_s = '{}:{}:{}'.format(id_c, t_a, k_c_s)
        p1_cryp = my_aes.crypt(parte1, k_c_tgs)
        t_c_s_cryp = my_aes.crypt(t_c_s, self.service_db[id_s][0])

        m4 = p1_cryp + b'::-+-::' + t_c_s_cryp
        return m4

    def create_service(self):
        while input('create new service? '):
            u_id = input('New service ID: ')
            senha = hashlib.sha512(input("Senha: ").encode()).hexdigest()[:32]
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
    tgs.listenFor()

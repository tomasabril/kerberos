#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Tomás Abril
"""

import os
import socket
import hashlib
import my_aes


# random data size
tam = 3


class Service1():

    def __init__(self, host='localhost', port=50003):
        self.k_s = hashlib.sha512(b'123').hexdigest()[:32]
        self.my_id = 1

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
                data_split = data.split(b'::-+-::')

                t_c_s = data_split[1]
                t_c_s = my_aes.decrypt(t_c_s, self.k_s)
                t_c_s_split = t_c_s.split(':')
                id_c = t_c_s_split[0]
                t_a = t_c_s_split[1]
                k_c_s = t_c_s_split[2]

                m5_p1 = data_split[0]
                m5_p1 = my_aes.decrypt(m5_p1, k_c_s)
                m5_p1_split = m5_p1.split(':')
                c_id_c = m5_p1_split[0]
                s_r = m5_p1_split[2]
                n3 = m5_p1_split[3]

                if c_id_c != id_c:
                    c_socket.send(b'Client id missmatch.')
                elif int(s_r) != self.my_id:
                    c_socket.send(b'Service missmatch.')
                else:
                    m6 = self.generatem6(n3, k_c_s, t_a)
                    c_socket.send(m6)

            # Fecha a conexão criada depois de responder o cliente
            c_socket.close()

    def generatem6(self, n3, k_c_s, t_a):
        resp = 'pode usar que deu tudo certo, tempo permitido = {}'.format(t_a)
        parte1 = '{}:{}'.format(resp, n3)
        p1_cryp = my_aes.crypt(parte1, k_c_s)
        m6 = p1_cryp
        return m6


if __name__ == "__main__":

    s1 = Service1()
    s1.listenFor()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Tomás Abril
"""

import socket
import os
import hashlib

# random data size
tam = 3

class Client():

    m1 = ''
    m2 = ''
    m3 = ''
    m4 = ''
    m5 = ''
    m6 = ''

    def __init__(self):
        self.id_c = 1
        self.kc = hashlib.sha512(input("Minha senha: ").encode()).hexdigest()

    def connectto(self, port=50001, host='localhost'):
        # Criamos o socket e o conectamos ao servidor
        self.sockobj = socket.socket()
        self.sockobj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockobj.connect((host, port))

    def send_msg(self, msg):
        # Menssagem a ser mandada condificada em bytes
        self.sockobj.send(msg.encode())

        data = self.sockobj.recv(1024)
        resposta = data.decode()

        return resposta

    def close_conection(self):
        # Fechamos a conexão
        self.sockobj.close()

    def auth_with_as(self, id_s=1, t_r=60):
        n1 = int.from_bytes(os.urandom(tam), byteorder="big")
        self.m1 = "{}:{}:{}:{}".format(self.id_c, id_s, t_r, n1)

        self.connectto(port=50001)
        self.m2 = self.send_msg(self.m1)
        self.close_conection()

        print('m1= {}'.format(self.m1))
        print('m2= {}'.format(self.m2))

    def get_ticket(self):
        msg1 = self.m1.split(':')
        id_s = msg1[1]
        t_r = msg1[2]
        n2 = int.from_bytes(os.urandom(tam), byteorder="big")
        parte1 = '{}:{}:{}:{}'.format(self.id_c, id_s, t_r, n2)
        msg2 = self.m2.split(':')
        t_c_tgs = '{}:{}:{}'.format(msg2[2], msg2[3], msg2[4])
        self.m3 = '{}:{}'.format(parte1, t_c_tgs)

        self.connectto(port=50002)
        self.m4 = self.send_msg(self.m3)
        self.close_conection()

        print('m3= {}'.format(self.m3))
        print('m4= {}'.format(self.m4))

if __name__ == "__main__":
    clt = Client()
    clt.auth_with_as(id_s=1)
    clt.get_ticket()

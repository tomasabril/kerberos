#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Tomás Abril
"""

import socket
import os
import hashlib
import my_aes

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
        # my ID
        self.id_c = 1
        self.id_s = -1
        self.t_r = -1
        self.kc = hashlib.sha512(input("Minha senha: ").encode()).hexdigest()[:32]
#        self.kc = hashlib.sha512(b'123').hexdigest()[:32]
        self.k_c_tgs = ''
        self.t_c_tgs = ''
        self.t_c_s = ''

    def connectto(self, port=50000, host='localhost'):
        # Criamos o socket e o conectamos ao servidor
        self.sockobj = socket.socket()
        self.sockobj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockobj.connect((host, port))

    def send_msg(self, msg):
        # Menssagem a ser mandada condificada em bytes
        self.sockobj.send(msg)
        data = self.sockobj.recv(1024)
        return data

    def close_conection(self):
        # Fechamos a conexão
        self.sockobj.close()

    def auth_with_as(self, id_s=1, t_r=60):
        self.id_s = id_s
        self.t_r = t_r
        n1 = int.from_bytes(os.urandom(tam), byteorder="big")
        parte1 = '{}'.format(self.id_c)
        parte2 = '{}:{}:{}'.format(id_s, t_r, n1)
        p2crypt = my_aes.crypt(parte2, self.kc)

        self.m1 = parte1.encode() + b'::-+-::' + p2crypt

        self.connectto(port=50001)
        self.m2 = self.send_msg(self.m1)
        self.close_conection()

        m2split = self.m2.split(b'::-+-::')
        m2_p1_cryp = m2split[0]
        m2_p1 = my_aes.decrypt(m2_p1_cryp, self.kc)
        self.k_c_tgs, n1rsp = m2_p1.split(':')
        n1rsp = int(n1rsp)
        if n1 != n1rsp:
            print('ERROR !!! n1 does not match.')
        self.t_c_tgs = m2split[1]

        print('m1= {}'.format(self.m1))
        print('m2= {}'.format(self.m2))

    def get_ticket(self):
        n2 = int.from_bytes(os.urandom(tam), byteorder="big")
        parte1 = '{}:{}:{}:{}'.format(self.id_c, self.id_s, self.t_r, n2)
        p1_cryp = my_aes.crypt(parte1, self.k_c_tgs)
        self.m3 = p1_cryp + b'::-+-::' + self.t_c_tgs

        self.connectto(port=50002)
        self.m4 = self.send_msg(self.m3)
        self.close_conection()

        m4split = self.m4.split(b'::-+-::')
        self.t_c_s = m4split[1]
        m4_p1 = m4split[0]
        m4_p1 = my_aes.decrypt(m4_p1, self.k_c_tgs)
        self.k_c_s, n2rsp = m4_p1.split(':')
        n2rsp = int(n2rsp)
        if n2 != n2rsp:
            print('ERROR !!! n2 does not match.')

        print('m3= {}'.format(self.m3))
        print('m4= {}'.format(self.m4))

    def use_service(self):
        n3 = int.from_bytes(os.urandom(tam), byteorder="big")
        parte1 = '{}:{}:{}:{}'.format(self.id_c, self.t_r, self.id_s, n3)
        p1_cryp = my_aes.crypt(parte1, self.k_c_s)

        self.m5 = p1_cryp + b'::-+-::' + self.t_c_s
        self.connectto(port=50003)
        self.m6 = self.send_msg(self.m5)
        self.close_conection()

        m6_decryp = my_aes.decrypt(self.m6, self.k_c_s)
        resposta, n3rsp = m6_decryp.split(':')
        if n3 != int(n3rsp):
            print('ERROR !!! n3 does not match.')

        print('m5= {}'.format(self.m5))
        print('m6= {}'.format(self.m6))

        print('resposta do servico:\n{}'.format(resposta))

if __name__ == "__main__":
    clt = Client()
    clt.auth_with_as(id_s=1)
    clt.get_ticket()
    clt.use_service()

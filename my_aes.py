#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 19:04:54 2017

@author: samot
"""

import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


def crypt(msg, chave):
    '''msg é uma string \n
       chave é Hex de 32 bits \n
       retorna binario \n
    '''
    # para o AES
    key = chave.encode()
    backend = default_backend()
    #iv = os.urandom(16)
    iv = b'a'*16
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    msgb = msg.encode()
#    print('mensagem descriptografada sem pad:')
#    print(msgb)

    # padding
    padder = padding.PKCS7(128).padder()
    padded_msg = padder.update(msgb) + padder.finalize()
#    print('mensagem descriptografada com pad:')
#    print(padded_msg)
#    print('mensagem descriptografada com pad em string:')
#    print(padded_msg.decode())
    msg_cryp = encryptor.update(padded_msg) + encryptor.finalize()

    return msg_cryp


def decrypt(msg, chave):
    '''msg é um binário criptografado \n
       chave é Hex de 32 bits \n
       retorna string \n
    '''
    # para o AES
    key = chave.encode()
    backend = default_backend()
    #iv = os.urandom(16)
    iv = b'a'*16
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)

    decryptor = cipher.decryptor()
    msg_denovo_pad = decryptor.update(msg) + decryptor.finalize()

#    print('mensagem descriptografada com pad:')
#    print(msg_denovo_pad)
#    print('mensagem descriptografada com pad em string:')
#    print(msg_denovo_pad.decode())
    # unpadding
    unpadder = padding.PKCS7(128).unpadder()
    msg_denovo_b = unpadder.update(msg_denovo_pad)
    msg_denovo_b += unpadder.finalize()
#    print('mensagem descriptografada sem pad:')
#    print(msg_denovo_b)
    msg_denovo = msg_denovo_b.decode()

    return msg_denovo

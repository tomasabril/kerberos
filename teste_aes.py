#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 15:49:45 2017

@author: samot
"""

import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# para o AES
backend = default_backend()
key = hashlib.sha512(b'chave').hexdigest()[:32].encode()
iv = os.urandom(16)
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
encryptor = cipher.encryptor()


msg = 'coisas muito secretas aqui:::123alo'
msgb = msg.encode()

# padding
padder = padding.PKCS7(128).padder()
padded_msg = padder.update(msgb) + padder.finalize()

msg_cryp = encryptor.update(padded_msg) + encryptor.finalize()

decryptor = cipher.decryptor()
msg_denovo_pad = decryptor.update(msg_cryp) + decryptor.finalize()

# unpadding
unpadder = padding.PKCS7(128).unpadder()
msg_denovo_b = unpadder.update(msg_denovo_pad) + unpadder.finalize()
msg_denovo = msg_denovo_b.decode()

print(msg)
print(msgb)
print(padded_msg)
print(msg_cryp)
print(msg_denovo_pad)
print(msg_denovo_b)
print(msg_denovo)

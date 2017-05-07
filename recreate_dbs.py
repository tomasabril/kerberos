#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 15:34:19 2017

@author: samot
"""

import os
import shelve

print('apagando as databases')

file1 = 'auth_server_db.shelve'
file2 = 'tg_server_db.shelve'
os.remove(file1)
os.remove(file2)

print('recriando as databases')

with shelve.open(file1) as db:
    db['0'] = {}
with shelve.open(file2) as db:
    db['0'] = {}

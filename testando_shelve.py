#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 22:03:05 2017

@author: samot
"""

import shelve

d = {1: ['aloo', 'testando'],
     2: ['numeros aqui', 1, 5, 8],
     3: 'pra ter certeza que mudou'}

with shelve.open('arq_teste.db') as db:
    db['0'] = d
#    saida = db['0']
#print(saida)

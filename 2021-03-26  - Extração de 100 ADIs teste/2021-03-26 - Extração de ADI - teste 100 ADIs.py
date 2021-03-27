# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 10:46:46 2021

@author: Pedro
"""

import requests

adis = []

for item in range(5000, 5100):
    
    temp = requests.get("http://portal.stf.jus.br/processos/listarProcessos.asp?classe=ADI&numeroProcesso=" + str(item)).text
    adis.append(temp)
    print(temp)

nomedoarquivo = 'ADIhtml//ADIs.html'
arquivoaberto = open(nomedoarquivo, 'w', encoding='utf-8')
arquivoaberto.write(adis)
arquivoaberto.close()
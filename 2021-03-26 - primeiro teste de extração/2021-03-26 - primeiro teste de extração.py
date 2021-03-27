# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 10:09:36 2021

@author: Pedro
"""

import requests

teste = requests.get("https://dadosabertos.camara.leg.br/api/v2/deputados/204534/despesas").text

print(teste)

nomedoarquivo = 'ADIhtml//ADI.txt'
arquivoaberto = open(nomedoarquivo, 'w', encoding='utf-8')
arquivoaberto.write(teste)
arquivoaberto.close()
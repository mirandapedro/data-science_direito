# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 10:55:28 2021

@author: Pedro
"""

import requests

incidents = str

for item in range(10, 11):
    
    temp = requests.get("https://www.worldcubeassociation.org/incidents/" + str(item)).text
    print(temp)
    nomedoarquivo = ('incidentes//Incidente ' + str(item) + ".odt")
    arquivoaberto = open(nomedoarquivo, 'w', encoding='utf-8')
    arquivoaberto.write(temp)
    arquivoaberto.close()

print("sucesso")
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 09:53:44 2021

@author: Pedro
"""

lista = ['ADI5000', 'ADPF333', 'MS4333', 'ADO33', 'ADC004', 'MS4300', 'RE98600', 'MS2222']
lista_adi = []
lista_ms = []
outros = []

for item in lista:
    if "ADI" in item:
        lista_adi.append(item)
    
    elif "MS" in item:
        lista_ms.append(item)
        
    else:
        outros.append(item)
        
print(lista_adi)
print(lista_ms)
print(outros)
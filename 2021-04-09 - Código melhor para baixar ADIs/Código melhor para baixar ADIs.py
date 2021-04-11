# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 10:21:30 2021

@author: Pedro
"""

import dsd

# Definição dos parâmetros de busca
Classe = "ADI"
NumeroInicial = 1
NumeroFinal = 10

#iteração para gerar as urls
for n in range (NumeroFinal-NumeroInicial+1):
    
    NumProcesso = str(NumeroFinal-n)
    url = ('http://www.stf.jus.br/portal/peticaoInicial/verPeticaoInicial.asp?base='
           + Classe 
           + '&documento=&s1=1&numProcesso=' 
           + NumProcesso)
    
    arquivo_a_gravar = f'2021-04-09 - ADIs 1 a 10\\{Classe}{str(0)*(4-len(NumProcesso))}{NumProcesso}.txt'

    html = dsd.get(url) 
    
    # redução do texto às variáveis
    inicio = html.find('processo/verProcessoAndamento.asp?')
    html = html[inicio:]

    dsd.gravar_dados_no_arquivo_nome(arquivo_a_gravar, html)

    print (f'Gravado arquivo {arquivo_a_gravar}')
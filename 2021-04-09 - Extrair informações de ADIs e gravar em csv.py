# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 10:29:09 2021

@author: Pedro
"""

import os, dsd
dados_geral = []



for arquivo in os.listdir("2021-04-09 - Código melhor para baixar ADIs")[:10]:
    
    print("Carregado o arquivo " + arquivo)
    nome_arquivo = "2021-04-09 - Código melhor para baixar ADIs//" + arquivo
    arquivo_aberto = dsd.carregar_arquivo(nome_arquivo)
    
    incidente = dsd.extrair(arquivo_aberto, "?incidente=", '"')
    
    requerente_linha = dsd.extrair(arquivo_aberto, "Requerente: <strong>", '<')
    requerente = requerente_linha.replace("\n", "")
    
    requerido_linha = dsd.extrair(arquivo_aberto, "Requerido :<strong>", '<')
    requerido = requerido_linha.replace("\n", "")
    
    dados = [arquivo, incidente, requerente, requerido]
    dados_geral.append(dados)
    
dsd.write_csv_header("2021-04-09 - Código melhor para baixar ADIs//ADIs de uma vez.txt", "arquivo, incidente, requerente, requerido")
dsd.write_csv_lines("2021-04-09 - Código melhor para baixar ADIs//ADIs de uma vez.txt", dados_geral)
    

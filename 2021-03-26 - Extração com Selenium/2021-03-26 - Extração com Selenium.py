# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:18:40 2021

@author: Pedro
"""

from selenium import webdriver

browser = webdriver.Chrome(executable_path='C:\\Users\\Pedro\\Desktop\\chromedriver.exe')
browser.get('http://portal.stf.jus.br/processos/detalhe.asp?incidente=2252302')
sitegeral = browser.page_source

arquivoaberto = open("teste.html", 'w', encoding='utf-8')
arquivoaberto.write(sitegeral)
arquivoaberto.close()

print(sitegeral)


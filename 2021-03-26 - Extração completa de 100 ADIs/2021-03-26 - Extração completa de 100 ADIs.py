# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 11:57:50 2021

@author: Pedro
"""

from selenium import webdriver

for item in range(5000, 5101):

    browser = webdriver.Chrome(executable_path='C:\\Users\\Pedro\\Desktop\\chromedriver.exe')    
    browser.get("http://portal.stf.jus.br/processos/listarProcessos.asp?classe=ADI&numeroProcesso=" + str(item))
    sitegeral = browser.page_source
    nomedoarquivo = ('ADIs tops//ADI ' + str(item) + ".html")
    arquivoaberto = open(nomedoarquivo, 'w', encoding='utf-8')
    arquivoaberto.write(sitegeral)
    arquivoaberto.close()
    browser.close()

print("sucesso")    
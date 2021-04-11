# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 17:20:53 2021

@author: Pedro
"""

import os 
import dsd

path = 'ADIs extraídas\\'
arquivo_a_gravar = 'ADI_versão final top bora bora.txt'
lista = os.listdir(path)
dsd.limpar_arquivo(arquivo_a_gravar)

for nomedoarquivo in lista:

    html = dsd.carregar_arquivo(path+nomedoarquivo)
    html = html.replace(',',';')
    html = html.replace('\n','')
    html = html.replace('  ',' ')
    
    # extrai campo incidente
    incidente = dsd.extrair (html, 
                             'verProcessoAndamento.asp?incidente=',
                             '">')   
    
    # extrai campos classe + liminar + numero
    cln = dsd.extrair(html, 
                      '<div><h3><strong>', 
                      '</strong>')
    
    # extrai numero
    numero = dsd.extrair (cln, ' - ', '')
    numero = dsd.limpar_numero(numero)
    
    # extrai liminar e classe    
    if 'Liminar' in cln:
        liminar = 'sim'
        classe = dsd.extrair(cln, '', ' (Med') 
    else:
        liminar = 'não'
        classe = dsd.extrair(cln, '', ' - ') 
        
    classe.upper()
    classe = classe.replace('ACAO DIRETA DE INCONSTITUCIONALIDADE','ADI')
    classe = classe.replace('AÇÃO DIRETA DE INCONSTITUCIONALIDADE','ADI')
    
    # define dados a gravar
    dados = (incidente, classe, liminar, numero)
    campos = 'incidente, classe, liminar, numero'
    
    # definição de campo: origem     
    origem = dsd.extrair(html,'Origem:</td><td><strong>','</strong>')
    
           
    ## definição de campo: entrada
    entrada = dsd.extrair(html,'Entrada no STF:</td><td><strong>','</strong>')
    
    ## definição de campo: relator
    relator = dsd.extrair(html,'Relator:</td><td><strong>','</strong>')
    relator = relator.replace('MINISTRO ','')
    relator = relator.replace('MINISTRA ','')
    
    
    ## definição de campo: distribuição
    distribuicao = dsd.extrair(html,'Distribuído:</td><td><strong>','</strong>')
    
    
    ## definição de campo: requerente
    requerente = dsd.extrair(html,'Requerente: <strong>','</strong>')
    if '(CF 103, ' in requerente:
        requerentesplit = requerente.split('(CF 103, ')
        requerente = requerentesplit[0]
        requerente = requerente.strip()
        requerentetipo = requerentesplit[1]
        requerentetipo = requerentetipo.replace(')','')
        requerentetipo = requerentetipo.replace('0','')
    else:
        requerentetipo = 'NA'
    
    ## definição de campo: requerido
    requerido = dsd.extrair(html,
                        'Requerido :<strong>',
                        '</strong>')
    
    ## definição de campo: dispositivo questionado
    dispositivoquestionado = dsd.extrair(html,
                                     'Dispositivo Legal Questionado</b></strong><br /><pre>',
                                     '</pre>')
    dispositivoquestionado = dsd.limpar(dispositivoquestionado)
    
    ## definição de campo: resultado da liminar
    resultadoliminar = dsd.extrair(html,
                                   'Resultado da Liminar</b></strong><br /><br />',
                                   '<br />')
    
    ## definição de campo: resultado final
    resultadofinal = dsd.extrair(html,
                                 'Resultado Final</b></strong><br /><br />',
                                 '<br />')
    
    ## definição de campo: decisão monocrática final
    if 'Decisão Monocrática Final</b></strong><br /><pre>' in html:
        decisaomonofinal = dsd.extrair(html,
                                       'Decisão Monocrática Final</b></strong><br /><pre>',
                                       '</pre>')
        decisaomonofinal = dsd.limpar(decisaomonofinal)
    else: 
        decisaomonofinal = 'NA'
         
    ## definição de campo: fundamento    
    if 'Fundamentação Constitucional</b></strong><br /><pre>' in html:
        fundamento = dsd.extrair(html,
                             'Fundamentação Constitucional</b></strong><br /><pre>',
                             '</pre>')
        fundamento = dsd.limpar(fundamento)
    else:
        fundamento = 'NA'
    
    ## definição de campo: fundamento
    if 'Indexação</b></strong><br /><pre>' in html:
        indexacao = dsd.extrair(html,
                            'Indexação</b></strong><br /><pre>',
                            '</pre>')
        indexacao = dsd.limpar(indexacao)        
    else:
        indexacao = 'NA'
    
    ### criação da variável dados extraídos, com uma lista de dados
    dados = [classe, numero, incidente, liminar, origem, entrada, relator,
             distribuicao, requerente, requerentetipo, requerido, 
             dispositivoquestionado, resultadoliminar, resultadofinal, 
             decisaomonofinal, fundamento, indexacao]
    #inserir aqui o conteúdo da lista acima, trocando [] por ''
    campos = '''classe, numero, incidente, liminar, origem, entrada, relator, 
                distribuicao, requerente, requerentetipo, requerido, 
                dispositivoquestionado, resultadoliminar, resultadofinal, 
                decisaomonofinal, fundamento, indexacao'''
                
    campos = campos.replace('\n','')
    campos = campos.replace('             ','')
    campos = campos.replace(',  ',',')
    campos = campos.replace(', ',',')
    campos = campos.replace(', ',',')
    

    
    # grava dados
    if classe != 'NA':
        dsd.write_csv_header(arquivo_a_gravar, campos)
        dsd.write_csv_line(arquivo_a_gravar, dados)
            
    print (classe + numero) 
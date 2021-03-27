import dsd

# Definição dos parâmetros de busca
Classe = "ADI"
NumeroInicial = 1
NumeroFinal = 50
dominio = 'http://portal.stf.jus.br/processos/'


#iterador para buscar os processos
for vezes in range (NumeroFinal-NumeroInicial+1):
    
    dsd.esperar(1,5,vezes)

 
    NumProcesso = str(NumeroFinal-vezes)
           
    # requisição das informações
    html = dsd.solicitar_dados_AP(Classe, NumProcesso)
    
    # extrai campo incidente do html
    incidente = dsd.extrair(html,'id="incidente" value="', '">')

    # extrai dados dos URLs
    
    partes       = dsd.solicitar_dados(dominio,
                                     'abaPartes.asp?incidente=', 
                                     incidente)
    
    informacoes  = dsd.solicitar_dados(dominio, 
                                     'abaInformacoes.asp?incidente=', 
                                     incidente)
    
    andamentos  = dsd.solicitar_dados(dominio,
                                     'abaandamentos.asp?incidente=', 
                                     (incidente +'&imprimir=1'))
    
    pauta       = dsd.solicitar_dados(dominio,
                                     'abapautas.asp?incidente=',
                                     incidente)
    
    sessao      = dsd.solicitar_dados(dominio, 
                                     'abasessao.asp?incidente=', 
                                     incidente)
    
    decisoes    = dsd.solicitar_dados(dominio, 
                                     'abadecisoes.asp?incidente=', 
                                     incidente)
    
    deslocamentos= dsd.solicitar_dados(dominio, 
                                     'abadeslocamentos.asp?incidente=', 
                                     incidente)
    
    peticoes    = dsd.solicitar_dados(dominio, 
                                     'abapeticoes.asp?incidente=', 
                                     incidente)
    
    recursos     =dsd.solicitar_dados(dominio, 
                                      'abarecursos.asp?incidente=', 
                                      incidente)
    
    if (Classe == 'ADI' 
        or Classe == 'ADPF' 
        or Classe == 'ADO' 
        or Classe == 'ADC'):
        cc = dsd.solicitar_dados_CC(Classe, NumProcesso)
    else:
        cc = 'NA'
    
    # define dados a serem gravados
    dados = ('incidente=' + incidente + 'fonte>>>>' +html + 
             'partes>>>>' + partes + 'informacoes>>>>' + informacoes + 
             'andamentos>>>>' + andamentos + 'pauta>>>>' + pauta + 
             'sessao>>>>' + sessao + 'decisoes>>>>' + decisoes + 
             'deslocamentos>>>>' + deslocamentos + 'peticoes>>>>' + 
             peticoes + 'recursos>>>>' + recursos + 'cc>>>>' + cc)
             
    # função de gravação
    dsd.gravar_dados_no_arquivo (Classe, NumProcesso, 'ADItotal\\', dados)
    
    
    print (f'Gravado arquivo {Classe+NumProcesso}')

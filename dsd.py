import csv
import requests
import time
import os
from unicodedata import normalize

def position1(list):
    return(list[1])

def csv_to_list(file):
    lista = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            lista.append(row)
    return (lista[1:])

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('utf-8')

def extrair(fonte,MarcadorInicio, MarcadorFim):
    if MarcadorInicio not in fonte:
        return 'NA'
    else:
        inicio = fonte.find(MarcadorInicio) + len(MarcadorInicio)
        fim = fonte.find(MarcadorFim, inicio)
        if  MarcadorFim == '' or fim == -1:
            return fonte[inicio:]
        elif MarcadorInicio == '':
            return fonte[:fim]
        else:
            return fonte[inicio:fim]

def extrair_campo_lista (string, split, lista_inicio_fim):
    # define o número de elementos a serem extraídos
    n_elementos= string.count(split)

    # cria uma lista (dados) com os dados da string, segmentada no split
    elementos = string.split(split)
    elementos = elementos[1:]

    # imprime o número de elementos a serem extraídos
    # print (str(n_elementos) + ' elementos')

    #define a lista que será retornada como resultado
    campo_lista = []

    # iteração sobre cada um dos n elementos
    for item in range(n_elementos):

        # carrega na variável campo um elemento de cada vez
        campo = elementos[item]
        # print (campo)
        # redefine a lista elemento_lista
        elemento_lista = []

        # insere no elemento o número de ordem, iniciando em 1
        elemento_lista.append(['ORDEM', str(item+1)])

        # identifica os atributos de cada elemento
        for elemento in range(len(lista_inicio_fim)):
            # extrai os marcadores da lista
            marcadores = lista_inicio_fim[elemento]
            atributo = marcadores[0].upper()
            inicio = marcadores[1]
            fim = marcadores[2]

            # extrai o atributo a partir dos marcadores
            dado = ''
            dado = extrair(campo, inicio, fim)
            dado = limpar(dado)
            dado = limpar(dado)
            dado = remover_acentos(dado)

            elemento_lista.append([atributo, dado.upper()])
        # acrescenta o elemento extraído na lista que compõe o campo
        campo_lista.append(elemento_lista)

    # retorna a lista de elementos como resultado função
    return campo_lista

def ajustar_nome(string):
    string.strip()
    
    trocar1 =[['ASSOC ','ASSOCIACAO '],
            ['GONGRESSO NACIONAL','CONGRESSO NACIONAL'],
            ['REPUBICA','REPUBLICA'],
            ['PROCURADOR GERAL','PROCURADOR-GERAL'],
            ['REUBLICA','REPUBLICA'],
            ['GONGRESSO','CONGRESSO'],
            ['(','- '],
            [')',''],
            ['  ',' '],
            ['MINISTRA','MINISTRO'],
            ['PRO-BELEZA','PROBELEZA'],
            ['VICE-GOV','V.GOV'],
            ['VICE PRESIDENTE','VICE-PRESIDENTE'],
            ['VICE-PRE','V.PRE'],
            ['CORREGEDOR-GERAL','CORR.GERAL'],
            ['CORREGEDORIA-GERAL','CORR.GERAL'],
            ['CORREGEDORIAGERAL','CORR.GERAL'],
            ['CORREGEDORIADA','CORR.GERAL DA'],
            ['ARCO-IRIS','ARCOIRIS'],
            ['TRT - ','TRT '],
            ['REGIAO -','REGIAO'],
            ['MATO-GROSSENSE','MATOGROSSENSE'],
            ['TRT - ','TRT '],
            
            ['-',' - '],
            ['  ',' '],
            ['  ',' '],
            [']',''],
            
            ['- ME',''],
            ['S/A','S.A.'],
            ['LTDA.','LTDA'],
            ['PREFEITA','PREFEITO'],
            ['PREFEITO DO MUNICIPIO','PREFEITO'],
            ['PREFEITO D', 'PREF. D'],
            ['PREFEITO MUNICIPAL D','PREF. D'],
            ['PREFEITURA D','PREF. D'],
            ['PREFEITURA MUNICIPAL','PREF.'],
            ['MUNICIPIO D','MUN. D'],
            ['MINISTRO D','MIN. D'],
            ['MINISTERIO D','MIN. D'],
            ['MESA DIRETIVA','MESA DIRETORA'],
            ['MESA DIRETORA','M.D.'],
            ['MESA DA','M.D. DA'],
            ['SENADO FEDERAL','SENADO'],
            ['JUIZ DE DIREITO','JUIZ'],
            ['CORREGEDOR ','CORREGEDORIA'],
            ['CORREGEDORIA ','CORREG. '],
            ['CAMARA DE VEREADORES','CAMARA MUNICIPAL'],
            ['CAMARA MUNICIPAL','C.MUN.'],
            ['C.MUN. DO MUNICIPIO','C.MUN.'],
            ['CAMPINHAS','CAMPINAS'],
            ['DE TOCANTINS','DO TOCANTINS']
            
            
            
            # ['/ALAGOAS', '/AC'],
            # ['/ALAGOAS', '/AL'],
            # ['/AMAPA', '/AP'],
            # ['/AMAZONAS', '/AM'],
            # ['/BAHIA', '/BA'],
            # ['/CEARA', '/CE'],
            # ['/DISTRITO FEDERAL', '/DF'],
            # ['/ESPIRITO SANTO', '/ES'],
            # ['/GOIAS', '/GO'],
            # ['/MARANHAO', '/MA'],
            # ['/MATO GROSSO DO SUL', '/MS'],
            # ['/MATO GROSSO', '/MT'],
            # ['/MINAS GERAIS', '/MG'],
            # ['/PARAIBA', '/PB'],
            # ['/PARANA', '/PR'],
            # ['/PERNAMBUCO', '/PE'],
            # ['/PIAUI', '/PI'],
            # ['/RIO DE JANEIRO', '/RJ'],
            # ['/RIO GRANDE DO NORTE', '/RN'],
            # ['/RIO GRANDE DO SUL', '/RS'],
            # ['/RONDONIA', '/RO'],
            # ['/RORAIMA', '/RR'],
            # ['/SANTA CATARINA', '/SC'],
            # ['/SAO PAULO', '/SP'],
            # ['/SERGIPE', '/SE'],
            # ['/PARA', '/PA'],
            # ['/TOCANTINS', '/TO'],
            # ['/ACRE','/AC'],
            # ['/RIO DE JANEIRO','/RJ']
            ]
    for item in trocar1:
        string = string.replace(item[0],item[1])
        
        
    if 'DEMOCRATAS' in string and 'DEM ' in string:
        string = 'DEM/PFL'
    if 'DEMOCRATAS -' in string:
        string = 'DEM/PFL'
    if 'DEMOCRATAS' == string:
        string = 'DEM/PFL'
    
    
    substituir = [
              ['PROCURADOR - GERAL DA REPUBLICA','PGR'],
              ['PROCURADOR GERAL DA REPUBLICA','PGR'],
              ['PROCURADORA - GERAL DA REPUBLICA','PGR'],
              ['PROCURADORIA - GERAL DA REPUBLICA','PGR'],
              ['CONSELHO FEDERAL DA ORDEM DOS ADVOGADOS DO BRASIL','OAB'],
              ['PARTIDO PROGRESSISTA','PP'],
              ['PARTIDO COMUNISTA DO BRASIL','PC DO B'],
              ['PARTIDO COMUNISTA BRASILEIRO','PCB'],
              ['PARTIDO DA FRENTE LIBERAL','DEM/PFL'],
              ['PARTIDO DA MOBILIZACAO NACIONAL','PMN'],
              ['PARTIDO DA MULHER BRASILEIRA','PMB'],
              ['REEDIFICACAO DA ORDEM NACIONAL','PRONA'],
              ['PARTIDO DA REPUBLICA','PR'],
              ['DEMOCRACIA BRASILEIRA','PSDB'],
              ['PSDB','PSDB'],
              ['DEMOCRATA CRISTAO','PDC'],
              ['PARTIDO DEMOCRATICO TRABALHISTA','PDT'],
              ['PARTIDO DO MOVIMENTO DEMOCRATICO','PMDB'],
              ['TRABALHADORES DO BRASIL','PT DO B'],
              ['PARTIDO TRABALHISTA DO BRASIL','PT DO B'],
              ['PARTIDO DOS TRABALHADORES','PT'],
              ['PARTIDO HUMANISTA DA SOLIDARIEDADE','PHS'],
              ['PARTIDO LIBERAL','PL'],
              ['PARTIDO POPULAR SOCIAL','PPS'],
              ['PARTIDO PROGRESSISTA BRASILEIRO','PPB'],
              ['PARTIDO PROGRESSISTA REFORMADOR','PPR'],
              ['PARTIDO PROGRESSISTA','PP'],
              ['RENOVADOR TRABALHISTA BRASILEIRO','PRTB'],
              ['PARTIDO REPUBLICANO BRASILEIRO','PRB'],
              ['REPUBLICANO DA ORDEM SOCIAL','PROS'],
              ['PARTIDO REPUBLICANO PROGRESSISTA','PRP'],
              ['PARTIDO SOCIAL CRISTAO','PSC'],
              ['PARTIDO SOCIAL DEMOCRATA CRISTAO','PSDC'],
              ['PARTIDO SOCIAL DEMOCRATICO','PSD'],
              ['PARTIDO SOCIAL LIBERAL','PSL'],
              ['PARTIDO SOCIAL TRABALHISTA','PST'],
              ['SOCIALISMO E LIBERDADE','PSOL'],
              ['PARTIDO SOCIALISTA BRASILEIRO','PSB'],
              ['PARTIDO SOCIALISTA DO BRASIL','PSB'],
              ['PARTIDO SOCIALISTA DOS TRABALHADORES UNIFICADO','PSTU'],
              ['PARTIDO TRABALHISTA BRASILEIRO','PTB'],
              ['PARTIDO TRABALHISTA CRISTAO','PTC'],
              ['PARTIDO TRABALHISTA NACIONAL','PTN'],
              ['PARTIDO TRABALHISTA RENOVADOR','PTR'],
              ['PARTIDO VERDE','PV'],
              ['PODEMOS','PODEMOS'],
              ['CONSELHO NACIONAL DE JUSTIÇA','CNJ'],
              ['CONGRESSO NACIONAL','CN'],
              ['TRIBUNAL SUPERIOR ELEITORAL','TSE'],
              ['SOLIDARIEDADE -','SOLIDARIEDADE'],
              ['PARTIDO NOVO','PARTIDO NOVO'],
              ['SUPREMO TRIBUNAL FEDERAL','STF'],
              ['^',''],
              ['TRIBUNAL SUPERIOR DO TRABALHO','TST']
                         
              ]
    
    for item in substituir:
        if item[0] in string:
            string = item[1]
    
    if string.find('ASSOCIACAO') > 0 and string.find('-') < 20:
        string = string.replace('-','')
        string = string.replace('  ',' ')
        string = string.replace('  ',' ')
        string = string[string.find('ASSOCIACAO'):] + ' - ' + string[:string.find('ASSOCIACAO')]
        
    if string.find('UNIAO D') > 0 and string.find('-') < 20:
        string = string.replace('-','')
        string = string.replace('  ',' ')
        string = string.replace('  ',' ')
        string = string[string.find('UNIAO'):] + ' - ' + string[:string.find('UNIAO')]
        
    if string.find('CONFEDERACAO') > 0 and string.find('-') < 20:
        string = string.replace('-','')
        string = string.replace('  ',' ')
        string = string.replace('  ',' ')
        string = string[string.find('CONFEDERACAO'):] + ' - ' + string[:string.find('CONFEDERACAO')]
        
    if string.find('FEDERACAO') > 0 and string.find('-') < 20 and 'CONFEDERACAO' not in string:
        string = string.replace('-','')
        string = string.replace('  ',' ')
        string = string.replace('  ',' ')
        string = string[string.find('FEDERACAO'):] + ' - ' + string[:string.find('FEDERACAO')]
        
    if string.find('CONSELHO') > 0 and string.find('-') < 20:
        string = string.replace('-','')
        string = string.replace('  ',' ')
        string = string.replace('  ',' ')
        string = string[string.find('CONSELHO'):] + ' - ' + string[:string.find('CONSELHO')]
        
    if 'ESTADO DO ' in string[0:12]:
        string.replace('ESTADO DO ','')
    
    if 'ESTADO DE ' in string[0:12]:
        string.replace('ESTADO DE ','')
        
    if 'ESTADO DA ' in string[0:12]:
        string.replace('ESTADO DA ','')
        
    # estados = [[' DO AC','/AC'],
    #          [' DE AL','/AL'],
    #          [' DO AP','/AP'],
    #          [' DO AM','/AM'],
    #          [' DA BA','/BA'],
    #          [' DO CE','/CE'],
    #          [' DO DF','/DF'],
    #          [' DE GO','/GO'],
    #          [' DO MA','/MA'],
    #          [' DO MS','/MS'],
    #          [' DO MT','/MT'],
    #          [' DE MG','/MG'],
    #          [' DA PB','/PB'],
    #          [' DE PE','/PE'],
    #          [' DO PI','/PI'],
    #          [' DO RJ','/RJ'],
    #          [' DO RN','/RN'],
    #          [' DO RS','/RS'], 
    #          [' DE RO','/RO'],
    #          [' DE RR','/RR'],
    #          [' DE SC','/SC'],
    #          [' DE SP','/SP'],
    #          [' DO PA','/PA'],
    #          [' DE TO','/TO'],
    #          [' DO TO','/TO'],
    #          [' DO ES','/ES']]
    
    # for item in estados:
    #     final = string[-6:0]
    #     if  final == item[0]:
    #         string = string.replace(item[0],item[1])
    
    # estados2 = [[' DO AC','/AC'],
    #          [' AL','/AL'],
    #          [' AP','/AP'],
    #          [' AM','/AM'],
    #          [' BA','/BA'],
    #          [' CE','/CE'],
    #          [' DF','/DF'],
    #          [' GO','/GO'],
    #          [' MA','/MA'],
    #          [' MS','/MS'],
    #          [' MT','/MT'],
    #          [' MG','/MG'],
    #          [' PB','/PB'],
    #          [' PE','/PE'],
    #          [' PI','/PI'],
    #          [' RJ','/RJ'],
    #          [' RN','/RN'],
    #          [' RS','/RS'], 
    #          [' RO','/RO'],
    #          [' RR','/RR'],
    #          [' SC','/SC'],
    #          [' SP','/SP'],
    #          [' PA','/PA'],
    #          [' TO','/TO'],
    #          [' TO','/TO'],
    #          [' ES','/ES']]
    
    # for item in estados2:
    #     final = string[-6:0]
    #     if  final == item[0]:
    #         string = string.replace(item[0],item[1])
            
    string = estado_nome_completo(string)

    trocar = [['ASSEMBLEIA LEGISLATIVA DO ESTADO DE ', 'AL/'],
             ['ASSEMBLEIA LEGISLATIVA DO ESTADO DA ', 'AL/'],
             ['ASSEMBLEIA LEGISLATIVA DO ESTADO DO ', 'AL/'],
             ['ASSEMBLEIA LEGISLATIVA DO','AL/'],
             ['ASSEMBLEIA LEGISLATIVA DE','AL/'],
             ['ASSEMBLEIA LEGISLATIVA DA','AL/'],
             ['ASSEMBLEIA LEGISLATIVA','AL/'],
             ['CONSELHO FEDERAL', 'CONS.FED'],
             ['CONSELHO', 'CONS.'],
             ['TRIBUNAL REGIONAL ELEITORAL','TRE'],
             ['MINISTERIO PUBLICO','MP'],
             ['ASSOCIACAO NACIONAL', 'ASSOC.NAC.'],
             ['ASSOCIACAO', 'ASSOC.'],
             ['CONFEDERACAO NACIONAL', 'CONF.NAC.'],
             ['CONFEDERACAO BRASILEIRA', 'CONF.BRAS.'],
             ['CONFEDERACAO', 'CONF.'],
             ['DO ESTADO ',''],
             ['GOVERNADORA','GOVERNADOR'],
             ['GOVERNADOR DE ','GOV./ '],
             ['GOVERNADOR DO ','GOV./ '],
             ['GOVERNADOR DA ','GOV./ '],
             ['SECRETARIO','SECRETARIA'],
             ['(0','('],
             ['(0','('],
             ['TRIBUNAL REGIONAL DO TRABALHO','TRT'],
             ['TRIBUNAL REGIONAL FEDERAL','TRF'],
             ['TRIBUNAL DE JUSTICA','TJ'],
             ['PROCURADORA','PROCURADOR'],
             ['PROCURADOR-GERAL DE ','PG/'],
             ['PROCURADOR-GERAL DO ','PG/'],
             ['PROCURADOR-GERAL DA ','PG/'],
             ['DF/DF','/DF'],
             ['PRESIDENTA','PRESIDENTE'],
             ['SANTANA CATARINA','SANTA CATARINA'],
             ['MINAS DE GERAIS','MINAS GERAIS'],
             ['A REGIAO','REG.'],
             ['A. REGIAO','REG.'],
             ['TRT DA','TRT'],
             ['TRF DA','TRT'],
             ['SECRETARIA DE FAZENDA','SEC.FAZ.'],
             ['SECRETARIA DA FAZENDA','SEC.FAZ.'],
             ['PRESIDENTE DO','PRES.'],
             ['PRESIDENTE DA','PRES.'],
             ['TRIBUNAL DE CONTAS DO','TC/'],
             ['TRIBUNAL DE CONTAS DE','TC/'],
             ['TRIBUNAL DE CONTAS DA','TC/'],
             ['TRIBUNAL DE CONTAS','TC'],
             ['/ ','/'],
             [' /','/'],
             ['//','/'],
             ['DEFENSORIA PUBLICA','DP'],
             ['DEFENSOR PUBLICO GERAL', 'DP.GERAL'],
             ['DEFENSOR PUBLICO-GERAL', 'DP.GERAL'],
             ['ESTADO/',''],
             ['ESTADO DE',''],
             ['JUIZ DO TRABALHO','JUIZ'],
             ['E OUTROS',''],
             ['E OUTRO',''],
             ['E OUTRA',''],
             ['E OUTRAS',''],
             ['MINISTRO DE ESTADO','MINISTRO'],
             ['SECRETARIA DE ESTADO','SECRETARIA'],
             ['SINDICADO DOS EMPREGADOS','SIND.EMPREG.'],
             ['DE MATO GROSSO DO SUL','DO MATO GROSSO DO SUL'],
             ['CONS. DA MAGISTRATURA','CONS.MAGIST.'],
             ['CONS. ESTADUAL','CONS.ESTAD.'],
             ['CONS. NACIONAL','CONS.NAC.'],
             ['CONS. REGIONAL','CONS.REG.'],
             ['CONS. SUPERIOR','CONS.SUP.'],
             ['CORREGEDORIAGERAL','CORR.GERAL'],
             ['CORREG. GERAL','CORR.GERAL'],
             ['DEFENSOR PUBLICO - GERAL','DP.GERAL'],
             ['DIRETOR - GERAL','D.G.'],
             ['FEDERACAO BRASILEIRA','FED.BRAS.'],
             ['FEDERACAO DAS ASSOCIACOES','FED.ASSOC.'],
             ['FEDERACAO NACIONAL DOS SERVIDORES','FED.NAC.SERV.'],
             ['FEDERACAO NACIONAL DOS TRABALHADORES','FED.NAC.TRAB.'],
             ['FEDERACAO NACIONAL','FED.NAC.'],
             ['INSTITUTO BRASILEIRO','INST.BRAS.'],
             ['ORGAO ESPECIAL DO',''],
             ['SINDICATO NACIONAL DE','SIND.NAC.'],
             ['SINDICATO NACIONAL DOS','SIND.NAC.'],
             ['SINDICATO NACIONAL DAS','SIND.NAC.'],
             ['SINDICATO NACIONAL','SIND.NAC.'],
             ['MIN. DE ESTADO','MIN.'],
             ['ORDEM DOS ADVOGADOS DO BRASIL','OAB'],
             ['PROCURADOR - GERAL','PROC.GERAL'],
             ['PROCURADOR GERAL DA REPUBLICA','PGR'],
             ['PROCURADOR GERAL','PROC.GERAL'],
             ['PROCURADORIA GERAL','PROC.GERAL'],
             ['SUPERIOR TJ','STJ'],
             
             ]
    
    for item in trocar:
        string = string.replace(item[0],item[1])
    
    if string[:2] == 'A ':
        string = string[2:]
        
    if string[:8] == 'ESTADO D':
        string = string[10:]
        
    string.strip(',')
    string.strip()
    
    return string

def extrair_partes(string):
    string = remover_acentos(string)
    
    partes = string.split('<div class="processo-partes lista-dados">')
    
    n=0
    lista_partes = []
    
    for parte in partes[1:]:
        n = n+1
        ordem = n
        tipo = extrair(parte, 'detalhe-parte">', '</div>').upper()
        tipo = tipo.replace('REQTE.(S)','REQTE')
        tipo = tipo.replace('INTDO.(A/S)','INTDO')
        tipo = tipo.replace('ADV.(A/S)','ADV')
        tipo = tipo.replace('AM. CURIAE.','AMICUS')
        nome = extrair(parte, '"nome-parte">', '&nbsp').upper()
        nome = ajustar_nome(nome)
        if tipo == 'ADV':
            if "(" in nome:
                nome = extrair(nome, '', '(')
        if tipo == 'RQTE':
            lista_partes.append([ordem, tipo, nome])
        
    return lista_partes

def listar_partes(string, processo):
    string = remover_acentos(string)
    
    partes = string.split('<div class="processo-partes lista-dados">')
    
    lista_partes = []
    
    for parte in partes[1:]:
        tipo = extrair(parte, 'detalhe-parte">', '</div>').upper()
        tipo = tipo.replace('REQTE.(S)','REQTE')
        tipo = tipo.replace('INTDO.(A/S)','INTDO')
        tipo = tipo.replace('REQDO.(A/S)','INTDO')
        tipo = tipo.replace('ADV.(A/S)','ADV')
        tipo = tipo.replace('AM. CURIAE.','AMICUS')
        tipo = tipo.replace('PROC.(A/S)(ES)','ADV/PUB')
        nome = extrair(parte, '"nome-parte">', '&nbsp').upper()
        nome = ajustar_nome(nome)
        if tipo == 'ADV' or tipo == 'ADV/PUB':
            if "(" in nome:
                nome = extrair(nome, '', '(')
        nome = nome.strip()
        nome = nome.replace('  ',' ')
        lista_partes.append([nome, tipo, processo])
        
    return lista_partes


def extrair_andamentos(string):
    string = remover_acentos(string)
    string = limpar(limpar(string))
    partes = string.split('<div class="andamento-item">')
    
    n=0
    lista_andamentos = []
    
    for parte in partes[1:]:
        n = n+1
        ordem = n
        data = extrair(parte, '<div class="andamento-data ">','</div>').upper()
        nome = extrair(parte, '<h5 class="andamento-nome ">','</h5>').upper()
        complemento = extrair(parte, '<div class="col-md-9 p-0">','</div>').upper()
        if complemento == ' ' or complemento == '':
            complemento = 'NA'
        docs = extrair(parte, '"col-md-4 andamento-docs">','</div>')
        if docs == ' ' or docs == '':
            docs = 'NA'
        if 'href=' in docs:
            docs = extrair(docs,'href="', '"')
        julgador = extrair(parte, 'julgador badge bg-info ">','</span>').upper()
        #print ([ordem, data, nome, complemento, docs, julgador])
        
        lista_andamentos.append([ordem, data, nome, complemento, docs, julgador])
        
    return lista_andamentos


def solicitar_dados_Juris (classe, numero):
    url = ('http://stf.jus.br/portal/jurisprudencia/listarJurisprudencia.asp?s1=%28'
           + classe
           +'%24%2ESCLA%2E+E+'
           + numero
           + '%2ENUME%2E%29+OU+%28'
           + classe +
           ' %2EACMS%2E+ADJ2+'
           + numero
           + '%2EACMS%2E%29&base=baseAcordaos')

    print (url)
    # Módulo básico de extração
    string = requests.get(url).text
    inicio = string.find('<a href="#" id="imprimir" onclick="sysImprimir(); return false;">Imprimir</a>')
    return (url + ">>>>> \n" + string[inicio:])

def solicitar_dados_CC (classe, numero):
    url = ('http://www.stf.jus.br/portal/peticaoInicial/verPeticaoInicial.asp?base='
           + classe
           + '&documento=&s1=1&numProcesso='
           + numero)
    print (url)
    # Módulo básico de extração
    string = requests.get(url).text
    inicio = string.find('processo/verProcessoAndamento.asp?')
    return (url + ">>>>> \n" + string[inicio:])

def solicitar_dados_mono (classe, numero):
    url = ('http://stf.jus.br/portal/jurisprudencia/listarJurisprudencia.asp?s1=%28'
           + classe
           +'%24%2ESCLA%2E+E+'
           + numero
           + '%2ENUME%2E%29+NAO+S%2EPRES%2E&base=baseMonocraticas')

    print (url)
    # Módulo básico de extração
    string = requests.get(url).text
    inicio = string.find('<a href="#" id="imprimir" onclick="sysImprimir(); return false;">Imprimir</a>')
    return (url + ">>>>> \n" + string[inicio:])

def solicitar_dados_AP (classe, numero):
    url = ('http://portal.stf.jus.br/processos/listarProcessos.asp?classe='
           + classe
           + '&numeroProcesso='
           + numero)
    string = requests.get(url)
    string.encoding = 'utf-8'
    htmlfonte = string.text
    htmlfonte = extrair(htmlfonte,
                        '<div class="processo-titulo m-b-8">',
                        '<div class="p-l-0" id="resumo-partes">')
    return (url + ">>>>> \n" + htmlfonte)

def solicitar_dados (dominio, path, incidente):
    html = requests.get(dominio+path+incidente)
    html.encoding = 'utf-8'
    html = html.text
    return html


def carregar_arquivo_composto (classe, numero, path):
    nomedoarquivo = (path + classe + str(0)*(4-len(numero)) + numero + '.html')
    arquivoaberto = (classe +  str(0)*(4-len(numero)) + numero + '.html')
    print (nomedoarquivo)
    arquivo = open(nomedoarquivo, 'r', encoding='utf-8')
    html = arquivo.read()
    arquivo.close()
    return arquivoaberto, html

def gerador_de_lista (path, classe, numeroinicial, numerofinal):
    lista = []
    for n in range (int(numerofinal) - int(numeroinicial) + 1):
        numero = numerofinal-n
        nomedoarquivo = (path + classe + str(0)*(4-len(str(numero))) + str(numero) + '.html')
        if nomedoarquivo in os.listdir(path):
            lista.append(nomedoarquivo)
    return lista

def gerar_lista (classe, numeroinicial, numerofinal, path):
    lista = []
    for item in range(int(numerofinal) - int(numeroinicial) +1):
        nomedoarquivo = (path + classe + ('0')*(4-len(str(item))) + str(item) + '.html')
        print (nomedoarquivo)
        lista.append(nomedoarquivo)
    return (lista)

def gerar_nome_arquivo (classe, numero, path):
    nomedoarquivo = (path + classe + str(0)*(4-len(numero)) + numero + '.html')
    return (nomedoarquivo)

def carregar_arquivo (nomedoarquivo):
    arquivo = open(nomedoarquivo, 'r', encoding='utf-8')
    html = arquivo.read()
    arquivo.close()
    return html

def gravar_dados_no_arquivo (classe, numero, path, dados):
    nomedoarquivo = (path + classe + str(0)*(4-len(numero)) + numero + '.html')
    arquivo = open(nomedoarquivo, 'w', encoding='utf-8')
    arquivo.write(dados)
    arquivo.close

def gravar_dados_no_arquivo_nome (nomedoarquivo, dados):
    arquivo = open(nomedoarquivo, 'w', encoding='utf-8')
    arquivo.write(dados)
    arquivo.close

def extrair_da_lista (relacao_de_arquivos, path):
    nomedoarquivo = relacao_de_arquivos.pop()
    arquivo = open(path + nomedoarquivo, 'r', encoding='utf-8')
    html = arquivo.read()
    arquivo.close()
    return nomedoarquivo, html

def limpa_estado(string):
    estados = [['ALAGOAS', '/AC'],
     ['ALAGOAS', '/AL'],
     ['AMAPA', '/AP'],
     ['AMAZONAS', '/AM'],
     ['BAHIA', '/BA'],
     ['CEARA', '/CE'],
     ['DISTRITO FEDERAL', '/DF'],
     ['ESPIRITO SANTO', '/ES'],
     ['GOIAS', '/GO'],
     ['MARANHAO', '/MA'],
     ['MATO GROSSO DO SUL', '/MS'],
     ['MATO GROSSO', '/MT'],
     ['MINAS GERAIS', '/MG'],
     ['PARAIBA', '/PB'],
     ['PARANA', '/PR'],
     ['PERNAMBUCO', '/PE'],
     ['PIAUI', '/PI'],
     ['RIO DE JANEIRO', '/RJ'],
     ['RIO GRANDE DO NORTE', '/RN'],
     ['RIO GRANDE DO SUL', '/RS'],
     ['RONDONIA', '/RO'],
     ['RORAIMA', '/RR'],
     ['SANTA CATARINA', '/SC'],
     ['SAO PAULO', '/SP'],
     ['SERGIPE', '/SE'],
     ['PARA', '/PA'],
     ['TOCANTINS', '/TO']
     ]
    
    for item in estados:
        string = string.replace(item[0],item[1])
    return string

def estado_nome_completo(string):
    estados = [['ALAGOAS', '/AC'],
     ['ALAGOAS', '/AL'],
     ['AMAPA', '/AP'],
     ['AMAZONAS', '/AM'],
     ['BAHIA', '/BA'],
     ['CEARA', '/CE'],
     ['DISTRITO FEDERAL', '/DF'],
     ['ESPIRITO SANTO', '/ES'],
     ['GOIAS', '/GO'],
     ['MARANHAO', '/MA'],
     ['MATO GROSSO DO SUL', '/MS'],
     ['MATO GROSSO', '/MT'],
     ['MINAS GERAIS', '/MG'],
     ['PARAIBA', '/PB'],
     ['PARANA', '/PR'],
     ['PERNAMBUCO', '/PE'],
     ['PIAUI', '/PI'],
     ['RIO DE JANEIRO', '/RJ'],
     ['RIO GRANDE DO NORTE', '/RN'],
     ['RIO GRANDE DO SUL', '/RS'],
     ['RONDONIA', '/RO'],
     ['RORAIMA', '/RR'],
     ['SANTA CATARINA', '/SC'],
     ['SAO PAULO', '/SP'],
     ['SERGIPE', '/SE'],
     ['PARA', '/PA'],
     ['TOCANTINS', '/TO']
     ]
    
    for item in estados:
        string = string.replace(item[1],item[0])
    return string
def siglas():
    return ['AC',
 'AL',
 'AP',
 'AM',
 'BA',
 'CE',
 'DF',
 'ES',
 'GO',
 'MA',
 'MS',
 'MT',
 'MG',
 'PB',
 'PR',
 'PE',
 'PI',
 'RJ',
 'RN',
 'RS',
 'RO',
 'RR',
 'SC',
 'SP',
 'SE',
 'PA',
 'TO']      
 
#   funções de limpeza
def limpar(fonte):
    fonte = fonte.replace('\n',' ')
    fonte = fonte.replace('  ',' ')
    fonte = fonte.replace('  ',' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip('"')
    fonte = fonte.lstrip('>')
    fonte = fonte.replace('  ',' ')
    fonte = fonte.replace('\t', '')
    fonte = fonte.replace('/#','')
    fonte = fonte.strip(' ')
    fonte = fonte.strip(' ')       
    fonte = fonte.strip('-')
    fonte = fonte.strip(' ')       
    fonte = fonte.strip(' ')       
    fonte = fonte.strip(' ')
    return fonte

def limpar_numero(numero):
    numero = numero.replace('<FONT COLOR=RED><B>','')
    numero = numero.replace('</B></FONT>','')
    numero = "0"*(4-len(numero))+numero
    return numero

def limpar_classe(string):
    string = limpar(string)
    string = string.replace('ACAO DIRETA DE INCONSTITUCIONALIDADE','ADI')
    string = string.replace('ACAO DIRETA DE INCONSTITUCI0NALIDADE','ADI')
    string = string.replace('7CAO DIRETA DE INCONSTITUCIONALIDADE','ADI')
    string = string.replace('01CAO DIRETA DE INCONSTITUCIONALIDADE','ADI')
    string = string.replace('CAO DIRETA DE INCONSTITUCIONALIDADE','ADI')
    string = string.replace('PACAO DIRETA DE INCONSTITUCIONALIDADE','ADI')
    string = string.replace('sACAO DIRETA DE INCONSTITUCIONALIDADE','ADI')
    string = string.replace('ARGUICAO DE DESCUMPRIMENTO DE PRECEITO FUNDAMENTAL','ADPF')
    
            
def limpar_cln(string):
    string = string.upper()
    string = remover_acentos(string)
    string = string.replace ('( MED','(MED')
    string = string.replace ('E(MED','E (MED')
    string = string.replace ('(LIMINAR)','(MED. LIMINAR)')
    string = string.replace ('E MED.','E (MED')
    string = string.replace ('CAUTELAR','LIMINAR')
    
def limpar_decisao (string):
    string = string.replace('\n','')
    string = string.replace('\t','')
    string = string.replace('     ','')
    string = string.replace('  ',' ')
    string = string.upper()
    string = remover_acentos(string)
    return string

def limpar_arquivo(nomedoarquivo):
    arquivoaberto =     open(nomedoarquivo, mode='w',
                             encoding="utf-8", newline='')
    arquivoaberto.close()

def write_csv_header (nomedoarquivo, string_campos):
    lista_de_campos = string_campos.split(',')
    if nomedoarquivo in os.listdir():
        arquivoaberto = open(nomedoarquivo, mode='r+',
                                 encoding="utf-8", newline='')
        html = arquivoaberto.read()
        arquivoaberto.close()

        
        if lista_de_campos[0] not in html[:100]:
            arquivoaberto = open(nomedoarquivo, mode='w',
                                 encoding="utf-8", newline='')
            arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',')
            arquivoaberto_csv.writerow(lista_de_campos)
            arquivoaberto.close()
    else:
            arquivoaberto = open(nomedoarquivo, mode='w',
                                 encoding="utf-8", newline='')
            arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',')
            arquivoaberto_csv.writerow(lista_de_campos)
            arquivoaberto.close()



def esperar (segundos, ciclos, variavel0):
    if variavel0%ciclos == 0 and variavel0 != 0:
        print ('espera ' + str(variavel0))
        time.sleep(segundos)


def write_csv_line (nomedoarquivo,dados):
    if dados != []:
        arquivoaberto = open(nomedoarquivo, mode='a+',
                             encoding="utf-8", newline='')
        arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',')
        arquivoaberto_csv.writerow(dados)
        arquivoaberto.close()

def write_csv_lines (nomedoarquivo, dados):
    if dados != []:
        arquivoaberto = open(nomedoarquivo, mode='a+',
                             encoding="utf-8", newline='')
        arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',')
        for item in dados:
            arquivoaberto_csv.writerow(item)
        arquivoaberto.close()

def extrai_acordaos_da_string (arquivo_a_extrair, path):  # usar duas contra-barras depois do nome

    if arquivo_a_extrair in os.listdir(path):
        nome_do_arquivo = str(path+arquivo_a_extrair)

        acordaos = carregar_arquivo (nome_do_arquivo)
        # print (arquivo_a_extrair)

        n_acordaos = extrair(acordaos,'Documentos encontrados: ','</td>')
        acordaos_publicados = []

        adi_decisao = 'NA'
        acordaos_publicados = []
        acordaos_adi = []
        acordaos_agr = []
        acordaos_emb = []
        acordaos_qo = []
        acordaos_outros = []

        if "Nenhum registro encontrado" in acordaos:
            decisao_colegiada = []

        else:
            decisao_colegiada = []

            for decisoes in range (int(n_acordaos)):


                acordaos_adi    = []
                acordaos_emb    = []
                acordaos_agr    = []
                acordaos_qo     = []
                acordaos_outros = []
                lista_processos_citados = []
                lista_procesoss_citados_com_tema = []
                acordao_tipo = 'NA'
                processo_juris = 'NA'
                relator_juris = 'NA'
                data_acordao = 'NA'
                orgao_julgador_acordao = 'NA'
                publicacao_acordao = 'NA'
                ementa = 'NA'
                decisao_juris = 'NA'
                legislacao = 'NA'
                observacao = 'NA'
                doutrina = 'NA'

                acordaos = acordaos.replace ('/n/n','/n')
                acordaos = acordaos.replace ('/t','')


                processo_juris = extrair(acordaos,'''<!-- Término do trecho que passa informações para o QueryString (Pesquisa Simultânea de Jurisprudência) --''', '<br />').upper()
                processo_juris = processo_juris.replace('AÇÃO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
                processo_juris = processo_juris.replace('ACAO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
                if 'ADI' in arquivo_a_extrair:
                    processo_juris = processo_juris.replace('AÇÃO DECLARATÓRIA DE CONSTITUCIONALIDADE', 'ADI')
                processo_juris = processo_juris.replace('MEDIDA CAUTELAR', 'MC')
                processo_juris = processo_juris.replace('\n', '')
                processo_juris = processo_juris.replace('\t', '')
                processo_juris = processo_juris.replace('>', '')
                processo_juris = processo_juris.replace('REFERENDO NA MC','MC (REFERENDO)')
                processo_juris = processo_juris.replace('REFERENDO NOS EMB.DECL.','EMB.DECL. (REFERENDO)')
                processo_juris = processo_juris.replace('REFERENDO NO AG.REG.','AG.REG (REFERENDO)')
                processo_juris = processo_juris.replace('SEGUNDOS ','')
                processo_juris = processo_juris.replace('SEGUNDO','')
                processo_juris = processo_juris.replace('TERCEIROS','')

                acordao_tipo = 'NA'

                if processo_juris[0:3] == "MC ":
                    acordao_tipo = "MC"
                elif processo_juris[0:3] == "EMB":
                    acordao_tipo = 'EMBARGOS'
                elif processo_juris[0:2] == "AG":
                    acordao_tipo = 'AGRAVO'
                elif processo_juris[0:3] == "QUE":
                    acordao_tipo = 'QO'
                elif processo_juris[0:3] == "ADI":
                    acordao_tipo = 'PRINCIPAL'
                else:
                    acordao_tipo = 'OUTROS'


                relator_juris = extrair(acordaos, 'Relator(a):&nbsp ', '<br />').upper()
                relator_juris = relator_juris.lstrip(' ')
                relator_juris = relator_juris.lstrip('MIN.')
                relator_juris = relator_juris.lstrip(' ')
                relator_juris = remover_acentos(relator_juris)

                data_acordao = extrair(acordaos, 'Julgamento:&nbsp', '&nbsp')
                data_acordao = data_acordao.replace('\t','')

                orgao_julgador_acordao = extrair(acordaos, 'Órgão Julgador:&nbsp', '<br />')

                publicacao_acordao = extrair (acordaos, '''<PRE><span style='font-family:tahoma, verdana, arial, sans-serif;font-size:1.1 em;font-weight:bold'>''', '</PRE>')

                ementa = extrair (acordaos, '''<p><div style="line-height: 150%;text-align: justify;">''', '</div>')

                decisao_juris = extrair (acordaos, '''<p><div style="text-align:justify; color: #385260; font-weight: normal; font-size: 11px">''', '</div>')

                legislacao = extrair (acordaos, '''Legislação</strong></p>''', '</PRE>')
                legislacao = legislacao.replace('\t','')
                legislacao = legislacao.replace('\n','')

                observacao =  extrair (acordaos, '''<p><strong>Observação</strong></p>''', '</PRE>')
                if 'Acórdão(s) citado(s)' in acordaos and 'Nenhum registro encontrado' not in acordaos and 'AGUARDANDO INDEXAÇÃO' not in acordaos:
                    observacao = observacao.replace ('(s)','')
                    observacao = observacao.replace ('(2ªT)','')
                    observacao = observacao.replace ('(1ªT)','')
                    observacao = observacao.replace ('(TP)','')
                    n_cit = observacao.count('href')
                    for links in range (n_cit):
                        inicio = observacao.find ('href')
                        fim = observacao.find ('>',inicio)
                        retirar = observacao[inicio:fim]
                        observacao = observacao.replace(retirar,'')

                    observacao = observacao.replace('\n','')
                    observacao = observacao.replace('<a>','')
                    observacao = observacao.replace('<a >','')
                    observacao = observacao.replace('</a>','')
                    observacao = observacao.replace(' ,',',')
                    observacao = observacao.replace(' .','.')
                    observacao = observacao.replace('.','')


                    observacao = observacao.split('(')[1:]
                    if  observacao != [] and 'Número de páginas' in observacao[-1]:
                        observacao[-1] = extrair (observacao[-1],'','Número de páginas')
                    lista_processos_citados = []
                    lista_procesoss_citados_com_tema = []
                    for obs in range (len(observacao)):
                        elemento = observacao[obs]
                        elemento = elemento.split(')')
                        tema = [elemento.pop(0)]
                        elemento = str(elemento).split(',')
                        for item in range (len(elemento)):
                            processo_citado = elemento[item]
                            processo_citado = processo_citado.lstrip('[')
                            processo_citado = processo_citado.lstrip("]")
                            processo_citado = processo_citado.lstrip(' ')
                            processo_citado = processo_citado.lstrip("'")

                            processo_citado_e_tema = processo_citado + ',' + str(tema)
                            lista_processos_citados.append(processo_citado)
                            lista_procesoss_citados_com_tema.append(processo_citado_e_tema)


                doutrina = extrair(acordaos, '''<p><strong>Doutrina</strong></p>''', '</PRE>')



                decisao_colegiada = [arquivo_a_extrair, acordao_tipo, processo_juris, relator_juris, data_acordao, orgao_julgador_acordao, publicacao_acordao, ementa, decisao_juris, legislacao, observacao, lista_processos_citados, lista_procesoss_citados_com_tema, doutrina]
                # print (decisao_colegiada)

                acordaos_publicados.append(decisao_colegiada)
                if acordao_tipo == 'PRINCIPAL':
                    acordaos_adi.append(decisao_colegiada)
                    adi_decisao = decisao_juris
                if acordao_tipo == 'EMB':
                    acordaos_emb.append(decisao_colegiada)
                if acordao_tipo == 'AGR':
                    acordaos_agr.append(decisao_colegiada)
                if acordao_tipo == 'QO':
                    acordaos_qo.append(decisao_colegiada)
                if acordao_tipo == 'OUTROS':
                    acordaos_outros.append(decisao_colegiada)




            recortar = acordaos.find('<!-- Término do trecho que passa informações para o QueryString (Pesquisa Simultânea de Jurisprudência) --')
            acordaos = acordaos[recortar+len('<!-- Término do trecho que passa informações para o QueryString (Pesquisa Simultânea de Jurisprudência) --'):]
        return (arquivo_a_extrair,
                adi_decisao,
                acordaos_publicados,
                acordaos_adi,
                acordaos_agr,
                acordaos_emb,
                acordaos_qo,
                acordaos_outros)
    else:
        return ([], 'NA', [], [], [], [], [], [])


def extrai_mono_da_string (arquivo_a_extrair, path):  # usar duas contra-barras depois do nome

        if arquivo_a_extrair in os.listdir(path):
            
            nome_do_arquivo = str(path+arquivo_a_extrair)

            monocraticas = carregar_arquivo (nome_do_arquivo)
            # print (arquivo_a_extrair)

            # n_monocraticas = extrair(monocraticas,'Documentos encontrados: ','</td>')


            n_monocraticas = monocraticas.count('img src="imagem/bt_imprimirpopup.gif" alt="Imprimir" style="position:relative;left:490px;top:-38px;margin-bottom:-55px;')

            adi_decisao_mono = 'NA'
            monocraticas_publicadas = []
            monocraticas_adi = []
            monocraticas_agr = []
            monocraticas_emb = []
            monocraticas_qo = []
            monocraticas_outros = []
            monocraticas_amicus = []
            monocraticas_mc = []
            monocraticas_publicadas = []
            processo_juris = 'NA'


            if "Nenhum registro encontrado" in monocraticas:
                decisao_monocratica = []

            else:
                decisao_monocratica = []

                for decisoes in range (int(n_monocraticas)):


                    monocraticas_adi    = []
                    monocraticas_emb    = []
                    monocraticas_agr    = []
                    monocraticas_qo     = []
                    monocraticas_outros = []

                    acordao_tipo = 'NA'
                    processo_juris = 'NA'
                    relator_juris = 'NA'
                    data_acordao = 'NA'
                    orgao_julgador_acordao = 'NA'
                    decisao_juris = 'NA'
                    legislacao = 'NA'
                    observacao = 'NA'


                    monocraticas = monocraticas.replace ('/n/n','/n')
                    monocraticas = monocraticas.replace ('/t','')


                    processo_juris = extrair(monocraticas,'''<img src="imagem/bt_imprimirpopup.gif" alt="Imprimir" style="position:relative;left:490px;top:-38px;margin-bottom:-55px;" />''', '<br />').upper()

                    processo_juris = processo_juris.replace('AÇÃO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
                    processo_juris = processo_juris.replace('ACAO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
                    processo_juris = processo_juris.replace('MEDIDA CAUTELAR', 'MC')
                    processo_juris = processo_juris.replace('\n', '')
                    processo_juris = processo_juris.replace('\t', '')
                    processo_juris = processo_juris.split('<STRONG>')[1]

                    acordao_tipo = 'na'

                    if "AMICUS" in processo_juris:
                        moocratica_tipo = "AMICUS"
                    elif 'MC' in processo_juris or 'CAUT' in processo_juris:
                        moocratica_tipo = "CAUT"
                    elif 'EMB.' in processo_juris:
                        moocratica_tipo = 'EMB'
                    elif 'AG.REG' in processo_juris:
                        moocratica_tipo = 'AGR'
                    elif 'ORDEM' in processo_juris or 'QO' in processo_juris:
                        moocratica_tipo = 'QO'
                    elif processo_juris[0:3] == "ADI":
                        moocratica_tipo = 'PRINCIPAL'
                    else:
                        moocratica_tipo = 'OUTROS'


                    relator_juris = extrair(monocraticas, 'Relator(a):&nbsp ', '<br />').upper()
                    relator_juris = relator_juris.lstrip(' ')
                    relator_juris = relator_juris.lstrip('MIN.')
                    relator_juris = relator_juris.lstrip(' ')
                    relator_juris = remover_acentos(relator_juris)

                    data_acordao = extrair(monocraticas, 'Julgamento:&nbsp', '&nbsp')
                    data_acordao = data_acordao.replace('\t','')

                    orgao_julgador_acordao = relator_juris

                    publicacao_monocratica = extrair (monocraticas, '''<pre><span style='font-family:tahoma, verdana, arial, sans-serif;font-size:1.1 em;font-weight:bold'>''', '</pre>')


                    decisao_juris = extrair (monocraticas, '''Decisão</strong></p>''', '</pre>')
                    if '<pre>' in decisao_juris:
                        decisao_juris = decisao_juris.split('<pre>')[1]
                    decisao_juris = limpar(decisao_juris)
                    decisao_juris = decisao_juris.replace('\n\n','\n')



                    legislacao = extrair (monocraticas, '''Legislação</strong></p>''', '</pre>')
                    legislacao = legislacao.replace('\t','')
                    legislacao = legislacao.replace('\n','')

                    observacao =  extrair (monocraticas, '''<p><strong>observação</strong></p>''', '</pre>')



                    decisao_monocratica = [arquivo_a_extrair, acordao_tipo, processo_juris, relator_juris, data_acordao, orgao_julgador_acordao, publicacao_monocratica, decisao_juris, legislacao, observacao]
                    # print (decisao_monocratica)

                    monocraticas_publicadas.append(decisao_monocratica)
                    if moocratica_tipo == 'PRINCIPAL':
                        monocraticas_adi.append(decisao_monocratica)
                        adi_decisao_mono = decisao_juris
                    if moocratica_tipo == 'EMB':
                        monocraticas_emb.append(decisao_monocratica)
                    if moocratica_tipo == 'AGR':
                        monocraticas_agr.append(decisao_monocratica)
                    if moocratica_tipo == 'QO':
                        monocraticas_qo.append(decisao_monocratica)
                    if moocratica_tipo == 'OUTROS':
                        monocraticas_outros.append(decisao_monocratica)
                    if moocratica_tipo == 'AMICUS':
                        monocraticas_amicus.append(decisao_monocratica)
                    if moocratica_tipo == 'MC':
                        monocraticas_mc.append(decisao_monocratica)



                recortar = monocraticas.find('''<img src="imagem/bt_imprimirpopup.gif" alt="Imprimir" style="position:relative;left:490px;top:-38px;margin-bottom:-55px;" />''')
                monocraticas = monocraticas[recortar+len('''<img src="imagem/bt_imprimirpopup.gif" alt="Imprimir" style="position:relative;left:490px;top:-38px;margin-bottom:-55px;" />'''):]
            return (processo_juris,
                    arquivo_a_extrair,
                    adi_decisao_mono,
                    monocraticas_publicadas,
                    monocraticas_adi,
                    monocraticas_mc,
                    monocraticas_agr,
                    monocraticas_emb,
                    monocraticas_qo,
                    monocraticas_amicus,
                    monocraticas_outros)
        else:
            return ([], 'NA', [], [], [], [], [], [], [],[], [])
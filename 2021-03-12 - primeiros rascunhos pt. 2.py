# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 00:40:58 2021

@author: Pedro
"""

html = '''<div id="divImpressao"><div><h3><strong>AÇÃO DIRETA DE INCONSTITUCIONALIDADE (Med. Liminar) - 6000</strong></h3><table width="99%" cellspacing="5"><tr><td>Origem:</td><td><strong>RIO DE JANEIRO</strong></td><td>Entrada no STF:</td><td><strong>30-Ago-2018</strong></td></tr><tr><td>Relator:</td><td><strong>MINISTRO ALEXANDRE DE MORAES</strong></td><td>Distribuído:</td><td><strong>30-Ago-2018</strong></td></tr><tr><td>Partes:</td><td colspan="3">Requerente: <strong>GOVERNADOR DO ESTADO DO RIO DE JANEIRO (CF 103, 00V)</strong><br />Requerido :<strong>ASSEMBLEIA LEGISLATIVA DO ESTADO DO RIO DE JANEIRO </strong></td></tr></table></div><br /><strong><strong '''

inicio_relator = html.find("Relator:</td><td><strong>")+len("Relator:</td><td><strong>")
fim_relator = html.find("<", inicio_relator)

print(html[inicio_relator:fim_relator])
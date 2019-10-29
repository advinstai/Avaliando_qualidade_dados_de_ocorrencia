
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 14:24:37 2019

@author: felipe

exPyBIO: equipe
"""

# Abrir Arquivo

def carregarCSV(path=None):

    # caso não tenha parâmetro: pegar do arquivo padrão:
    caminho = path if path else "portalbio_export_16-10-2019-14-39-54.csv"

    arquivo = None

    try:
        arquivo = open(caminho, "r")
    except IOError as e:
        print("erro ao abrir o arquivo: ", e.args)
        return

    # Lê tudo de uma vez:
    base = arquivo.readlines()

    arquivo.close()

    dadosXY = list()

    # Converte CSV em matriz

    try:
        dadosXY = map(lambda l: l.split(";"), base)

    except AttributeError as e:
        print("Falha ao processar o arquivo CSV, deve ter muitas colunas faltando. ", e.args)

    return dadosXY


def getColuna(k,dados):
    return map(lambda x:x[k], dados )


# verifica se tem uma celula fazia ou não:
def vazio(celula): return celula == "Sem Informações" or celula == ""


#no python3 colocar o list antes do map

def verificaTaxonomia(dados):
    """
        nível taxonomico: [1-7]
        reino filo classe ordem familia genero especie

        exemplo: nivel = 5
                1        2   3             4         5
           Animal Chordata Aves Ciconiiformes Ardeidae 0 0

    """

    dadosXY = dados[1::] # pega apenas o campo dos dados (Retira o rotulo)

    nivelTaxonomico = list()

    try:
        colunaFilo = dados[0].index('Reino') #captura o índice do rotulo que contem o filo

        #alguns reinos estão faltando
        #quando se tem o Filo, o reino é obvio, então começamos a percorrer
        #a partir do filo

    except ValueError as e:
        print( "formato dos rótulso inválido ou sem a classificação taxonomica: ", e.args)
        return # sair da função

    for linha in dadosXY:
         tax = linha[colunaFilo:colunaFilo+7] # examina apenas as colunas com a classificação
         # para cada coluna que contem a taxonomia ver quais são nulas,
         # caso nenhuma coluna é nula a classificacao é completa: 7
         nivel =  7 - sum ( list(map(vazio, tax))  )

         # adiciona o nível calculado na listagem geral
         nivelTaxonomico.append(nivel)

    return nivelTaxonomico

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 14:24:37 2019
@author: felipe
exPyBIO: equipe
"""

import numpy as np
import pandas as pd


#esta classe utiliza métodos estáticos @staticmethod
#estes métodos podem ser acessados fora dos objetos, como se fosse uma função solta. É como se apenas estivesse agrupando as funçoes para
#não ficaram perdidas ao importar para outros arquivos

# exemplo: from Felipe import AvaliaTax
# meusDados = leiaTudo(arquivo)
# AnaliaTax.verificaTaxonomia(meusDados)
# 
# Não precisa fazer:
# meuObjeto = AvaliaTax()
# e depois: meuObjeto.verificaTaxonomia(meusDados)
# pois neste projeto só vai ter 1 objeto AvaliaTax, não faz sentido eu criar mais de um. 
# 
# quando uma classe vira um aglomerado de funções, para projetos pequenos, fica mais fácil de entender. 

class AvaliaTax:
    
    #shared atribute
    defaultFile =  "portalbio_export_16-10-2019-14-39-54.csv"
    
    def __init__(self):
        print("Nao precisa instanciar esta classe, pode fazer AvaliaTax.metodo() para utilizar as funções")
    
    #usar este método apenas para testes internos. Utilizar o método da classe MyData para carregar o arquivo
    @staticmethod
    def carregarCSV(path=None):
      
        # caso não tenha parâmetro: pegar do arquivo padrão:
        caminho = path if path else AvaliaTax.defaultFile
        
        arquivo = None
        
        try:
            arquivo = open(caminho, "r")
        except IOError as e:
            print ("erro ao abrir o arquivo: " , e.args)
            return
        
        # Lê tudo de uma vez:    
        base = arquivo.readlines()
        
        arquivo.close()
            
        dadosXY = list()
    
        # Converte CSV em matriz
        
        try:
            dadosXY = list(map(lambda l: l.split(";"), base))
            
        except AttributeError as e:
            print ("Falha ao processar o arquivo CSV, deve ter muitas colunas faltando. " , e.args)
        
        return dadosXY
    
    @staticmethod
    def getColuna(k,dados):
        return map(lambda x:x[k], dados )
    
    
    # verifica se tem uma celula fazia ou não:
    @staticmethod
    def vazio(celula): return celula == "Sem Informações" or celula == ""
    
    vaziop = "Sem Informações" # atributo shared
    
    #no python3 colocar o list antes do map
    #implementação antiga:
    @staticmethod
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
            colunaFilo = dados[0].index('Filo') #captura o índice do rotulo que contem o filo
            
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
            nivel =  7 - sum ( list(map(AvaliaTax.vazio, tax))  )
             
             # adiciona o nível calculado na listagem geral
            nivelTaxonomico.append(nivel)
        
        return nivelTaxonomico
    
    @staticmethod
    def listaMetodos(): return dir(AvaliaTax)
    
    @staticmethod
    def pandasAdapter(pandaDataframe):
        out = pandaDataframe.to_numpy()
        
        outlist =  np.array(out, dtype=str).tolist()
        
        outlist.insert(0, list(pandaDataframe))
        
        return outlist
        
    
    @staticmethod
    def verificaTaxonomiaAsNumpy(dadosd):
        
        '''
        Entrada: lista das listas de todos os dados, incluindo o cabeçalho, use o Adapter para funcionar com o Pandas
        Saída: faz o mesmo do verificaTaxonomia(dados), porém retorna uma lista 1D de números no formato do numpy
        este método é mais resumido devido as funcionalidados do numpy.
        '''
        
        try:
            dadosnp = np.array(dadosd[1::]) #converte os dados (e exclui o cabeçalho)
        except TypeError as e:
            print("tipo inválido, muitas colunas faltantes ou numpy não importado/instalado: ", e.args)
            print("use import numpy as np ou !conda install numpy=1.16.15")
            return -1
        
        #verifica em que lugar da tabela tem a taxonomia
        try:
            colunaFilo = dadosd[0].index('Filo')
        except ValueError:
            print("falha ao procurar as colunas do nível taxonomico, verifique se está no formato 'filo'")
            return -1
        
        
        #aqui acontece o procedimento (ver detalhes na documentação)
        #usei a técnica da máscara de matriz
        return 7 - np.sum( dadosnp[:,colunaFilo:colunaFilo+6] == AvaliaTax.vaziop , 1)
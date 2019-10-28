#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 10:06:11 2019

@author: alexandremarcondes
"""

# Bibliotecas
import sys
import pandas as pd

# Classes
class MyData:
    
    def __init__(self, my_csv):
        try:
            self.df = pd.read_csv(my_csv, sep='\n', delimiter=';')  # Cria o dataframe através do arquivo CSV
        except IOError as e:
            print('Could not read the file', my_csv) # Caso o arquivo com o nome citado não exista, o programa é encerrado
            print ('I/O error({0}): {1}'.format(e.errno, e.strerror))  # Indica o erro ocorrido 
            sys.exit()
        
        self.fields = list(self.df)  # Cria uma lista com todos os campos presentes no CSV
        self.n_lines = len(self.df)  # Atribui o número de linhas do arquivo a variável n_lines
     
    def getEmpty(self):  # Método que retorna a média de dados faltantes por campo no arquivo CSV
        count_mean = {}  # Dicionário com a média de dados faltantes pela quantidade de linhas
        for field in self.fields:  # Itera sobre cada campo na lista de campos do arquivo CSV
            
            # List comprehension:
            # Soma 1 se a célula não tiver informação ou 0 se a célula tiver informação 
            count_mean[field] = sum([1 if value == "" or value == "Sem Informações" else 0 for value in self.df[field]])
            
            # Divide a soma dos dados faltantes pelo número de linhas para obtger a média
            count_mean[field] = (count_mean[field]/self.n_lines)*100  #  A multiplicação por 100 obtém a porcentagem dos dados faltantes
        nan_df = pd.DataFrame([count_mean])  # Transforma o dicionário em um dataframe com as porcentagens de dados faltantes
        return nan_df
        

csv_file = 'portalbio_export_17-10-2019-13-06-22.csv'  # Arquivo CSV que será carregado
csv_open = MyData(csv_file)  # Criação da instância da classe MyData
mean_nan_values = csv_open.getEmpty() #  Utiliza o método para obter as células vazias

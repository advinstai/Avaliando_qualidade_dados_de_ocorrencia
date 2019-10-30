#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 17:27:53 2019

@author: cavalcante87
"""

class desAna:
    string_list = []
    temp_list = []
    
    def __init__(self, path):
        self.path=path
        self.read_file=open(path, 'r')
        self.txt=self.read_file.readlines()

    def stringList(self):
        self.string_list = [element.strip().split(',') for element in self.txt]
        return self.string_list
    
    def emptyCounter(self):
        a = self.stringList()
        count = 0
        for i in range(len(a[1:])):
            for j in range(len(a[i])):
                if str(a[i][j]).lower() == 'sem informações' or a[i][j] == '':
                    count = count + 1        
        return count
    
    def mediaEmptyColumnsData(self):
        a = self.stringList()
        count_list = []
        columns_count = []
        for j in range(len(a[0])):
            for i in range(len(a[1:])):
                if str(a[i][j]).lower() == 'sem informações' or a[i][j] == '': 
                    count_list.append(1)
                else:
                    count_list.append(0)
                    
            columns_count.append(sum(count_list)/len(count_list))
            count_list = []
                
        return columns_count
    
    #taxonomicRank() retorna uma lista onde cada entrada é uma lista com uma taxonomia biologica de Espécie até Reino
    #taxonomic_rank é uma lista temporaria que se esvazia para criar uma nova lista dentro da lista maior    
    def taxonomicRank(self):
        a = self.stringList()
        taxonomic_rank_list = []
        for i in range(1,len(a)):
            taxonomic_rank = []
            for j in range(21,14, -1):
                if str(a[i][j].lower()) != 'sem informações':
                    taxonomic_rank.append('Nível Taxonômico: ' + a[0][j] + ': ' + a[i][j])
                else:
                    pass
            taxonomic_rank_list.append(taxonomic_rank)

                
        return taxonomic_rank_list
    
    #showTaxonomicRank() retorna apenas o nível taxonomico do mais específico (Espécie) para o geral (Reino) 
    #b chama o metodo taxonomicRank() ja criado, que lista a taxonomia que foi preenchida com informações pertinentes
    #primeiro 'for' (i) varre cada linha de Espécie até Reino (backwards)
    #segundo 'for' (j) varre cada item da linha do primeiro 'for' (i) e imprime unicamente a primeira taxonomia
    def showTaxonomicRank(self):
        b = self.taxonomicRank()
        for i in range(len(b)):
            for j in range(len(b[i])):
                if j == 0:
                    print(b[i][j])

                    
#path='/home/cavalcante87/Documents/fiephub/OOP2_2/portalbio_export_16-10-2019-14-39-54.csv'
path='/home/cavalcante87/Documents/fiephub/OOP2_2/portalbio_export_17-10-2019-13-06-22.csv'
#path='/home/cavalcante87/Documents/fiephub/OOP2_2/portalbio_export_17-10-2019-13-15-00.csv'
file=desAna(path)
#file.stringList()
#file.emptyCounter()
#file.mediaEmptyColumnsData()
file.taxonomicRank()
#file.showTaxonomicRank()
#b=file.stringList()
#df=pd.DataFrame(b[1:], columns=b[0])
#df.head()

"""
Created on Thu Oct 28 16:00 2019
@author: Wana 

"""

import pandas as pd
import numpy as np
import csv


'''
The above ANSI escape code will set the text colour to bright green. The format is;
\033[  Escape code, this is always the same
1 = Style, 1 for normal.
32 = Text colour, 32 for bright green.
40m = Background colour, 40 is for black.
'''
#Atividade 3

class wana:
	dados = []
	df = None
	dict_header = {}
	header = None
	auxh = []
	def __init__(self, file, sep):

		try:

			self.file = pd.read_csv(file, sep=sep)

		except:
			print('Could not open the file')
			sys.exit(1)

	def dict(self):
		self.df = self.file.apply(lambda x: x.astype(str).str.lower()) # turn all my data to lower case
		self.header = self.df.columns.tolist() # getting the list of header' names
		#creating a dictionary with column' names
		for i in range(len(self.header)):
			self.dict_header[i] = self.header[i]

	def entry(self):
		self.dict()
		entry = input('\033[1;31;47m{}\n\033[1;30;47m PLEASE, ENTER THE INDICES YOU WOULD LIKE TO FILTER, SEPARATED BY SPACE: \n'.format(self.dict_header))
		list_filter  = entry.split() # turning it in a list os string
		int_list = [int(i) for i in list_filter] #list comprehansion to convert the string values into int values
		for i in int_list:
			for j in range(len(self.header)):
				if i == j:
					self.dfaux = list(set(self.df[self.header[i]]))
					print("{}: {}".format(self.header[i],', '.join(self.dfaux)))
					print("")
					f = input('Based on the options above, %s:' %self.header[i])
					self.auxh.append(self.header[i])
					self.dados.append(f)


	def show_and_save(self):
		self.dict()
		self.entry()
		for k in range(len(self.dados)):
		# selecting rows based on condition 
			data = self.df[self.df[self.auxh[k]] == self.dados[k]] 

		print('result for:' , '-'.join(i for i in self.dados))
		print(data) if len(data) > 0 else print('result is empty')
		a = input("would you like to save the result [yes]/no?")
		if a == 'no':
			print('file not saved')
		elif a == 'yes' or a == '':
			exemplo= "/home/wanabb/repo-git/repositorio-git/pesquisa1.csv"
			output = input('enter with the path and name, ex: %s \n' %exemplo)
			data.to_csv(output, sep=';')
			print('file saved')
		else:
			print('wrong answer, try again :(')
			
'''
if __name__ == '__main__':
	f = '/home/wanabb/repo-git/repositorio-git/Avaliando_qualidade_dados_de_ocorrencia/Entregas/Grupo_Felipe_Wana_Andre_Alexandre/portalbio_export_16-10-2019-14-39-54.csv'
	s = ';'
	r = wana(f,s)
	r.show_and_save()
'''
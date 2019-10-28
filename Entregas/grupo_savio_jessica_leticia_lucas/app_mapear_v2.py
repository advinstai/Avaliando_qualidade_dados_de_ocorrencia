#Importando bibliotecas
import sys
import pandas as pd
import numpy as np
import streamlit as st

sys.path.append('libs')
#from loni import *
from felipe import *
#teste()

print('leticia333333333333333')

class app_hub():

	#Atributos da classe app_hub:
	dicionario = ['Exe. 1: Valores vazios','Exe. 2: Nivel Taxonomico','Exe. 3: Filtros','Exe. 4: Avaliar Lon / Lat']
	linhas = []
	lista_completa = []

	#Metodo construtor
	def __init__(self):
		file = open('Arquivos/portalbio_export_17-10-2019-13-06-22.csv', 'r', encoding='utf8')
		self.linhas = file.readlines()

	#Metodo para construir a matriz
	def construir(self, lines):
		self.lista_completa = [[item for item in itens.split(',')]for itens in lines]
		return self.lista_completa

	#Metodo para contar os nulos
	def count_nulls(self, lista):

		#list compehension que retorna lista das colunas vazias
		def funcao(texto):
			return True if texto == "Sem Informações" or texto == " " else False
		colunas_vazias = [sum([funcao(lista[linha][coluna]) for linha in range(len(lista))]) for coluna in range(len(lista[0]))]
		return colunas_vazias

	#Metodo para retornar a porcetagem de itens sem informação em cada coluna
	def media_nulls(self, lista):

	#Map aplicando a função lambda em cada item da lista
		return map(lambda item: item /len(self.lista_completa), lista)

	#Metodo para checar nível taxonom...
	def taxonom(self):
		count=0

		#Procura pela posição da palavra filo nas colunas:
		for i in range(0, len(self.lista_completa[0:][0])):
			if self.lista_completa[0][i] == 'Filo':
				count = i
				break

		#List comprehension pra criar uma lista com os valores taxon..: 0 a 6
		def testar(teste):
			return False if teste == "Sem Informações" or teste == " " else True
		novas_colunas = [sum([testar(self.lista_completa[linha][coluna]) for coluna in range(count, count+6)]) for linha in range(len(self.lista_completa))]
		novas_colunas.insert(0,'Taxonom')
		return novas_colunas

class app_grafica(app_hub):

	option = []
	option_01 = []

	def __init__(self, app = app_hub()):
		print('App Inicializado com Sucesso! =^.^=')
		st.sidebar.markdown('### @Desafio 02')
		self.option = st.sidebar.selectbox('Escolha o exercicio: ',app.dicionario)
		st.title('Hub IA - SENAI / Londrina')
		st.write('Voce selecionou a opcao: ', self.option)

		if st.sidebar.checkbox('Integrantes'):
			st.sidebar.markdown('#### @Savio')
			st.sidebar.markdown('#### @Leticia')
			st.sidebar.markdown('#### @Lucas')
			st.sidebar.markdown('#### @Jessica')
			st.sidebar.markdown(' ')

	def inicializar(self, app = app_hub()):

		opcoes = ['Quantidade de valores nao preenchidos', 'Porcetagem de dados faltantes por coluna']

		#Exercicio 01 valores vazios
		if self.option == app.dicionario[0]:
			self.option_01 = st.selectbox('Exercicio 01: Escolha o grafico:', opcoes)
			st.write('Para cada coluna identique a quantidade de linhas com dados faltantes (em alguns casos, o dado faltante é uma string vazia, em outros casos é uma string contendo algum valor do tipo: "sem informação"). Faça um método que retorna a média de dados faltantes por coluna')
			if self.option_01 == opcoes[0]:
				st.markdown('### Valores vazios ou faltantes: ')
				st.bar_chart(app.count_nulls(app.construir(app.linhas)))
				if st.checkbox('Mostrar lista de dados faltantes'):
					st.write(app.count_nulls(app.construir(app.linhas)))
			if self.option_01 == opcoes[1]:
				st.markdown('### Porcetagem de valores faltantes por coluna: ')
				st.bar_chart(app.media_nulls(app.count_nulls(app.construir(app.linhas))))
				if st.checkbox('Mostrar lista de porcetagem'):
					st.write(list(app.media_nulls(app.count_nulls(app.construir(app.linhas)))))

		#Exercicio 02 Nivel taxonomico
		if self.option == app.dicionario[1]:
			st.write('Para cada item identifique até qual nível taxônomico a ocorrência foi identificada.')
			#verificaTaxonomia metodo importado do felipe
			st.bar_chart(verificaTaxonomia(app.construir(app.linhas)))
			if st.checkbox('Valores por Coluna'):
				st.write(verificaTaxonomia(app.construir(app.linhas)))

		#Exercicio 03  Filtros
		if self.option == app.dicionario[2]:
			mapa_bio = pd.read_csv('Arquivos/mapa_biodiversidade.csv', header=0)
			st.write('Monte filtros de ocorrências por estados, nome de espécie (nome exato ou parte do nome) e categoria de ameaça, e outros filtros que julgar relevante.')
			municipios = st.multiselect("Escolha os municipios", list(set(mapa_bio['Municipio'])), ["Londrina"])
			data = mapa_bio.loc[mapa_bio['Municipio'].isin(municipios)]

			st.deck_gl_chart(
    			viewport={
         		'latitude': -23.37,
         		'longitude': -51.28,
         		'zoom': 11,
         		'pitch': 50,
     			},
     			layers=[{
         		'type': 'HexagonLayer',
		         'data': data,
		         'radius': 200,
		         'elevationScale': 4,
		         'elevationRange': [0, 1000],
		         'pickable': True,
		         'extruded': True,
		     	}, {
		         'type': 'ScatterplotLayer',
		         'data': data,
		     	}])

			if st.checkbox('Mostrar dados'):
				st.dataframe(data)

		#Exercicio 04 - Geocode - Verificar se dados batem
		if self.option == app.dicionario[3]:
			st.image('Arquivos/Erro.jpg')
hub_ia = app_grafica()
hub_ia.inicializar()

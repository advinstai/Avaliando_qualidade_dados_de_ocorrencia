#Importando bibliotecas
#lucas teste
import sys
import pandas as pd
import numpy as np
import streamlit as st
import time
import urllib
import reverse_geocode

sys.path.append('libs')
from felipe import verificaTaxonomia

#teste()asdasd
#print('leticia d+')

class app_hub():

	#Atributos da classe app_hub:
	dicionario = ['Exe. 1: Valores vazios','Exe. 2: Nivel Taxonomico','Exe. 3: Filtros','Exe. 4: Avaliar Lon / Lat']
	linhas = []
	lista_completa = []

	#Metodo construtor
	#def __init__(self):
	#	file = open('Arquivos/portalbio_export_17-10-2019-13-06-22.csv', 'r', encoding='utf8')
	#	self.linhas = file.readlines()

	def carregar(self, path):
		file = open(path, 'r', encoding='utf-8')
		self.linhas = file.readlines()
		df = pd.read_csv(path)
		lista = df.values.tolist()
		return df, lista

	#Metodo para construir a matriz
	def construir(self, path):
		# ifs provisórios ate resolver os bugs
		if path == 'Arquivos/df1.csv':
			file = open('Arquivos/portalbio_export_17-10-2019-13-06-22.csv', 'r', encoding='utf-8')
		if path == 'Arquivos/df2.csv':
			file = open('Arquivos/portalbio_export_16-10-2019-14-39-54.csv', 'r', encoding='utf-8')
		if path == 'Arquivos/df3.csv':
			file = open('Arquivos/portalbio_export_17-10-2019-13-15-00.csv', 'r', encoding='utf-8')
		self.linhas = file.readlines()
		self.lista_completa = [[item for item in itens.split(';')]for itens in self.linhas]
		return self.lista_completa

	#Metodo para contar os nulos
	def count_nulls(self, lista):

		#list compehension que retorna lista das colunas vazias
		def funcao(texto):
			return True if texto == 'Sem Informações' or texto == ' ' else False
		colunas_vazias = [sum([funcao(lista[linha][coluna]) for linha in range(len(lista))]) for coluna in range(len(lista[0]))]
		return colunas_vazias

	#Metodo para retornar a porcetagem de itens sem informação em cada coluna
	def media_nulls(self, lista, num):
	#Map aplicando a função lambda em cada item da lista
		return map(lambda item: item /num.shape[0], lista)


class app_grafica(app_hub):

	option = []
	option_01 = []
	path = 'Arquivos/df1.csv'

	def __init__(self, app = app_hub()):
		print('App Inicializado com Sucesso! =^.^=')

		st.sidebar.markdown('### @Desafio 02')
		self.option = st.sidebar.selectbox('Escolha o exercicio: ',app.dicionario)

		st.title('Hub IA - SENAI / Londrina')
		st.write('Voce selecionou a opcao: ', self.option)

		if st.sidebar.checkbox('Integrantes'):

			st.sidebar.markdown('##### @Savio')
			st.sidebar.markdown('##### @Leticia')
			st.sidebar.markdown('##### @Lucas')
			st.sidebar.markdown('##### @Jessica')
			st.sidebar.markdown(' ')

		if st.sidebar.checkbox('Caminho para a base de dados'):
			self.path = st.sidebar.text_input('Digite o caminho: ', 'Arquivos/df1.csv')

	def inicializar(self, app = app_hub()):

		opcoes = ['Quantidade de valores nao preenchidos', 'Porcetagem de dados faltantes por coluna']
		dados, lista = app.carregar(self.path)

			#Exercicio 01 valores vazios
		if self.option == app.dicionario[0]:
			self.option_01 = st.radio('Exercicio 01: Escolha o grafico:', opcoes)
			st.write('Para cada coluna identique a quantidade de linhas com dados faltantes (em alguns casos, o dado faltante é uma string vazia, em outros casos é uma string contendo algum valor do tipo: "sem informação"). Faça um método que retorna a média de dados faltantes por coluna')
			if self.option_01 == opcoes[0]:
				st.markdown('### Valores vazios ou faltantes: ')
				st.bar_chart(app.count_nulls(lista))
				#st.bar_chart(dados)
				if st.checkbox('Mostrar lista de dados faltantes'):
					#st.write(app.count_nulls(app.construir(app.linhas)))
					st.write(app.count_nulls(lista))

			if self.option_01 == opcoes[1]:
				st.markdown('### Porcetagem de valores faltantes por coluna: ')
				#st.bar_chart(app.media_nulls(app.count_nulls(app.construir(app.linhas))))
				st.bar_chart(app.media_nulls(app.count_nulls(lista),dados))
				if st.checkbox('Mostrar lista de porcetagem'):
					st.write(list(app.media_nulls(app.count_nulls(app.construir(self.path)))))

		#Exercicio 02 Nivel taxonomico
		if self.option == app.dicionario[1]:
			st.write('Para cada item identifique até qual nível taxônomico a ocorrência foi identificada.')
			#verificaTaxonomia metodo importado do felipe
			st.bar_chart(verificaTaxonomia(app.construir(self.path)))
			#st.bar_chart(verificaTaxonomia(app.construir(lista)))
			if st.checkbox('Valores por Coluna'):
				st.write(verificaTaxonomia(app.construir(self.path)))

		#Exercicio 03  Filtros
		if self.option == app.dicionario[2]:

			mapa_bio = pd.read_csv(self.path)
			mapa_bio.rename(columns={'Latitude':'lat','Longitude':'lon'}, inplace=True)

			st.write('Monte filtros de ocorrências por estados, nome de espécie (nome exato ou parte do nome) e categoria de ameaça, e outros filtros que julgar relevante.')

			lista_de_filtros = ['Municipio', 'Familia','Filo','Classe','Localidade', 'Nome cientifico']
			filtros = st.multiselect("Escolha os filtros: -> Municipio -> Familia -> Filo -> Classe -> Localidade -> Nome cientifico", lista_de_filtros)
			if filtros:
				my_bar = st.progress(0)

				for percent_complete in range(0, 100):
					my_bar.progress(percent_complete + 1)

			mun_key, fam_key, fil_key, cla_key, loc_key, nom_key = False, False, False, False, False, False

			for i in range(0, len(filtros)):
				if filtros[i] == 'Municipio':
					municipios = st.multiselect('Escolha os municipios', list(set(mapa_bio[filtros[i]]))) #, ["Londrina"]
					data = mapa_bio.loc[mapa_bio[filtros[i]].isin(municipios)]
					mun_key == True
			for i in range(0, len(filtros)):
				if filtros[i] == 'Familia' and mun_key == False:
					familias = st.multiselect('Escolha as familias', list(set(mapa_bio[filtros[i]]))) #, ["Londrina"]
					data = data.loc[mapa_bio[filtros[i]].isin(familias)]
				elif filtros[i] == 'Familia' and mun_key == True:
					familias = st.multiselect('Escolha as familias', list(set(mapa_bio[filtros[i]]))) #, ["Londrina"]
					data = mapa_bio.loc[mapa_bio[filtros[i]].isin(familias)]

			if filtros:
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
			mapa_bio = pd.read_csv(self.path)
			mapa_bio.rename(columns={'Latitude':'lat','Longitude':'lon'}, inplace=True)
			row = np.arange(0,len(mapa_bio))
			loc = []
			for i in row:
				loc.append([mapa_bio["lat"][i], mapa_bio["lon"][i]])
			locDF = pd.DataFrame(loc,columns=['lat', 'lon'])
			st.map(locDF)
			#st.write(locDF)

			#Reverse geocoder (Precisa terminar)
			cities =reverse_geocode.search(loc) #Faz processo reverso e através de lat long traz a cidade
			cities =  pd.DataFrame(cities) #Transforma a lista em dataframe
			#New dataset com lat long e a respectiva cidade
			newdf = mapa_bio[['lat','lon','Municipio']]
			comparecities = []
			for j in np.arange(0,len(newdf)):
				if newdf['Municipio'][j] != cities['city'][j]:
					comparecities.append([mapa_bio['Municipio'][j],cities['city'][j]])
			comparecities = pd.DataFrame(comparecities, columns=['Municipio Planilha', 'Reverse Geocode'])
			st.write(comparecities)

hub_ia = app_grafica()
hub_ia.inicializar()

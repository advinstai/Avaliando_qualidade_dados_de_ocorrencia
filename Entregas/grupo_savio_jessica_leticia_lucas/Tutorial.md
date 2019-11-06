#  <p align="center"> Desafio Biodiversidade</p>
#### Grupo: Sávio, Jessica, Leticia, Lucas

## Projeto de Avaliação de qualidade de dados de biodiversidade

As seguintes informações foram fornecidos para a execução do projeto:
* Estudos na área de ecologia e conservação da biodiversidade são baseados em observações da natureza. Para que tais estudos normalmente é necessário utilizar uma grande quantidade de dados em grandes escala geografica e temporal.

O que é Informática para Biodiversidade: https://figshare.com/articles/Introduction_to_Biodiversity_Informatics/1295382

    Diversos portais reunem dados de observações que são chamados dados de ocorrência. Um dado de ocorrência é definido como uma observação individual de um animal ou planta, para essa observação muitas informações podem ser registradas, tais como, taxonomia da espécie, data, hora, local (lat/log), nome comum, coleção a que pertence, entre outros. Alguns metadados definem centenas de campos que podem ser preenchidos para cada observação.

    Diversos portais, tais como, Gbif, ALA, bson, canadensys, entre outros, reunem informações de dados de ocorrência para uso público.

    Uma área de pesquisa referente a dados de biodiversidade é quanto a qualidade desses dados. (https://www.researchgate.net/publication/264387406_Data_Quality_Control_in_Biodiversity_Informatics_The_Case_of_Species_Occurrence_Data)

    Nessa atividade dados de ocorrência de diferentes portais em formato CSV são fornecidos para que seja feita uma análise descritiva dessa informação, com base na qualidade dos dados. Nesse sentido, crie uma classe python que realize as seguintes funções:

--------------------------------------

## Ferramentas e Bibliotecas utilizadas

As seguintes bibliotecas são utilizadas:
```
import sys
import pandas as pd
import numpy as np
import streamlit as st
import time
import urllib
import reverse_geocode
```
O streamlit é um framework definido pelos criadores como:

> Streamlit is the first app framework specifically for Machine Learning and Data Science teams.
So you can stop spending time on frontend development and get back to what you do best. 

Permitindo a criação gráfica de apps de forma rápida utilizando somente python.
A aplicação foi implementada na nuvem com heroku, e sua primeira versão está disponivel em http://mapear.herokuapp.com/

Para importar a classe e executa-la:
```
objeto = app_grafica()
objeto.inicializar()
```
Para executar o streamlit localmente, acessar o terminal e:
```
streamlit
```
--------------------------------------
--------------------------------------
--------------------------------------

## **1.** Identificar a quantidade de linhas com dados faltantes.  
  
* Inicialmente três bases de dados de biodiversidade foram adquiridos do portal supracitado. Identificou-se que os dados precisavam ser avaliados quanto a sua consistência, pois diversas informações foram incluidas pelos usuários do portal **incorretamente**.  
* Verificou-se que a separação dos dados nas bases de dados no formato csv se dava por ";".

### Para resolução do exercicios avaliou-se as soluções que foram feitas nos grupos anteriores de cada integrante.

1.1 Na solução do exercicio_01 avaliou-se a solução do grupo anterior da residente Leticia onde foi feita a leitura do arquivo utilizando o pandas, csv_read:

```
import pandas as pd
import os
print(os.getcwd())
data = pd.read_csv("caminho_do_arquivo", sep=";")
```
  
* Utilizou o ';' como separador porque existem alguns campos que utilizam virgulas no meio da informaçao da celula, podendo causar desconfiguraçao no arquivo. Tendo o Dataframe, sao entao definidos as colunas/indices com o 'keys'  
  
* itensHash = data.keys()  

* Depois sao pegos todos os dados (data.values()) e enviados para a funçao ItemFaltante. Ali é feito um somatorio do total de espacos vazios por coluna para cada linha  

* No final divide-se esse somatorio pela quantidade total de linhas para dar o percentual de itens faltantes em cada coluna  

Por questões de avaliação das formas possíveis de atuar no problema, optou-se por ler o arquivo da seguinte forma:

```
def carregar(self, path):
	file = open(path, 'r', encoding='utf-8')
	self.linhas = file.readlines()
	df = pd.read_csv(path)
	lista = df.values.tolist()
	return df, lista
```
Isso foi feito para que fosse possivel abordar o problema tanto utilizando DataFrame como Lista.
A contagem dos dados foi feito com o metodo:

```
def count_nulls(self, lista):

	#list compehension que retorna lista das colunas vazias
	def funcao(texto):
		return True if texto == 'Sem Informações' or texto == ' ' else False
	colunas_vazias = [sum([funcao(lista[linha][coluna]) for linha in range(len(lista))]) for coluna in range(len(lista[0]))]
	return colunas_vazias
```

## **2.** Para cada item identifique até qual nível taxônomico a ocorrência foi identificada.

2.1 Na resolução do exercicio_02 avaliou-se a solução do grupo anterior dos residentes Sávio, e do Lucas onde foi importado o código do residente Felipe

```
sys.path.append('libs')
from felipe import verificaTaxonomia
```

Que retorna-va uma lista com o nível taxonomico. Como desafio optou-se por implementar uma nova forma de atacar o problema. Criou-se um novo metodo para o exercicio.

--------------------------------------

## **3.** Monte filtros de ocorrências por estados, nome de espécie (nome exato ou parte do nome) e categoria de ameaça.

3.1 Na resolução do exercicio_03 optou-se por trabalhar com DataFrame e utlizar o "loc" para criação dos filtros.
* Os filtros são criados a partir do DataFrame da seguinte forma:
```
mapa_bio = pd.read_csv(self.path)
mapa_bio.rename(columns={'Latitude':'lat','Longitude':'lon'}, inplace=True)

			st.write('Monte filtros de ocorrências por estados, nome de espécie (nome exato ou parte do nome) e categoria de ameaça, e outros filtros que julgar relevante.')
			lista_de_filtros = ['Municipio', 'Familia','Filo','Classe','Localidade', 'Nome cientifico']
			filtros = st.multiselect("Escolha os filtros: -> Municipio -> Familia -> Filo -> Classe -> Localidade -> Nome cientifico", lista_de_filtros)

			data = pd.DataFrame()
			f1,f2,f3,f4,f5,f6 = 1,1,1,1,1,1

			if filtros:
				 my_bar = st.progress(0)
				 for percent_complete in range(0, 100):
				 	my_bar.progress(percent_complete + 1)
                       for item in filtros:
				if item == 'Municipio':
					municipios = st.multiselect('Escolha os municipios', list(set(mapa_bio['Municipio']))) #, ["Londrina"]
					if not municipios:
						f1 = 1
					else :
						f1 = mapa_bio['Municipio'].isin(municipios)

                        ...

                        ...

				data = mapa_bio.loc[f1 & f2 & f3 & f4 & f5 & f6]

```
Se o filtro selecionado tiver contido na coluna correspondente do DataFrame, então um novo DataFrame é criado. No final o DataFrame "data" contem a junção de todos os filtros que existem, que é então utilizado para plotagem do mapa 3d através da interface gráfica criada pelo framework streamlit.
```
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
```
--------------------------------------

## **4.** Crie uma funcionalidade para avaliar se a informação de longitude e latitude corresponde a informação presente na localização.

4.1 Na resolução do exercicio_4 avaliou-se a solução do grupo anterior da residente Jéssica onde através da biblioteca reverse_geocode foi implementada a solução do exercicio.
* O input é o DataFrame total e o output são dois DataFrames, um com os resultados corretos e outro com os incorretos.
```

			cities =reverse_geocode.search(loc) #Faz processo reverso e através de lat long traz a cidade
			cities =  pd.DataFrame(cities) #Transforma a lista em dataframe
			#New dataset com lat long e a respectiva cidade
			newdf = mapa_bio[['lat','lon','Municipio']]
			comparecitiesTrue = []
			comparecitiesFalse = []
			for j in np.arange(0,len(newdf)):
				if newdf['Municipio'][j] != cities['city'][j]:
					comparecitiesFalse.append([mapa_bio['lat'][j],mapa_bio['lon'][j],mapa_bio['Municipio'][j],cities['city'][j]])
				if newdf['Municipio'][j] == cities['city'][j]:
					comparecitiesTrue.append([mapa_bio['lat'][j],mapa_bio['lon'][j],mapa_bio['Municipio'][j],cities['city'][j]])
			comparecitiesFalse = pd.DataFrame(comparecitiesFalse, columns=['lat','lon','Municipio Planilha', 'Reverse Geocode'])
			comparecitiesTrue = pd.DataFrame(comparecitiesTrue, columns=['lat','lon','Municipio Planilha', 'Reverse Geocode'])
```
--------------------------------------
## **5.** Teste da classe desenvolvida com os 3 arquivos passados.

A leitura dos 3 arquivos é  feita com o read_csv do pandas, dividindo por ";", como explicado no primeiro exercicio.

O residente Sávio testou os três arquivos na aplicação atestando seu correto funcionamento, o deploy no Heroku foi feito nessa fase, entretanto a versão mais nova da aplicação ainda não foi atualizada na nuvem.

--------------------------------------
## **6.** Documentação da solução

- Formato Livre
- Sugiro que utilizem a wiki do repositório git, pois aceita markdown
- A idéia é que os outros grupos possam utilizar as suas classes para testes, para isso é importante a documentação, bem como, comentários no código.

Conforme proposto a documentação foi feita na wiki do repositório git.

## **7.** Teste da sua solucao com ao menos dois outros arquivos do portal da biodiversidade do ICMBio.

O residente Lucas fez a aquisição de mais três base de dados do portal biodiversidade, testando na aplicação. Os quatro exercícios funcionaram corretamente após correção dos seguintes bugs pela residente Jéssica:
#  <p align="center"> **BUGS**</p>
------------------------------------------------------
* No exercicio 2 devido ao formato gerado pela lista, a incosistência dos arquivos com relação a "," e ";" gerava alguns erros que faziam que o gráfico não funcionasse corretamente.
* No exercicio 4 a base de dados com maior tamanho gerava erros, pois havia alguns algumas linhas que possuiam _strings_ ao invés da informação de Latitude e Longitude.
------------------------------------------------------
## **8.** Teste de uma das classes implementadas por outros grupos com arquivos de entrada obtidos por voce no portal, e um texto dos erros obtidos usando uma classe de outro grupo (resultados e possivelmente erros).
* Gerar Package

Durante a criação da aplicação foram utilizados metodos de classes de outros grupos como informado inicialmente nessa documentação. O package foi gerado com sucesso pela residente Leticia.

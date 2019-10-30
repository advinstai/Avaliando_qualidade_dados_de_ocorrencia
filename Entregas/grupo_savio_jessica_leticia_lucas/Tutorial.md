#
# <p align="center"> Tutorial</p>

## Projeto de Avaliação de qualidade de dados de biodiversidade

## 1.** Identificar a quantidade de linhas com dados faltantes.  
-> Leticia  
  
*=1.1 Documentaçao: No item 1 busca-se dar a informaçao da quantidade de itens faltando por coluna

* Fazemos a leitura do arquivo utilizando o pandas, csv_read:
  
* import pandas as pd  
* import os  
* print(os.getcwd())  
* data = pd.read_csv("./portalbio_export_16-10-2019-14-39-54.csv", sep=";")  
  
* utilizamos o ';' como separador porque existem alguns campos que utilizam virgulas no meio da informaçao da celula, podendo causar desconfiguraçao no arquivo.  
  
* Tendo o Dataframe, sao entao definidos as colunas/indices com o 'keys'  
  
* itensHash = data.keys()  

* Depois sao pegos todos os dados (data.values()) e enviados para a funçao ItemFaltante  

* Ali eh feito um somatorio do total de espacos vazios por coluna para cada linha  

* No final divide-se esse somatorio pela quantidade total de linhas para dar o percentual de itens faltantes em cada coluna  




## 2.** Para cada item identifique até qual nível taxônomico a ocorrência foi identificada.
-> Lucas

**3.** Monte filtros de ocorrências por estados, nome de espécie (nome exato ou parte do nome) e categoria de ameaça.
-> Savio

**4.** Crie uma funcionalidade para avaliar se a informação de longitude e latitude corresponde a informação presente na localização.
-> Jessica

**5.** Teste da classe desenvolvida com os 3 arquivos passados.

A leitura dos 3 arquivos pode ser feita com o read_csv do pandas, dividindo por ;, como explicado no primeiro exercicio, utilizando o streamlit. 



**6.** Documentação da solução

- Formato Livre

- Sugiro que utilizem a wiki do repositório git, pois aceita markdown

- A idéia é que os outros grupos possam utilizar as suas classes para testes, para isso é importante a documentação, bem como, comentários no código.

**7.** Teste da sua solucao com ao menos dois outros arquivos do portal da biodiversidade do ICMBio.

**8.** Teste de uma das classes implementadas por outros grupos com arquivos de entrada obtidos por voce no portal, e um texto dos erros obtidos usando uma classe de outro grupo (resultados e possivelmente erros).

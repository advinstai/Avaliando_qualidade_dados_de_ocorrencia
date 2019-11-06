# Realizando teste de ferramentas do grupo do Vitor

# dependencias: pandas, numpy e opencage
from analisadados.AnalisadordeDados import AnalisadordeDados
# criacao da classe 
# path do arquivo e separador
ad = AnalisadordeDados('portalbio_export_17-10-2019-13-06-22.csv', ';')
# analisar dados faltantes
ad.missingData()
# realizar uma pesquisa em uma coluna
ad.filter(["Municipio"], ["Londrina"])
# em mais de uma coluna do dataset
ad.filter(["Municipio", "Classe"], ["Londrina", "Actinopterygii"])
# checar nivel taxinomico
print(ad.nivelTax())
# checar lat long de uma sample de 10 elementos do dataset
print(ad.verificar_lat_log(10))
# Participantes:

* Alessandra
* Cristiano
* Duan Cleypaul
* Vitor

## Modo de uso:

```python
# dependencias: pandas, numpy e opencage
from analisadados.AnalisadordeDados import AnalisadordeDados
# criacao da classe 
# path do arquivo e separador
ad = AnalisadordeDados('portalbio_export_16-10-2019-14-39-54.csv', ';')
# analisar dados faltantes
ad.missingData()
# realizar uma pesquisa em uma coluna
ad.filter(["Municipio"], ["Londrina"])
# em mais de uma coluna do dataset
ad.filter(["Municipio", "Classe"], ["Londrina", ""])
# checar nivel taxinomico
print(ad.nivelTax())
# checar lat long de uma sample de 10 elementos do dataset
ad.verificar_lat_log(10)
```
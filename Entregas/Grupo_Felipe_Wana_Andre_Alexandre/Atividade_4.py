import pandas as pd
from opencage.geocoder import OpenCageGeocode
import json

class mapear:
    def __init__(self, caminho, separador = ',', chave = 'b230d495ac944577b6fd999bdfe087fd'):
        self.dados = pd.read_csv(caminho, separador)
        self.chave = chave

    def validar_localidade(self, lat, long, estado):
        geocode = OpenCageGeocode(self.chave)
        resultado = geocode.reverse_geocode(lat, long)

        if 'components' in resultado[0] and 'state' in resultado[0]['components'] and 'state_code' in resultado[0]['components']:
            if resultado[0]['components']['state'] == estado or resultado[0]['components']['state_code'] == estado :
                return True
            else:
                return False
        
        return False

'''
# Teste da classe:
m = mapear("iris.csv")
print(m.dados.head())
n = mapear("portalbio_export_16-10-2019-14-39-54.csv", ";")

# Posição válida
print("estado csv: ", n.dados.at[5,"Estado/Provincia"])
print("municipio csv: ", n.dados.at[5,"Municipio"])
print(n.dados.at[5,"Latitude"],n.dados.at[5,"Longitude"])
print(n.validar_localidade(n.dados.at[5,"Latitude"],n.dados.at[5,"Longitude"],n.dados.at[5,"Estado/Provincia"]))

# Posição inválida
print("estado csv: ", n.dados.at[246,"Estado/Provincia"])
print("municipio csv: ", n.dados.at[246,"Municipio"])
print(n.dados.at[246,"Latitude"],n.dados.at[246,"Longitude"])
print(n.validar_localidade(n.dados.at[246,"Latitude"],n.dados.at[246,"Longitude"],n.dados.at[246,"Estado/Provincia"]))
'''
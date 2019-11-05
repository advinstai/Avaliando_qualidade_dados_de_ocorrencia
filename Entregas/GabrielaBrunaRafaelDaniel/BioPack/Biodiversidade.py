import numpy as np
import pandas as pd 
from opencage.geocoder import OpenCageGeocode
import geopy.distance
    	
key = '09aadb1b1d8840acacfa0fcece0acb13'
geocoder = OpenCageGeocode(key)

class desafioBiodiversidade():
    def __init__(self,filePath):
        try:
            f = open(filePath,"r")
            self.originalData = f.readlines()
            self.data = [l.rstrip().split(";") for l in self.originalData]
            self.len = len(self.data)-1
            f.close()
        except:
            print("Error: cannot open file.")
            exit(1)  

    # Tópico 1 - Dados Faltantes
    def retornaMediaDadosFaltantesPorColuna(self):
        data = self.data
        
        nblank = [0]*len(data[0])
  
        for line in data:
            for ind,column in enumerate(line):
                if column == "Sem Informações" or column == "":
                    nblank[ind]+=1
 
        mean = [np.round((x/self.len)*100,2) for x in nblank]

        dict = {'Coluna': data[0], 'Faltantes':nblank, 'Média': mean}
        df = pd.DataFrame(dict)
        return df
    
    # Tópico 2 - Nível Taxonômico
    def retornaNivelTaxonomicoCadaOcorrencia(self):
        lista = self.data

        filo = []
        for i in range(len(lista[0])):
            
            if lista[0][i] == 'Especie':
              
                for k in range(1,len(lista)):
                    
                    if lista[k][i] != 'Sem Informações':
                        filo.append('{} - Especie'.format(k))
                    
                    elif lista[k][i-1] != 'Sem Informações':
                        filo.append('{} - Genero'.format(k))
                        
                    elif lista[k][i-2] != 'Sem Informações':
                        filo.append('{} - Familia'.format(k))
                        
                    elif lista[k][i-3] != 'Sem Informações':
                        filo.append('{} - Ordem'.format(k))
                    
                    elif lista[k][i-4] != 'Sem Informações':
                        filo.append('{} - Classe'.format(k))
                        
                    elif lista[k][i-5] != 'Sem Informações':
                        filo.append('{} - Filo'.format(k))
                        
                    else:
                        filo.append('{} - Reino'.format(k))
     
        return filo 

    # Tópico 3 - Filtro de Ocorrências
    def retonaSeOcorrenciaExiste(self, filterAmeaca):
        self.AmeacaList = []
        self.dataAux = []
        self.dataT = []
        
        # Matriz transposta
        for j in range(len(self.data[0])):        
            for i in range(len(self.data)-1):
                self.dataAux.append(self.data[i][j])
            self.dataT.append(self.dataAux)
            self.dataAux = []
        
        
        # Filtro estado de conservacao
        for i in range(len(self.dataT)):
            if self.dataT[i][0] == "Estado de conservacao":
                for j in range(len(self.dataT[i])):
                    if self.dataT[i][j] == filterAmeaca :
                        self.AmeacaList.append(["Amostra {}: {}: ".format(j, self.dataT[i-12][j]), filterAmeaca])
                    
        return self.AmeacaList
    
class GeoCode:

    def __init__(self,data):
        self.data = data
        self.topics = ["country","state","state_code","city"]

    def check_localization(self):
        indlat = self.data[0].index("Latitude")	
        indpais = self.data[0].index("Pais")
        
        print("Número de dados: ",len(self.data))
        result = []
        for ind,line in enumerate(self.data[1:]):
            lat = self.parse_float(line[indlat])
            lon = self.parse_float(line[indlat+1])

            geo = geocoder.reverse_geocode(lat,lon)   # retorna info de lat,lon
            comp = geo[0]['components']               # separa info de localizacao
            info = self.get_info(comp) 

            res = self.info_compare(line[indpais:indpais+3],info)
    
            if not res:
                rlat,rlon = self.get_latlon(line[indpais:indpais+3])
                dist = self.get_distance((lat,lon),(rlat,rlon))
                print(ind+1," Localização incorreta. Distância: ", np.round(dist,2),"km.")
                result.append(dist)
            else:
                print(ind+1," Localização correta.")
                result.append(True)
        return result

    # tenta a leitura de numeros float para latitude e longitude 
    def parse_float(self,info):
        try:
            value = float(info)
        except:
            value = 0.0
        return value


    # separa as informacoes de país, estado, código de estado e cidade
    def get_info(self,components):
        aux = []
        for elem in self.topics:
            try:
                value = components[elem]
            except:
                value = "Sem Informações"
            aux.append(value)
        return [aux[0],(aux[1],aux[2]),aux[3]]


    # compara as informacoes existentes
    def info_compare(self,line,info):

        correct = True
        for i, elem in enumerate(line):
            if line[i]!="Sem Informações" and info[i]!= "Sem Informações":
                if i==1:
                    if (line[i]!=info[i][0] and line[i]!=info[i][1]):
                        correct = False
                elif line[i]!=info[i]:
                    correct = False
        return correct 


    # busca a latitude e longitude de um endereco
    def get_latlon(self,line):

        address = self.concat_info(line) 
        geo = geocoder.geocode(address)
        lat,lon = geo[0]['geometry']['lat'], geo[0]['geometry']['lng']
        return lat,lon


    # concatena info em string para fazer a busca no geocode
    def concat_info(self,line):
        aux = ""
        for elem in line:
            if elem != "Sem Informações":
                aux += elem + ","
        return aux[:-1]


    # calcula distancia entre duas coordenadas
    def get_distance(self,coord1, coord2):
        return geopy.distance.geodesic(coord1,coord2).km
        

if __name__ == "__main__":
    filePath1 = "portalbio_export_16-10-2019-14-39-54.csv"
    filePath2 = "portalbio_export_17-10-2019-13-06-22.csv"
    filePath3 = "portalbio_export_17-10-2019-13-15-00.csv"   

    #PARTE GABRIELA
    biodiversidade = desafioBiodiversidade(filePath1)
    dadosfaltantes = biodiversidade.retornaMediaDadosFaltantesPorColuna()
    print(dadosfaltantes.to_string(index=False))

    #PARTE BRUNA
    niveltax = biodiversidade.retornaNivelTaxonomicoCadaOcorrencia()
    print(niveltax)

    #PARTE RAFAEL
    ocorrencias = biodiversidade.retonaSeOcorrenciaExiste("Espécie Ameaçada")
    print(ocorrencias)

    #PARTE DANIEL
    gCode = GeoCode(biodiversidade.data)
    result = gCode.check_localization()
    print(result)

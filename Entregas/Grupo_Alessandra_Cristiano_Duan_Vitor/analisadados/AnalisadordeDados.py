import numpy as np
import pandas as pd
from opencage.geocoder import OpenCageGeocode
from operator import itemgetter


class AnalisadordeDados:

    def __init__(self, path, sep):
        with open(path, 'r') as arq:
            self.__txt = arq.readlines()
        self.__sep = sep
        self.__path = path

    def __structlist(self):
        lst = [[a.replace("\n", "") for a in y.split(self.__sep)]
               for y in self.__txt]
        return lst

    def __column(self):
        org = self.__structlist()
        cat = org[0]
        out = []
        for i in range(len(org[0])):
            b = [a[i] for a in org]
            out.append(b)
        return out, cat

    def __structcsv(self, header, title, data):
        with open(title, 'w') as out:
            out.write(";".join(header))
            out.write("\n")
            for item in data:
                out.write(str(item))

    def filter(self, category, search, stype="or", outputfile='resultado_busca.csv'):
        # Filtra as ocorrencias segundo as caracteristicas indicadas.
        # Exemplo de uso AnalisadordeDados.filter(["Municipio"], ["Londrina"])
        # Parametros:
        # **category** - característica a ser avaliada; search - parametros de filtro das informações; **stype**: tipo de
        # busca, "and" (retorna itens que possuam todas os parametros informados) e "or" (retorna itens que possuam
        # ao menos um dos parametros informados), por default "or"; **outputfile** - nome do arquivo de saída com os
        # resultados filtrados, por default 'resultado_busca.csv'.

        # Observações:#1
        #   1. Este método diferencia letras maiúsculas e minúsculas
        #   2. Cada argumento de busca deve ser respectivo à sua categoria, ou seja, devem estar na mesma ordem em suas respectivas listas

        if len(category) != len(search):
            # Apresenta erro caso a quantidade de categorias e argumentos de busca não forem condizentes
            print(
                "Erro: a quantidade de categorias e argumentos de busca não são condizentes")

        else:
            # Cria dicionário vinculando cada categoria aos seus respectivos argumentos
            dic = {}
            for x in range(len(category)):
                dic[category[x]] = search[x]

            # Utiliza método privado para organizar os dados segundo suas colunas
            data, cat = self.__column()

            # Seleciona as colunas de acordo com as categorias informadas
            ref = [i for i in data if i[0] in category]

            # Cria matriz de avaliação os argumentos por categoria: 1 para Verdadeiro e 0 para Falso
            temp = [[1 if info in str(dic[list[0]])
                     else 0 for info in list] for list in ref]

            # Avalia as correspondencia em uma mesma ocorrencia: 0 para sem correspondencia, 1 para correspondencia do tipo "ou" e
            # n para correspondencia do tipo "e"
            evaluate = list(np.sum(temp, axis=0))

            # Seleciona o tipo de filtro
            if stype == "and":
                # Filtro do tipo "e"
                output = [self.__txt[x]
                          for x, ev in enumerate(evaluate) if ev == len(category)]
            else:
                # Filtro do tipo "ou"
                output = [self.__txt[x]
                          for x, ev in enumerate(evaluate) if ev >= 1]

            # Utiliza método privado para criar arquivo .csv com as ocorrencias filtradas
            self.__structcsv(cat, outputfile, output)

            # Calcula a quantidade de ocorrencias filtradas
            resultados = len(output)

            # Informa a quantidade de ocorrencias filtradas e o nome do arquivo .csv criado
            print("%d resultados.\nArquivo %s criado com sucesso!" %
                  (resultados, outputfile))

    # Crie uma funcionalidade para avaliar se a informação de longitude e latitude corresponde
    #  a informação presente na localização

    def verify_lat_long(self, city, lat, long):
        key = '65b25c705a5349ad99c824ca809363b7'
        geocoder = OpenCageGeocode(key)
        results = geocoder.reverse_geocode(lat, long)
        try:
            r_city = results[0]['components']['city']
        except Exception as identifier:
            try:
                r_city = results[0]['components']['island']
            except Exception as identifier:
                r_city = ""
        self.pbar.update(1)
        return r_city == city

    def call(self):
        df = pd.read_csv(self.__path, sep='\n', delimiter=';')
        df_sample = df.sample(n=10, random_state=1)
        count = {}
        for i, (lat, long, city) in enumerate(zip(df_sample['Latitude'], df_sample['Longitude'], df_sample['Municipio'])):
            count[i] = self.verify_lat_long(city, lat, long)
        return count

    def missingData(self):
        count = {}
        df = pd.read_csv(self.__path, sep='\n', delimiter=';')
        # Realiza a contagem somente de valores em branco ou "Sem Informacoes"
        for field in list(df):
            count[field] = round((100*sum(
                [1 if value == "" or value == "Sem Informações" else 0 for value in df[field]]) / len(df)), 1)
        # Ordena o dictionary em função da ocorrência dos values.
        for key, value in sorted(count.items(), key=itemgetter(1), reverse=True):
            # Imprime somente a lista que contém dados faltantes
            if value != 0:
                print(key, ":", value, "%")

    def nivelTax(self):
        # Retorna o nivel taxonomico mais especifico identificado em cada item do arquivo csv
        # Exemplo de uso: AnalisadordeDados.nivelTax()
        # ----------- OUTPUT (salvo em self.nvTax):
        # [['Nivel Taxonomico de 0:','Especie'],['Nivel Taxonomico de 1:','Genero'],...]
        
        with open(self.__path, 'r') as file:
            arquivo = list(file)
            print("\n------Nível Taxonômico-----")
            # aloca a taxonomia a ser lida na iteracao
            self.temp = [linha.strip("\n").split(';') for linha in arquivo]
            self.nvTax = []
            # aloca o nivel taxonomico de cada item no formato:
            # [['Nivel Taxonomico de 1:','Especie'],['Nivel Taxonomico de 2:','Genero'],...]
            for i in range(len(arquivo[1:])):
                if self.temp[i][21].lower() != "Sem Informações".lower() and self.temp[i][21] != "":
                    self.nvTax.append(
                        ["Nível Taxônomico de {}:".format(i), "Espécie"])
                elif self.temp[i][20].lower() != "Sem Informações".lower() and self.temp[i][20] != "":
                    self.nvTax.append(
                        ["Nível Taxônomico de {}:".format(i), "Gênero"])
                elif self.temp[i][19].lower() != "Sem Informações".lower() and self.temp[i][19] != "":
                    self.nvTax.append(
                        ["Nível Taxônomico de {}:".format(i), "Família"])
                elif self.temp[i][18].lower() != "Sem Informações".lower() and self.temp[i][18] != "":
                    self.nvTax.append(
                        ["Nível Taxônomico de {}:".format(i), "Ordem"])
                elif self.temp[i][17].lower() != "Sem Informações".lower() and self.temp[i][17] != "":
                    self.nvTax.append(
                        ["Nível Taxônomico de {}:".format(i), "Classe"])
                else:
                    self.nvTax.append(
                        ["Nível Taxônomico de {} :".format(i), "Filo"])

        return self.nvTax

# a = AnalisadordeDados('/home/vitorbezerra/Documents/python/Exercicios/portalbio_export_16-10-2019-14-39-54.csv', ';')
# print(a.nivelTax())
# a.missingData()
# a.filter(["Municipio"], ["Londrina"])
# print(a.call())

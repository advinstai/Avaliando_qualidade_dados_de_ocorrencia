import numpy as __np
import pandas as pd
from opencage.geocoder import OpenCageGeocode


class AnalisadordeDados:

    def __init__(self, path, sep):
        with open(path, 'r') as arq:
            self.__txt = arq.readlines()
        self.__sep = sep
        self.__path = path
        self.__txt = []

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
            evaluate = list(self.__np.sum(temp, axis=0))

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
        df = pd.read_csv(self.__path)
        df_sample = df.sample(n=10, random_state=1)
        count = {}
        for i, (lat, long, city) in enumerate(zip(df_sample['Latitude'], df_sample['Longitude'], df_sample['Municipio'])):
            count[i] = self.verify_lat_long(city, lat, long)
        return count

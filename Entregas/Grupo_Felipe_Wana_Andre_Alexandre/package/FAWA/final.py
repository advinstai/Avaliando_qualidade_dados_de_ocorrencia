# Bibliotecas
import sys
import pandas as pd
import numpy as np
import csv
from opencage.geocoder import OpenCageGeocode

# Classes
class FindNan:
    
    def __init__(self, my_csv):
        try:
            self.df = pd.read_csv(my_csv, sep='\n', delimiter=';')  # Cria o dataframe através do arquivo CSV
            self.nan_df = []
        except IOError as e:
            print('Could not read the file', my_csv) # Caso o arquivo com o nome citado não exista, o programa é encerrado
            print ('I/O error({0}): {1}'.format(e.errno, e.strerror))  # Indica o erro ocorrido 
            sys.exit()
        
        self.fields = list(self.df)  # Cria uma lista com todos os campos presentes no CSV
        self.n_lines = len(self.df)  # Atribui o número de linhas do arquivo a variável n_lines
     
    def getEmpty(self):  # Método que retorna a média de dados faltantes por campo no arquivo CSV
        count_mean = {}  # Dicionário com a média de dados faltantes pela quantidade de linhas
        for field in self.fields:  # Itera sobre cada campo na lista de campos do arquivo CSV
            
            # List comprehension:
            # Soma 1 se a célula não tiver informação ou 0 se a célula tiver informação 
            count_mean[field] = sum([1 if value == "" or value == "Sem Informações" else 0 for value in self.df[field]])
            
            # Divide a soma dos dados faltantes pelo número de linhas para obtger a média
            count_mean[field] = (count_mean[field]/self.n_lines)*100  #  A multiplicação por 100 obtém a porcentagem dos dados faltantes
        self.nan_df = pd.DataFrame([count_mean])  # Transforma o dicionário em um dataframe com as porcentagens de dados faltantes
        return self.nan_df
    
    def printReport(self): # Método que envia um relatório dos dados faltantes
        fr = open('report', 'w')
        print('\n')
        print('***********************************************')
        print('Relatório dos dados faltantes')
        print('***********************************************')
        print('\n')
        fr.write('item'+';'+'dados faltantes(%)'+'\n')
        for column in self.nan_df.columns:
            print(column , ':', self.nan_df[column].values[0], ' %')  # Printa os dados faltantes na tela
            fr.write(column+';'+str(self.nan_df[column].values[0])+'\n') # Gera um CSV com a porcentagem dos dados faltantes
        fr.close()
        return fr  # O método retorna o arquivo com o relatório de dados faltantes
                    # A primeira linha do arquivo são os títulos das colunas
    
    


#esta classe utiliza métodos estáticos @staticmethod
#estes métodos podem ser acessados fora dos objetos, como se fosse uma função solta. É como se apenas estivesse agrupando as funçoes para
#não ficaram perdidas ao importar para outros arquivos

# exemplo: from Felipe import AvaliaTax
# meusDados = leiaTudo(arquivo)
# AnaliaTax.verificaTaxonomia(meusDados)
# 
# Não precisa fazer:
# meuObjeto = AvaliaTax()
# e depois: meuObjeto.verificaTaxonomia(meusDados)
# pois neste projeto só vai ter 1 objeto AvaliaTax, não faz sentido eu criar mais de um. 
# 
# quando uma classe vira um aglomerado de funções, para projetos pequenos, fica mais fácil de entender. 

class AvaliaTax:
    
    #shared atribute
    defaultFile =  "portalbio_export_16-10-2019-14-39-54.csv"
    
    def __init__(self):
        print("Nao precisa instanciar esta classe, pode fazer AvaliaTax.metodo() para utilizar as funções")
    
    #usar este método apenas para testes internos. Utilizar o método da classe MyData para carregar o arquivo
    @staticmethod
    def carregarCSV(path=None):
      
        # caso não tenha parâmetro: pegar do arquivo padrão:
        caminho = path if path else AvaliaTax.defaultFile
        
        arquivo = None
        
        try:
            arquivo = open(caminho, "r")
        except IOError as e:
            print ("erro ao abrir o arquivo: " , e.args)
            return
        
        # Lê tudo de uma vez:    
        base = arquivo.readlines()
        
        arquivo.close()
            
        dadosXY = list()
    
        # Converte CSV em matriz
        
        try:
            dadosXY = list(map(lambda l: l.split(";"), base))
        except AttributeError as e:
            print ("Falha ao processar o arquivo CSV, deve ter muitas colunas faltando. " , e.args)
        
        return dadosXY
    
    @staticmethod
    def getColuna(k,dados):
        return map(lambda x:x[k], dados )
    
    
    # verifica se tem uma celula fazia ou não:
    @staticmethod
    def vazio(celula): return celula == "Sem Informações" or celula == ""
    
    vaziop = "Sem Informações" # atributo shared
    
    #no python3 colocar o list antes do map
    #implementação antiga:
    @staticmethod
    def verificaTaxonomia(dados):
        """
            nível taxonomico: [1-7]
            reino filo classe ordem familia genero especie
            
            exemplo: nivel = 5
                    1        2   3             4         5
               Animal Chordata Aves Ciconiiformes Ardeidae 0 0
    
        """
        
        dadosXY = dados[1::] # pega apenas o campo dos dados (Retira o rotulo)
       
        nivelTaxonomico = list()
        
        try:
            colunaFilo = dados[0].index('Filo') #captura o índice do rotulo que contem o filo
            
            #alguns reinos estão faltando
            #quando se tem o Filo, o reino é obvio, então começamos a percorrer 
            #a partir do filo
            
        except ValueError as e:
            print( "formato dos rótulso inválido ou sem a classificação taxonomica: ", e.args)
            return # sair da função
        
        for linha in dadosXY:
        
            tax = linha[colunaFilo:colunaFilo+7] # examina apenas as colunas com a classificação 
             # para cada coluna que contem a taxonomia ver quais são nulas, 
             # caso nenhuma coluna é nula a classificacao é completa: 7
            nivel =  7 - sum ( list(map(AvaliaTax.vazio, tax))  )
             
             # adiciona o nível calculado na listagem geral
            nivelTaxonomico.append(nivel)
        
        return nivelTaxonomico
    
    @staticmethod
    def listaMetodos(): return dir(AvaliaTax)
    
    @staticmethod
    def pandasAdapter(pandaDataframe):
        out = pandaDataframe.to_numpy()
        
        outlist =  np.array(out, dtype=str).tolist()
        
        outlist.insert(0, list(pandaDataframe))
        
        return outlist
        
    
    @staticmethod
    def verificaTaxonomiaAsNumpy(dadosd):
        
        '''
        Entrada: lista das listas de todos os dados, incluindo o cabeçalho, use o Adapter para funcionar com o Pandas
        Saída: faz o mesmo do verificaTaxonomia(dados), porém retorna uma lista 1D de números no formato do numpy
        este método é mais resumido devido as funcionalidados do numpy.
        '''
        
        try:
            dadosnp = np.array(dadosd[1::]) #converte os dados (e exclui o cabeçalho)
        except TypeError as e:
            print("tipo inválido, muitas colunas faltantes ou numpy não importado/instalado: ", e.args)
            print("use import numpy as np ou !conda install numpy=1.16.15")
            return -1
        
        #verifica em que lugar da tabela tem a taxonomia
        try:
            colunaFilo = dadosd[0].index('Filo')
        except ValueError:
            print("falha ao procurar as colunas do nível taxonomico, verifique se está no formato 'filo'")
            return -1
        
        
        #aqui acontece o procedimento (ver detalhes na documentação)
        #usei a técnica da máscara de matriz
        return 7 - np.sum( dadosnp[:,colunaFilo:colunaFilo+6] == AvaliaTax.vaziop , 1)
    

'''
The above ANSI escape code will set the text colour to bright green. The format is;
\033[  Escape code, this is always the same
1 = Style, 1 for normal.
32 = Text colour, 32 for bright green.
40m = Background colour, 40 is for black.
'''
#Atividade 3

class wana:
	dados = []
	df = None
	dict_header = {}
	header = None
	auxh = []

	def __init__(self, filea=None, sep=None):
                self.file0 = filea
		
		#try:

			#self.file = pd.read_csv(file, sep=sep)

		#except:
			#print('Could not open the file')
			#sys.exit(1)

	def dict(self):
		self.df = self.file0.apply(lambda x: x.astype(str).str.lower()) # turn all my data to lower case
		self.header = self.df.columns.tolist() # getting the list of header' names
		#creating a dictionary with column' names
		for i in range(len(self.header)):
			self.dict_header[i] = self.header[i]

	def entry(self):
		self.dict()
		entry = input('\033[1;31;47m{}\n\033[1;30;47m PLEASE, ENTER THE INDICES YOU WOULD LIKE TO FILTER, SEPARATED BY SPACE: \n'.format(self.dict_header))
		list_filter  = entry.split() # turning it in a list os string
		int_list = [int(i) for i in list_filter] #list comprehansion to convert the string values into int values
		for i in int_list:
			for j in range(len(self.header)):
				if i == j:
					self.dfaux = list(set(self.df[self.header[i]]))
					print("{}: {}".format(self.header[i],', '.join(self.dfaux)))
					print("")
					f = input('Based on the options above, %s:' %self.header[i])
					self.auxh.append(self.header[i])
					self.dados.append(f)


	def show_and_save(self):
		self.dict()
		self.entry()
		for k in range(len(self.dados)):
		# selecting rows based on condition 
			data = self.df[self.df[self.auxh[k]] == self.dados[k]] 

		print('result for:' , '-'.join(i for i in self.dados))
		print(data) if len(data) > 0 else print('result is empty')
		a = input("would you like to save the result [yes]/no?")
		if a == 'no':
			print('file not saved')
		elif a == 'yes' or a == '':
			exemplo= "/home/wanabb/repo-git/repositorio-git/pesquisa1.csv"
			output = input('enter with the path and name, ex: %s \n' %exemplo)
			data.to_csv(output, sep=';')
			print('file saved')
		else:
			print('wrong answer, try again :(')


class mapear:
    def __init__(self, caminho=None, chave = 'b230d495ac944577b6fd999bdfe087fd'):
        self.dados = caminho
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
			

if __name__ == '__main__':
	print('Grupo FAWA')
	



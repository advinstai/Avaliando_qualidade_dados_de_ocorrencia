class AnalisadordeDados:
    def __init__(self, arquivo):
        self.arquivo = list(open(arquivo))

    def nivelTax(self):
        print("\n------Nível Taxonômico-----")
        
        self.temp = [linha.strip("\n").split(';') for linha in self.arquivo]     # aloca a taxonomia a ser lida na iteracao       
        self.nvTax = []     # aloca o nivel taxonomico de cada item no formato: 
                            # [['Nivel Taxonomico de 1:','Especie'],['Nivel Taxonomico de 2:','Genero'],...]
       
        for i in range(len(self.arquivo[1:])):
            if self.temp[i][21].lower() != "Sem Informações".lower() and self.temp[i][21] != "":
                self.nvTax.append(["Nível Taxônomico de {}:".format(i),"Espécie"])
            elif self.temp[i][20].lower() != "Sem Informações".lower() and self.temp[i][20] != "":
                self.nvTax.append(["Nível Taxônomico de {}:".format(i),"Gênero"])
            elif self.temp[i][19].lower() != "Sem Informações".lower() and self.temp[i][19] != "":
                self.nvTax.append(["Nível Taxônomico de {}:".format(i),"Família"])
            elif self.temp[i][18].lower() != "Sem Informações".lower() and self.temp[i][18] != "":
                self.nvTax.append(["Nível Taxônomico de {}:".format(i),"Ordem"])
            elif self.temp[i][17].lower() != "Sem Informações".lower() and self.temp[i][17] != "":
                self.nvTax.append(["Nível Taxônomico de {}:".format(i),"Classe"])
            else:
                self.nvTax.append(["Nível Taxônomico de {} :".format(i),"Filo"])
	        
        # Usar linhas abaixo para imprimir valores taxonomicos de cada nivel, a titulo de teste
        #for i in self.nvTax[:50]:
        #   print(i)
        #
        return self.nvTax

# Testando metodos da classe:
#obj = AnalisadordeDados("portalbio_export_28-10-2019-16-30-36.csv")
#obj.nivelTax()

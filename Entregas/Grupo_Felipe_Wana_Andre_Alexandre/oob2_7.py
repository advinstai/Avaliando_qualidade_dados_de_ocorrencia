class testes:
    """ 
    classe de testes 
    
    """
    
    pathBase = "db/"
    
    arquivos = [
     "portalbio_export_04-11-2019-20-55-04.csv" ,
     "portalbio_export_05-11-2019-09-57-30.csv" ,
     "portalbio_export_17-10-2019-11-22-06.csv" ]
    
    log = "logTeste.txt"
    
    
    @staticmethod
    def teste1(default=1, log=None):
        """
        primeira fase de teste Carregamento de arquivos csv e contagens
        
            * Itens 1 e 2
    
        
        :param default: padrão de testes, por enquanto só tem 1
        :param log: ative para não printar tudo na tela
        :return: 1 se sucesso, None se erro ou -1 caso haja problemas nas classes importadas
        """
        
        try: #lista das classes usadas
            assert wana
            assert MyData
            assert AvaliaTax 
            # se algumas delas nao existirem no contexto aparece uma exepction
        except NameError:
            print("classes nao encontradas ou com nomes errados")
            return -1
            
        if default!=1:
            raise NotImplementedError("Fazer, implementar outros testes ou usar teste1(1)")
        
        for arquivo in testes.arquivos:
            
            mydata = MyData(pathBase+arquivo)
            
            res1 = mydata.getEmpty()
            
            if not log: print(res1)
            
            dadosN = AvaliaTax.pandasAdapter(mydata.df)
            
            res2 = AvaliaTax.verificaTaxonomiaAsNumpy(dadosN)
            
            if not log: print(res2)
            
        
        return 1

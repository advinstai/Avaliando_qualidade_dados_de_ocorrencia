from BioPack.Biodiversidade import desafioBiodiversidade as bio

filePath1 = "/home/rafael/HUB/Atividades/OOP02/Avaliando_qualidade_dados_de_ocorrencia/Entregas/GabrielaBrunaRafaelDaniel/portalbio_export_16-10-2019-14-39-54.csv"

#PARTE GABRIELA
biodiversidade = bio(filePath1)
dadosfaltantes = biodiversidade.retornaMediaDadosFaltantesPorColuna()
print(dadosfaltantes.to_string(index=False))



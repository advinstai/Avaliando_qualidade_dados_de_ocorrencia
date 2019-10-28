import streamlit as st

import icmbio_search as bio

import pandas as pd
import numpy as np
#import folium
#import math


from IPython.display import Markdown, display


def special_print(title, content):
    display(Markdown("### %s:" % title))
    print(content)
    return None
    
    



####################################################################################
#
# Initializing all data

key = '09aadb1b1d8840acacfa0fcece0acb13'

#url = "PortalBio 00002.csv"
url = "PortalBio 00043.csv"
#url = "PortalBio 00555.csv"
#url = "PortalBio 03912.csv"
#url = "PortalBio 58411.csv"

TAXONOMY_COLUMNS = ['Filo', 'Classe', 'Ordem', 'Familia', 'Genero', 'Especie']
LOCATION_COLUMNS = ['Pais', 'Estado/Provincia', 'Municipio', 'Latitude', 'Longitude']
LOCATION_SAMPLING = 2 # number of locations to check

FILTER_FIELDS = ['Municipio','Filo']
FILTER_VALUES = [['Nova Friburgo','Niquelândia','Vitoria','Natal'],['Mollusca','Magnoliophyta']]



biodiversity = bio.getBiodiversity(url, key, TAXONOMY_COLUMNS, LOCATION_COLUMNS)
biodiversity.checkEmpty()
biodiversity.getTaxonomy(col_name='Nível Taxonômico')
biodiversity.filterFields(FILTER_FIELDS, FILTER_VALUES)
biodiversity.checkCoordinates(LOCATION_SAMPLING)




st.header("CMBio Visualizer")


biodiversity.url


####################################################################################
#
# Show sample of each output - raw data load

special_print("File URL", biodiversity.url)
special_print("Raw file info", biodiversity.data_info)
special_print("Raw file sample", biodiversity.df_data.head(1).T)
special_print("Dataframe columns", biodiversity.df_columns)

####################################################################################
#
# Show sample of each output - data missing analysis

special_print("Data missing sample (1 = missing)", biodiversity.df_dataNAN.head(5).T)
special_print("Data missing statistics (%)", biodiversity.df_data_missing)

####################################################################################
#
# Show sample of each output - show taxonomic info

special_print("Raw data sample after taxonomic level inclusion", biodiversity.df_data.head(1).T)
special_print("Taxonomic info", biodiversity.df_taxonomy_info)
special_print("Taxonomy sample", biodiversity.df_taxonomy.head(3).T)

####################################################################################
#
# Show sample of each output - filtered data

special_print("Filtered data info", biodiversity.filtered_info)
special_print("Filtered data sample", biodiversity.df_filtered.head(1).T)

####################################################################################
#
# Show sample of each output - show location info

special_print("Applied filters", FILTER_FIELDS)
special_print("Applied filter values", FILTER_VALUES)

special_print("Sample of locations to check", biodiversity.df_location_sample.head(1).T)

####################################################################################
#
# Show sample of each output - show map with reported observations

display(Markdown("### Observations (click to see more details)"))

st.write(biodiversity.observations_map)



df = pd.DataFrame(
    np.random.randn(1000, 3) / [50, 50, 100] + [37.76, -122.4, 0],
    columns=['lat', 'lon', 'Confidence'])


st.deck_gl_chart(
    viewport={
        'latitude': 37.76,
        'longitude': -122.4,
        'zoom': 11,
        'pitch': 50,
    },
    layers=[{
        'type': 'HexagonLayer', # GridLayer, LineLayer,PointCloudLayer,TextLayer, ScreenGridLayer
        'data': df,
        #'radius': 200,
        #'encoding': {'getRadius': 'Confidence'},
        #'elevationScale': 4,
        #'elevationRange': [0, 1000],
        'pickable': True,
        'extruded': True,
        #'onHover' : ,
        #'onClick': ,
        #'opacity': ,
        #'visible': ,
        #'highlightColor': [255, 0, 0, 128],
        'autoHighlight': True,
        #'coordinateSystem': ,
        }, {
        'type': 'ScatterplotLayer',
        'data': df,
    }])


"""
Para usar dentro do parâmetro encoding acima:

Instead of “getPosition” : use “getLatitude” and “getLongitude”.
Instead of “getSourcePosition” : use “getLatitude” and “getLongitude”.
Instead of “getTargetPosition” : use “getTargetLatitude” and “getTargetLongitude”.
Instead of “getColor” : use “getColorR”, “getColorG”, “getColorB”, and (optionally) “getColorA”, for red, green, blue and alpha.
Instead of “getSourceColor” : use the same as above.
Instead of “getTargetColor” : use “getTargetColorR”, etc.

Plus anything accepted by that layer type. For example, for ScatterplotLayer you can set fields like “opacity”, “filled”, “stroked”, and so on.

Ver mais em: https://deck.gl/#/documentation/deckgl-api-reference/layers/layer?section=pickable-boolean-optional-


Como mudar a inclinação do mapa
Como mostrar um popup com info
Como mudar o ícone da mãozinha

"""
from package import icmbio_search as bio

import streamlit as st

import pandas as pd
import numpy as np 


####################################################################################
#
# Initializing STREAMLIT APP


st.title("ICMBio Visualizer")
st.sidebar.header("Settings")

key = '09aadb1b1d8840acacfa0fcece0acb13'
key = st.sidebar.text_input("Product key", key)

FILES = ["PortalBio 00002.csv",
        "PortalBio 00043.csv",
        "PortalBio 00555.csv",
        "PortalBio 03912.csv",
        "PortalBio 58411.csv"]
url = "Arquivos_csv/" + st.sidebar.selectbox("Select a file", FILES)
st.write("Reading file %s" % url)

TAXONOMY_COLUMNS = ['Filo', 'Classe', 'Ordem', 'Familia', 'Genero', 'Especie']
TAXONOMY_COLUMNS = st.sidebar.multiselect("Taxonomy columns to analyse", TAXONOMY_COLUMNS, TAXONOMY_COLUMNS)

LOCATION_COLUMNS = ['Pais', 'Estado/Provincia', 'Municipio', 'Latitude', 'Longitude']
LOCATION_COLUMNS = st.sidebar.multiselect("Location columns to analyse", LOCATION_COLUMNS, LOCATION_COLUMNS)

LOCATION_SAMPLING = st.sidebar.slider("Number of samples to plot", 1, 20, 2)

# class initializer
biodiversity = bio.getBiodiversity(url, key, TAXONOMY_COLUMNS, LOCATION_COLUMNS)
#if st.checkbox("Show raw data (%d rows x %d columns)" % (biodiversity.df_data.shape[0],biodiversity.df_data.shape[1])):
#    st.dataframe(biodiversity.df_data)

# missing data analysis
biodiversity.checkEmpty()
if st.checkbox("Show missing data statistics (% of data missing)"):
    st.dataframe(biodiversity.df_dataNAN)

# run taxonomic analysis
biodiversity.getTaxonomy(col_name='Nível Taxonômico')
if st.checkbox("Show taxonomic data (%d rows x %d columns)" % (biodiversity.df_taxonomy.shape[0],biodiversity.df_taxonomy.shape[1])):
    st.dataframe(biodiversity.df_taxonomy)

# filtering data to show
FILTER_FIELDS = st.sidebar.multiselect("Please select one or more columns to filter by", list(biodiversity.df_data.columns))
FILTER_VALUES = [st.sidebar.multiselect("Filter values for column %s"%column, biodiversity.df_data[column].unique()) for column in FILTER_FIELDS]
biodiversity.filterFields(FILTER_FIELDS, FILTER_VALUES)
biodiversity.getTaxonomy(col_name='Nível Taxonômico')
if st.checkbox("Show filtered data (%d rows x %d columns)" % (biodiversity.df_filtered.shape[0],biodiversity.df_filtered.shape[1])):
    st.dataframe(biodiversity.df_filtered)

# check if latitude and longitude are correct or not
#biodiversity.checkCoordinates(LOCATION_SAMPLING)
#biodiversity.df_location_sample = biodiversity.df_location_sample.rename(columns={'AdjustedLatitude': 'lat', 'AdjustedLongitude': 'lon'})
#if st.checkbox("Show locations sample data (%d rows x %d columns)" % (biodiversity.df_location_sample.shape[0],biodiversity.df_location_sample.shape[1])):
#    st.dataframe(biodiversity.df_location_sample[["lat", "lon", "Municipio", "ReversedAddress"]])
#st.map(biodiversity.df_location_sample)



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
        #'extruded': True,
        #'onHover' : ,
        #'onClick': ,
        #'opacity': ,
        #'visible': ,
        #'highlightColor': [255, 0, 0, 128],
        #'autoHighlight': True,
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
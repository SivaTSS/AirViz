

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
import plotly.graph_objects as go
import hiplot as hip
import utils

if 'df' in st.session_state:
    df = st.session_state.df
else:
    df = utils.load_data("dataset/refined/annual_conc_by_monitor.parquet")
    st.session_state.df=df

if 'df_aqi' in st.session_state:
    df_aqi = st.session_state.df_aqi
else:    
    df_aqi = utils.load_data("dataset/refined/annual_aqi_by_county.csv")
    st.session_state.df_aqi=df_aqi

if 'geojson_data' in st.session_state:
    geojson_data= st.session_state.geojson_data
else:
    with open("geojson/USA_state.geojson", "r") as geojson_file:
        geojson_data = json.load(geojson_file)
        st.session_state.geojson_data = geojson_data

mapbox_layout = utils.mapbox_layout
params=utils.params
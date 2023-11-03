import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
import plotly.graph_objects as go
import hiplot as hip


st.set_page_config(layout="wide")#📊
st.set_option('deprecation.showPyplotGlobalUse', False)

@st.cache_data
def load_data(filepath):
    if "parquet" in filepath:
        data = pd.read_parquet(filepath)
    elif "csv" in filepath:
        data = pd.read_csv(filepath)
    else:
        raise Exception("file format not supported")
    return data



st.session_state.df = load_data("dataset/refined/annual_conc_by_monitor.parquet")
st.session_state.df_aqi = load_data("dataset/refined/annual_aqi_by_county.csv")


st.title("AirViz")
st.write(
    """
The goal of this webapp is to help users understand more about the air we breath.

 
"""
)

st.subheader("Introduction")

st.write(
    """
Air quality is a critical aspect of our environment that directly impacts the health and 
well-being of individuals and the ecosystems we inhabit. It refers to the measurement of 
various pollutants and particulate matter in the atmosphere, which can have adverse effects 
on human health and the environment.

"""
)
st.subheader("Learn about Parameters")
params = [
    "Carbon monoxide",
    "Sulfur dioxide",
    "Nitrogen dioxide (NO2)",
    "Ozone",
    "PM10 Total 0-10um STP",
    "PM10-2.5 - Local Conditions",
    "PM2.5 - Local Conditions",
    "Acceptable PM2.5 AQI & Speciation Mass",
    "Lead (TSP) STP",
    "Barometric pressure",
    "Relative Humidity ",
    "Dew Point",
    "Outdoor Temperature",
    "Wind Direction - Resultant",
    "Wind Speed - Resultant",
]

st.session_state.params = params

param_info = {
    "Carbon monoxide": {
        "description": "Carbon monoxide is a colorless, odorless gas produced by incomplete combustion of carbon-containing fuels. High levels of CO can be harmful, affecting air quality and human health. Monitoring CO is vital because it can lead to respiratory problems and, at elevated concentrations, pose a risk to life.",
        "air_quality_levels": {
            "Good": "0-4.4 ppm",
            "Moderate": "4.5-9.4 ppm",
            "Unhealthy for Sensitive Groups": "9.5-12.4 ppm",
            "Unhealthy": "12.5-15.4 ppm",
            "Very Unhealthy": "15.5-30.4 ppm",
            "Hazardous": "30.5+ ppm",
        },
    },
    "Sulfur dioxide": {
        "description": "Sulfur dioxide is a pungent gas emitted from sources like power plants and industrial processes. It can contribute to poor air quality, cause respiratory issues, and lead to the formation of acid rain, harming both human health and the environment.",
        "air_quality_levels": {
            "Good": "0-35 ppb",
            "Moderate": "36-75 ppb",
            "Unhealthy for Sensitive Groups": "76-185 ppb",
            "Unhealthy": "186-304 ppb",
            "Very Unhealthy": "305-604 ppb",
            "Hazardous": "605+ ppb",
        },
    },
    "Nitrogen dioxide (NO2)": {
        "description": "Nitrogen dioxide is a reddish-brown gas, often associated with vehicle emissions. High levels of NO2 are harmful to respiratory health and can contribute to the formation of ground-level ozone and fine particulate matter, impacting air quality.",
        "air_quality_levels": {
            "Good": "0-53 ppb",
            "Moderate": "54-100 ppb",
            "Unhealthy for Sensitive Groups": "101-360 ppb",
            "Unhealthy": "361-649 ppb",
            "Very Unhealthy": "650-1249 ppb",
            "Hazardous": "1250+ ppb",
        },
    },
    "Ozone": {
        "description": "Ground-level ozone is a secondary pollutant formed by chemical reactions in the atmosphere. While ozone in the stratosphere protects us from the sun's harmful rays, ground-level ozone can be harmful, leading to respiratory issues and poor air quality.",
        "air_quality_levels": {
            "Good": "0-54 ppb",
            "Moderate": "55-70 ppb",
            "Unhealthy for Sensitive Groups": "71-85 ppb",
            "Unhealthy": "86-105 ppb",
            "Very Unhealthy": "106-200 ppb",
            "Hazardous": "201+ ppb",
        },
    },
    "Particulate Matter (PM2.5)": {
        "description": "These are tiny particles suspended in the air and include dust, soot, and pollutants. PM10 and PM2.5 can be inhaled, leading to respiratory and cardiovascular issues. Monitoring their levels is crucial for assessing air quality.",
        "air_quality_levels": {
            "Good": "0-12 µg/m³",
            "Moderate": "13-35.4 µg/m³",
            "Unhealthy for Sensitive Groups": "35.5-55.4 µg/m³",
            "Unhealthy": "55.5-150.4 µg/m³",
            "Very Unhealthy": "150.5-250.4 µg/m³",
            "Hazardous": "250.5+ µg/m³",
        },
    },
    "Particulate Matter (PM10)": {
        "description": "These are tiny particles suspended in the air and include dust, soot, and pollutants. PM10 and PM2.5 can be inhaled, leading to respiratory and cardiovascular issues. Monitoring their levels is crucial for assessing air quality.",
        "air_quality_levels": {
            "Good": "0-54 µg/m³",
            "Moderate": "55-154 µg/m³",
            "Unhealthy for Sensitive Groups": "155-254 µg/m³",
            "Unhealthy": "255-354 µg/m³",
            "Very Unhealthy": "355-424 µg/m³",
            "Hazardous": "425+ µg/m³",
        },
    },
    "Lead": {
        "description": "Lead is a toxic heavy metal. Monitoring lead levels is essential as exposure can lead to severe health problems, particularly in children. Reducing lead emissions is a significant aspect of improving air quality."
    },
    "Barometric Pressure": {
        "description": "While not a pollutant, barometric pressure influences the dispersal and dilution of pollutants. Understanding its impact is essential for assessing how pollution accumulates in an area."
    },
    "Relative Humidity": {
        "description": "Humidity affects the concentration of airborne particles and gases. High humidity can contribute to the formation of aerosols and influence air quality conditions."
    },
    "Dew Point": {
        "description": "Dew point is the temperature at which air becomes saturated with moisture, leading to condensation. Understanding the dew point is essential for assessing the potential for fog and haze formation, which can impact visibility and air quality."
    },
    "Outdoor Temperature": {
        "description": "Temperature influences the rate of chemical reactions in the atmosphere, affecting the formation and dispersion of pollutants. Monitoring temperature is crucial for understanding air quality dynamics."
    },
    "Wind Direction and Speed": {
        "description": "Wind direction and speed are critical in dispersing pollutants and influencing local air quality. Understanding these factors is vital for assessing how pollutants are transported and distributed in an area."
    }
    # Add information for other parameters here
}

selected_param = st.selectbox("**Select a parameter to learn more about**", list(param_info.keys()))

if selected_param:
    param_description = param_info[selected_param]["description"]
    st.write(f"**About {selected_param}:**")
    st.write(param_description)
    if "air_quality_levels" in param_info[selected_param]:
        air_quality_levels = param_info[selected_param]["air_quality_levels"]
        st.write("**Air Quality Impact:**")
        table_content = "| Level | Range |\n|-------|-------|\n"
        for level, range in air_quality_levels.items():
            table_content += f"| {level} | {range} |\n"
        st.markdown(table_content)

st.write(
    """
   
    """
    )
st.subheader("About the dataset")
st.write(
    """
    The [EPA Air Quality Dataset](https://www.epa.gov/outdoor-air-quality-data) is a valuable resource provided by the United States Environmental Protection Agency (EPA) that offers a comprehensive and detailed record of air quality measurements across the United States.
    With a wide range of spatial and temporal granularity, the EPA's air quality dataset allows us to track air quality levels over time and across different locations, helping us understand the impact of air pollution on public health and the environment.
    Whether you're interested in studying long-term trends, assessing the effectiveness of air quality regulations, or simply gaining insights into local air quality, this dataset is an essential tool for making informed decisions and taking action to protect the air we breathe.
    
    """
    )


with open("geojson/USA_state.geojson", "r") as geojson_file:
    geojson_data = json.load(geojson_file)

st.session_state.geojson_data = geojson_data

mapbox_layout = {
    "style": "carto-positron",
    "center": {"lat": 38.0902, "lon": -95.7129},
    "zoom": 2.6,
    
}

st.session_state.mapbox_layout = mapbox_layout
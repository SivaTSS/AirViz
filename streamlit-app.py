import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
import plotly.graph_objects as go
import hiplot as hip
st.set_page_config(layout="wide")
@st.cache_data
def load_data(filepath):
    if "parquet" in filepath:
        data = pd.read_parquet(filepath)
    elif "csv" in filepath:   
        data = pd.read_csv(filepath)
    else:
        raise Exception("file format not supported")
    return data

st.sidebar.header("EDA Options")

df = load_data("dataset/refined/annual_conc_by_monitor.parquet")
df_aqi = load_data("dataset/refined/annual_aqi_by_county.csv")

# df.dropna()

st.title("AirViz")
st.write("""
The goal of this webapp is to help users understand more about the air we breath.

         
""")

st.header("Importance")

st.write("""
Air quality is a critical aspect of our environment that directly impacts the health and 
well-being of individuals and the ecosystems we inhabit. It refers to the measurement of 
various pollutants and particulate matter in the atmosphere, which can have adverse effects 
on human health and the environment.

""")
params=['Carbon monoxide', 'Sulfur dioxide', 'Nitrogen dioxide (NO2)', 'Ozone', 'PM10 Total 0-10um STP',\
        'PM10-2.5 - Local Conditions', 'PM2.5 - Local Conditions', 'Acceptable PM2.5 AQI & Speciation Mass',\
        'Lead (TSP) STP', 'Barometric pressure', 'Relative Humidity ',\
        'Dew Point', 'Outdoor Temperature', 'Wind Direction - Resultant', 'Wind Speed - Resultant']

param_info = {
    'Carbon monoxide': {
        'description': "Carbon monoxide is a colorless, odorless gas produced by incomplete combustion of carbon-containing fuels. High levels of CO can be harmful, affecting air quality and human health. Monitoring CO is vital because it can lead to respiratory problems and, at elevated concentrations, pose a risk to life.",
        'air_quality_levels': {
                'Good': '0-4.4 ppm',
                'Moderate': '4.5-9.4 ppm',
                'Unhealthy for Sensitive Groups': '9.5-12.4 ppm',
                'Unhealthy': '12.5-15.4 ppm',
                'Very Unhealthy': '15.5-30.4 ppm',
                'Hazardous': '30.5+ ppm'
            }
    },
    'Sulfur dioxide': {
        'description': "Sulfur dioxide is a pungent gas emitted from sources like power plants and industrial processes. It can contribute to poor air quality, cause respiratory issues, and lead to the formation of acid rain, harming both human health and the environment."
        ,'air_quality_levels': {
                'Good': '0-35 ppb',
                'Moderate': '36-75 ppb',
                'Unhealthy for Sensitive Groups': '76-185 ppb',
                'Unhealthy': '186-304 ppb',
                'Very Unhealthy': '305-604 ppb',
                'Hazardous': '605+ ppb'
            }
    },
    'Nitrogen dioxide (NO2)':{
        'description': "Nitrogen dioxide is a reddish-brown gas, often associated with vehicle emissions. High levels of NO2 are harmful to respiratory health and can contribute to the formation of ground-level ozone and fine particulate matter, impacting air quality."
        ,'air_quality_levels': {
                'Good': '0-53 ppb',
                'Moderate': '54-100 ppb',
                'Unhealthy for Sensitive Groups': '101-360 ppb',
                'Unhealthy': '361-649 ppb',
                'Very Unhealthy': '650-1249 ppb',
                'Hazardous': '1250+ ppb'
            }    },
    'Ozone':{
        'description': "Ground-level ozone is a secondary pollutant formed by chemical reactions in the atmosphere. While ozone in the stratosphere protects us from the sun's harmful rays, ground-level ozone can be harmful, leading to respiratory issues and poor air quality."
        ,'air_quality_levels': {
                'Good': '0-54 ppb',
                'Moderate': '55-70 ppb',
                'Unhealthy for Sensitive Groups': '71-85 ppb',
                'Unhealthy': '86-105 ppb',
                'Very Unhealthy': '106-200 ppb',
                'Hazardous': '201+ ppb'
            }    },
    'Particulate Matter (PM2.5)':{
        'description': "These are tiny particles suspended in the air and include dust, soot, and pollutants. PM10 and PM2.5 can be inhaled, leading to respiratory and cardiovascular issues. Monitoring their levels is crucial for assessing air quality."
        ,'air_quality_levels': {
                'Good': '0-12 µg/m³',
                'Moderate': '13-35.4 µg/m³',
                'Unhealthy for Sensitive Groups': '35.5-55.4 µg/m³',
                'Unhealthy': '55.5-150.4 µg/m³',
                'Very Unhealthy': '150.5-250.4 µg/m³',
                'Hazardous': '250.5+ µg/m³'
            }    },
    'Particulate Matter (PM10)':{
        'description': "These are tiny particles suspended in the air and include dust, soot, and pollutants. PM10 and PM2.5 can be inhaled, leading to respiratory and cardiovascular issues. Monitoring their levels is crucial for assessing air quality."
        ,'air_quality_levels': {
                'Good': '0-54 µg/m³',
                'Moderate': '55-154 µg/m³',
                'Unhealthy for Sensitive Groups': '155-254 µg/m³',
                'Unhealthy': '255-354 µg/m³',
                'Very Unhealthy': '355-424 µg/m³',
                'Hazardous': '425+ µg/m³'
            }    },
    'Lead':{
        'description': "Lead is a toxic heavy metal. Monitoring lead levels is essential as exposure can lead to severe health problems, particularly in children. Reducing lead emissions is a significant aspect of improving air quality."
    },
    'Barometric Pressure':{
        'description': "While not a pollutant, barometric pressure influences the dispersal and dilution of pollutants. Understanding its impact is essential for assessing how pollution accumulates in an area."
    },
    'Relative Humidity':{
        'description': "Humidity affects the concentration of airborne particles and gases. High humidity can contribute to the formation of aerosols and influence air quality conditions."
    },
    'Dew Point':{
        'description': "Dew point is the temperature at which air becomes saturated with moisture, leading to condensation. Understanding the dew point is essential for assessing the potential for fog and haze formation, which can impact visibility and air quality."
    },
    'Outdoor Temperature':{
        'description': "Temperature influences the rate of chemical reactions in the atmosphere, affecting the formation and dispersion of pollutants. Monitoring temperature is crucial for understanding air quality dynamics."
    },
    'Wind Direction and Speed':{
        'description': "Wind direction and speed are critical in dispersing pollutants and influencing local air quality. Understanding these factors is vital for assessing how pollutants are transported and distributed in an area."
    }
    # Add information for other parameters here

}
# Create a dropdown to select a parameter
selected_param = st.selectbox("Select a parameter to learn more about", list(param_info.keys()))

if selected_param:
    param_description = param_info[selected_param]['description']
    st.write(f"**About {selected_param}:**")
    st.write(param_description)
    if 'air_quality_levels' in param_info[selected_param]:
        air_quality_levels = param_info[selected_param]['air_quality_levels']
        st.write("**Air Quality Impact:**")
        for level, range in air_quality_levels.items():
            st.write(f"- {level}: {range}")


year = st.sidebar.slider("Select a year", min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), value=2021)
parameters = st.sidebar.selectbox("Select the Parameter to visualize ", params)


with open('geojson/USA_state.geojson', 'r') as geojson_file:
    geojson_data = json.load(geojson_file)

import streamlit as st

region_level = st.radio("Select region level", ["State", "County"])
tab1, tab2= st.tabs(["Concentration", "Coverage"])

with tab1:
    st.header("Statewise- Concentration of Ozone")
    col="Arithmetic Mean" 
    custom_agg= lambda x: x.max()
    fig = px.choropleth_mapbox(
        df.loc[(df["Year"]==year) & (df["Parameter Name"]=="Ozone")].groupby("State Name")[col].agg(**{col: custom_agg}).reset_index(),
        geojson=geojson_data,
        locations='State Name',
        featureidkey="properties.shapeName",  
        color=col,
        color_continuous_scale='magma',  
        mapbox_style="carto-positron",
        center={"lat": 37.0902, "lon": -95.7129},
        zoom=3,
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Coverage")
    
    fig = px.scatter_mapbox(
        df.loc[df["Year"]==year],
        lat="Latitude",
        lon="Longitude",
        zoom=3,
        opacity=0.6,
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        title="Coverage of centers",
    )
    st.plotly_chart(fig, use_container_width=True)




st.header("Pollutant Trends")

fig = go.Figure()
param="Ozone"
aggregation = {
        f'Arithmetic Mean': 'mean',
        f'Arithmetic Standard Dev' : 'mean',
        f'1st Max Value': 'max',
    }
country_df = df[(df["Parameter Name"]==param) & (df["Sample Duration"]=="1 HOUR")].groupby(['Year']).agg(aggregation).reset_index()

# Add the shaded area for mean ± std
fig.add_trace(go.Scatter(
    x=country_df['Year'],  # Assuming the index represents your x-axis values
    y=country_df['Arithmetic Mean'] - country_df['Arithmetic Standard Dev'],
    fill=None,
    line=dict(color='rgba(0,100,80,0)'),
    name='Mean ± Std',
))

fig.add_trace(go.Scatter(
    x=country_df['Year'],
    y=country_df['Arithmetic Mean'] + country_df['Arithmetic Standard Dev'],
    fill='tonexty',  # Fills the area to the line below
    fillcolor='rgba(0,100,80,0.2)',  # Color and opacity of the shaded area
    line=dict(color='rgba(0,100,80,0)'),
    name='Mean ± Std',
))

# Add the mean line
fig.add_trace(go.Scatter(
    x=country_df['Year'],
    y=country_df['Arithmetic Mean'],
    mode='lines+markers',
    line=dict(color='rgb(0,100,80)'),
    name='Mean',
))

# # Add the max line
# fig.add_trace(go.Scatter(
#     x=country_df['Year'],
#     y=country_df[f'1st Max Value'],
#     mode='lines+markers',
#     line=dict(color='rgb(200,0,0)'),
#     name='Max',
# ))

# Customize the layout
fig.update_layout(
    title='Mean, Std, and Max',
    xaxis_title='X-axis',
    yaxis_title='Y-axis',
)

# Show the plot
st.plotly_chart(fig, use_container_width=True)


st.header("Compare air quality with standard(radar plot)")


st.header("AQI")
st.write("""
The AQI is determined using data on the following pollutants:

Particulate Matter (PM2.5 and PM10): These are tiny particles in the air that can be inhaled into the lungs and cause respiratory problems.

Ground-level Ozone (O3): Ozone is a harmful gas that can irritate the respiratory system and cause other health issues.

Nitrogen Dioxide (NO2): A gas that can irritate the respiratory system and contribute to the formation of ground-level ozone.

Sulfur Dioxide (SO2): A gas that can irritate the respiratory system and contribute to the formation of fine particles.

Carbon Monoxide (CO): A colorless, odorless gas that can be harmful when inhaled in large amounts.

The AQI is calculated for each of these pollutants separately, and the highest of these individual AQI values is used to represent the overall air quality for a specific location. 
""")

with st.expander("Expore data using parallel coords"):
    st.write("This content is hidden by default but can be expanded.")
    st.header("Parallel coords")
    exp = hip.Experiment.from_dataframe(df_aqi)

    def save_hiplot_to_html(exp):
        output_file = "hiplot_plot_1.html"
        exp.to_html(output_file)
        return output_file

    hiplot_html_file = save_hiplot_to_html(exp)
    st.components.v1.html(
        open(hiplot_html_file, 'r').read(), height=1500, scrolling=True)
    
st.header("AQI plot")


aqi_tab1, aqi_tab2= st.tabs(["Radio", "Heatmap"])

with aqi_tab1:
    # Sample data for air quality metrics (replace with your actual data)
    set1 = ['Days with AQI', 'Good Days', 'Moderate Days', 'Unhealthy for Sensitive Groups Days',
        'Unhealthy Days', 'Very Unhealthy Days', 'Hazardous Days']
    set2 = ['Days CO', 'Days NO2', 'Days Ozone', 'Days PM2.5', 'Days PM10']

    # Assuming you have a DataFrame df_aqi containing your data
    county_data = df_aqi[(df_aqi['State'] == "Alabama") & (df_aqi['County'] == "Autauga") & (df_aqi['Year'] == 1990)]
    yearly_avg = df_aqi.groupby('Year')[set1+set2].mean().reset_index()

    # Create the radar chart using Plotly Express for 'set1'
    fig_set1 = px.line_polar(county_data, r=county_data[set1].values[0], theta=set1, line_close=True)
    fig_set1.update_traces(fill='toself')
    yearly_avg_trace_set1 = px.line_polar(yearly_avg, r=yearly_avg[set1].values[0], theta=set1, line_close=True)
    yearly_avg_trace_set1.update_traces(line=dict(color="red"))
    yearly_avg_trace_set1.data[0].name = "Yearly Average (set1)"

    # Create the radar chart using Plotly Express for 'set2'
    fig_set2 = px.line_polar(county_data, r=county_data[set2].values[0], theta=set2, line_close=True)
    fig_set2.update_traces(fill='toself')
    yearly_avg_trace_set2 = px.line_polar(yearly_avg, r=yearly_avg[set2].values[0], theta=set2, line_close=True)
    yearly_avg_trace_set2.update_traces(line=dict(color="green"))
    yearly_avg_trace_set2.data[0].name = "Yearly Average (set2)"

    # Create subplots
    from plotly.subplots import make_subplots

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Metrics (set1)", "Metrics (set2)"), specs=[[{'type': 'polar'}, {'type': 'polar'}]])
    fig.add_trace(fig_set1.data[0], row=1, col=1)
    fig.add_trace(fig_set2.data[0], row=1, col=2)
    fig.add_trace(yearly_avg_trace_set1.data[0], row=1, col=1)
    fig.add_trace(yearly_avg_trace_set2.data[0], row=1, col=2)

    # Set the chart title
    county_name = "Autauga, Alabama"  # You can use this name or customize it as needed
    fig.update_layout(title=f'Air Quality Metrics Comparison for {county_name} in 1990')

    # Show the chart
    st.plotly_chart(fig, use_container_width=True)

with aqi_tab2:
    col="Good Days" 
    with open('geojson/USA_state.geojson', 'r') as geojson_file:
        geojson_data = json.load(geojson_file)
    custom_agg= lambda x: x.max()
    fig = px.choropleth_mapbox(
        df_aqi.loc[df_aqi["Year"]==year].groupby("State")[col].agg(**{col: custom_agg}).reset_index(),
        geojson=geojson_data,
        locations='State',
        featureidkey="properties.shapeName",  
        color=col,
        color_continuous_scale='magma',  
        mapbox_style="carto-positron",
        center={"lat": 37.0902, "lon": -95.7129},
        zoom=3,
    )
    st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
import plotly.graph_objects as go
import hiplot as hip
import utils
from streamlit_extras.app_logo import add_logo

add_logo("airviz_image.png", height=30)
utils.add_navigation()

def aqi_intro():
    st.header("Air Quality Index(AQI)")
    st.subheader("How is AQI Calculated?")
    st.write(
        """
    The AQI is determined using data on the following pollutants:

    - **Particulate Matter (PM2.5 and PM10)**: These are tiny particles in the air that can be inhaled into the lungs and cause respiratory problems.
    - **Ground-level Ozone (O3)**: Ozone is a harmful gas that can irritate the respiratory system and cause other health issues.
    - **Nitrogen Dioxide (NO2)**: A gas that can irritate the respiratory system and contribute to the formation of ground-level ozone.
    - **Sulfur Dioxide (SO2)**: A gas that can irritate the respiratory system and contribute to the formation of fine particles.
    - **Carbon Monoxide (CO)**: A colorless, odorless gas that can be harmful when inhaled in large amounts.

    The AQI is calculated for each of these pollutants separately, and the highest of these individual AQI values is used to represent the overall air quality for a specific location. 
    """
    )

    st.subheader("Air Quality Index (AQI) Categories")

    st.write(
        """
    - **Good (0-50):** Air quality is satisfactory, posing little or no risk to health.
    - **Moderate (51-100):** Air quality is acceptable; however, some pollutants may be a concern for a very small number of individuals who are unusually sensitive to air pollution.
    - **Unhealthy for Sensitive Groups (101-150):** Members of sensitive groups, such as children, the elderly, and individuals with respiratory or heart conditions, may experience health effects. The general public is not likely to be affected.
    - **Unhealthy (151-200):** Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.
    - **Very Unhealthy (201-300):** Health alert: everyone may experience more serious health effects.
    - **Hazardous (301-500):** Health warnings of emergency conditions; the entire population is likely to be affected.

    """)
    return

def plot_parallel_coords(df_aqi):
    with st.expander("**Expore data using parallel coords**"):
        st.write("This content is hidden by default but can be expanded.")
        st.header("Parallel coords")
        exp = hip.Experiment.from_dataframe(df_aqi)

        def save_hiplot_to_html(exp):
            output_file = "hiplot_plot_1.html"
            exp.to_html(output_file)
            return output_file

        hiplot_html_file = save_hiplot_to_html(exp)
        st.components.v1.html(open(hiplot_html_file, "r").read(), height=1500, scrolling=True)

def plot_airquality_lineplot(df_aqi):
    with st.expander("Choose attibute to plot"):
        aqi_measurement_type = st.radio(
                "Select from below",
                [
                    "Days with AQI",
                    "Good Days",
                    "Moderate Days",
                    "Unhealthy for Sensitive Groups Days",
                    "Unhealthy Days",
                    "Very Unhealthy Days",
                    "Hazardous Days",
                    "Max AQI",
                    "90th Percentile AQI",
                    "Median AQI",
                    "Days CO",
                    "Days NO2",
                    "Days Ozone",
                    "Days PM2.5",
                    "Days PM10",
                ],
                index=8, key="aqi_mes1"
            )
    fig = go.Figure()
    custom_arg = {aqi_measurement_type: lambda x: x.mean()}
    comb_df = df_aqi.groupby("Year").agg(custom_arg).reset_index()

    fig.add_trace(
        go.Scatter(
            x=comb_df["Year"],
            y=comb_df[aqi_measurement_type],
            mode="lines+markers",
            line=dict(color="rgb(200,0,0)")
        )
    )
    fig.update_layout(
        title=f"{aqi_measurement_type} - Yearly trends(1980-2022)",
        title_font=dict(size=20),
        margin=dict(b=10),
        xaxis_title="Years",
        yaxis_title=aqi_measurement_type,
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_airquality_radioplot(df_aqi):
    col1, col2 = st.columns([3, 6])
    with col1:
        selected_fields = st.multiselect(
            "Select fields to plot:",
            [
                "Days with AQI",
                "Good Days",
                "Moderate Days",
                "Unhealthy for Sensitive Groups Days",
                "Unhealthy Days",
                "Very Unhealthy Days",
                "Hazardous Days",
                "Max AQI",
                "90th Percentile AQI",
                "Median AQI",
            ],
            default=["Days with AQI", "Good Days", "Moderate Days", "Max AQI", "90th Percentile AQI", "Median AQI"],
        )
        state_list = df_aqi["State"].unique().tolist() + ["All"]
        selected_state = st.selectbox("Select State", state_list, index=1, key="state2")
        county_list = df_aqi[df_aqi["State"] == selected_state]["County"].unique().tolist() + ["All"]
        selected_county = st.selectbox("Select County", county_list, index=1, key="county2")
    with col2:
        year = st.slider("Select a year", min_value=int(df_aqi["Year"].min()), max_value=int(df_aqi["Year"].max()), value=2020)
        year_df = df_aqi[df_aqi["Year"] == year]
        if selected_state == "All":
            filtered_df = year_df.groupby("Year")[selected_fields].mean().reset_index()
        elif selected_county == "All":
            state_df = year_df[year_df["State"] == selected_state]
            filtered_df = state_df.groupby("Year")[selected_fields].mean().reset_index()
        else:
            state_df = year_df[year_df["State"] == selected_state]
            county_df = state_df[state_df["County"] == selected_county]
            filtered_df = county_df.groupby("Year")[selected_fields].mean().reset_index()

        yearly_avg = year_df.groupby("Year")[selected_fields].mean().reset_index()
        fig = px.line_polar(yearly_avg, r=yearly_avg[selected_fields].values[0], theta=selected_fields, line_close=True)
        fig.update_traces(fill="toself", line=dict(color="green"))
        fig2 = px.line_polar(
            filtered_df, r=filtered_df[selected_fields].values[0], theta=selected_fields, line_close=True
        )
        fig2.update_traces(fill="toself")
        fig.add_traces(fig2.data)

        if selected_state == "All":
            fig.update_layout(title=f"Air Quality Metrics for USA - {year}")
        elif selected_county == "All":
            fig.update_layout(title=f"Air Quality Metrics for {selected_state} - {year}")
        else:
            fig.update_layout(title=f"Air Quality Metrics for {selected_county} - {year}")
        st.plotly_chart(fig, use_container_width=True)

def plot_airquality_heatmap(df_aqi,config):
    
    year = st.slider("Select a year", min_value=int(df_aqi["Year"].min()), max_value=int(df_aqi["Year"].max()), value=2020, key="year2")
    with st.expander("Choose attibute to plot"):
        aqi_measurement_type2 = st.radio(
            "Select from below",
            [
                "Days with AQI",
                "Good Days",
                "Moderate Days",
                "Unhealthy for Sensitive Groups Days",
                "Unhealthy Days",
                "Very Unhealthy Days",
                "Hazardous Days",
                "Max AQI",
                "90th Percentile AQI",
                "Median AQI",
                "Days CO",
                "Days NO2",
                "Days Ozone",
                "Days PM2.5",
                "Days PM10",
            ],
            index=8, key="aqi_mes2"
        )

    custom_agg2 = lambda x: x.max()
    fig = px.choropleth_mapbox(
        df_aqi.groupby("State")[aqi_measurement_type2].agg(**{aqi_measurement_type2: custom_agg2}).reset_index(),
        geojson=config["geojson_data"],
        locations="State",
        featureidkey="properties.shapeName",
        color=aqi_measurement_type2,
        color_continuous_scale="magma",
    )
    fig.update_layout(
        title=f"{aqi_measurement_type2} - {year}",
        title_font=dict(size=20),
        mapbox=config["mapbox_layout"]
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_airquality_metrics(df_aqi,config):
    st.header("Air Quality Metric plots")
    aqi_tab1, aqi_tab2, aqi_tab3 = st.tabs(["Line Plot","Radio", "Heatmap"])

    with aqi_tab1:
        plot_airquality_lineplot(df_aqi)
    with aqi_tab2:
        plot_airquality_radioplot(df_aqi)
    with aqi_tab3:
        plot_airquality_heatmap(df_aqi,config)

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
config={
    "params":params,
    "geojson_data":geojson_data,
    "mapbox_layout":mapbox_layout
}

aqi_intro()
plot_parallel_coords(df_aqi)
plot_airquality_metrics(df_aqi,config)
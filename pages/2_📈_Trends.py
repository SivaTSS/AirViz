import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
import plotly.graph_objects as go
import hiplot as hip


def plot_geospacial_trend_concentration(filtered_df, year, parameter, config):
    col = "Arithmetic Mean"
    custom_agg = lambda x: x.max()
    fig = px.choropleth_mapbox(
        filtered_df.groupby("State Name")[col].agg(**{col: custom_agg}).reset_index(),
        geojson=config["geojson_data"],
        locations="State Name",
        featureidkey="properties.shapeName",
        color=col,
        color_continuous_scale="magma",
    )
    fig.update_layout(
        title=f"Concentration of {parameter} - {year}",
        title_font=dict(size=20),
        margin=dict(b=10),
        mapbox=config["mapbox_layout"],
    )
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        """
    A pronounced trend is evident in the case of several pollutants, including Ozone and NO2, with consistently higher levels observed along the western coast, particularly in California's southern regions.

            
    """
    )

def plot_geospacial_trend_coverage(filtered_df, year, parameter, config):
    fig = px.scatter_mapbox(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
    )
    fig.update_layout(
        title=f"Coverage of centers - {year}",
        title_font=dict(size=20),
        margin=dict(b=10),
        mapbox=config["mapbox_layout"],
    )
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        """
    Adequate coverage of Air Quality measurement centers is of paramount importance as it provides the data needed to monitor and address regional variations in air quality, safeguard public health, protect the environment, inform policy and regulation and establish early warning systems. It also helps in raising public awareness, and facilitates international cooperation in addressing the global challenge of air pollution. Coverage patterns mirror population trends, with a notable concentration along the eastern and western coasts and sparse availability elsewhere, apart from a few isolated hotspots.

            
    """
    )

def plot_geospacial_trends(df, parameter, config):
    st.header("Pollutant Trends")
    st.subheader("Geospacial Trends")
    year = st.slider("Select a year", min_value=int(df["Year"].min()), max_value=int(df["Year"].max()), value=2020)
    filtered_df = df.loc[(df["Year"] == year) & (df["Parameter Name"] == parameter)]
    tab1, tab2 = st.tabs(["Concentration", "Coverage"])
    with tab1:
        plot_geospacial_trend_concentration(filtered_df, year, parameter, config)
    with tab2:
        plot_geospacial_trend_coverage(filtered_df, year, parameter, config)   

def get_temporal_trends_inputs(df):
    col1, col2 = st.columns([6, 4])
    show_lines={}
    with col1:
        year_range = st.slider(
            "Select Year Range", min_value=min(df["Year"]), max_value=max(df["Year"]), value=(1980, max(df["Year"]))
        )
        col3, col4 = st.columns(2)
        with col3:
            with st.expander("Show/Hide Lines"):
                show_lines["Max"] = st.checkbox("Max", value=False)
                show_lines["Mean"] = st.checkbox("Mean", value=True)
                show_lines["Std"] = st.checkbox("Std", value=True)
        with col4:
            with st.expander("Measurement Type"):
                measurement_type = st.radio("Select from below", df[df["Parameter Name"] == parameter]["Sample Duration"].unique())
    with col2:
        state_list = df["State Name"].unique().tolist() + ["All"]
        selected_state = st.selectbox("Select State", state_list, index=4)
        county_list = df[df["State Name"] == selected_state]["County Name"].unique().tolist() + ["All"]
        selected_county = st.selectbox("Select County", county_list, index=len(county_list)-1)
    return show_lines,year_range,measurement_type,selected_state,selected_county

def get_temporal_trends_filtered_df(df,year_range,measurement_type,selected_state,selected_county):
    aggregation = {
        f"Arithmetic Mean": "mean",
        f"Arithmetic Standard Dev": "mean",
        f"1st Max Value": "max",
    }
    p_df = df[df["Parameter Name"] == parameter]
    year_df = p_df[(p_df["Year"] >= year_range[0]) & (p_df["Year"] <= year_range[1])]
    if selected_state == "All":
        filtered_df = (
            year_df[(year_df["Sample Duration"] == measurement_type)].groupby(["Year"]).agg(aggregation).reset_index()
        )
    elif selected_county == "All":
        state_df = year_df[year_df["State Name"] == selected_state]
        filtered_df = (
            state_df[(state_df["Sample Duration"] == measurement_type)].groupby(["Year"]).agg(aggregation).reset_index()
        )
    else:
        state_df = year_df[year_df["State Name"] == selected_state]
        county_df = state_df[state_df["County Name"] == selected_county]
        filtered_df = (
            county_df[(county_df["Sample Duration"] == measurement_type)].groupby(["Year"]).agg(aggregation).reset_index()
        )
    return filtered_df

def plot_temporal_trends(df, parameter): 
    st.subheader("Temporal Trends")
    show_lines,year_range,measurement_type,selected_state,selected_county=get_temporal_trends_inputs(df)
    filtered_df=get_temporal_trends_filtered_df(df,year_range,measurement_type,selected_state,selected_county)

    fig = go.Figure()
    if show_lines["Std"]:
        fig.add_trace(
            go.Scatter(
                x=filtered_df["Year"],
                y=filtered_df["Arithmetic Mean"] - filtered_df["Arithmetic Standard Dev"],
                fill=None,
                line=dict(color="rgba(0,100,80,0)"),
                name="",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=filtered_df["Year"],
                y=filtered_df["Arithmetic Mean"] + filtered_df["Arithmetic Standard Dev"],
                fill="tonexty",
                fillcolor="rgba(0,100,80,0.2)",
                line=dict(color="rgba(0,100,80,0)"),
                name="Mean ± Std",
            )
        )

    if show_lines["Mean"]:
        fig.add_trace(
            go.Scatter(
                x=filtered_df["Year"],
                y=filtered_df["Arithmetic Mean"],
                mode="lines+markers",
                line=dict(color="rgb(0,100,80)"),
                name="Mean",
            )
        )

    if show_lines["Max"]:
        fig.add_trace(
            go.Scatter(
                x=filtered_df["Year"],
                y=filtered_df[f"1st Max Value"],
                mode="lines+markers",
                line=dict(color="rgb(200,0,0)"),
                name="Max",
            )
        )

    fig.update_layout(
        title=f"{parameter} - Yearly trends({year_range[0]}-{year_range[1]})",
        title_font=dict(size=20),
        margin=dict(b=10),
        xaxis_title="Years",
        yaxis_title="Concentration",
    )

    st.plotly_chart(fig, use_container_width=True)
    st.write(
            """
        A conspicuous trend is discernible in the case of several pollutants: a consistent reduction over the years. This decrease can be attributed to a combination of factors, including stricter environmental regulations, technological advancements in emission controls, and heightened public awareness regarding the detrimental effects of pollution.
                
        """
        )
    


df = st.session_state.df
params= st.session_state.params
geojson_data= st.session_state.geojson_data
mapbox_layout = st.session_state.mapbox_layout


parameter = st.sidebar.selectbox("Select the Parameter to visualize ", params, index=params.index("Ozone"))

config={
    "params":params,
    "geojson_data":geojson_data,
    "mapbox_layout":mapbox_layout
}
    
plot_geospacial_trends(df, parameter, config)
    
plot_temporal_trends(df, parameter)



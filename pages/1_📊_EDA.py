import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
import plotly.graph_objects as go
import hiplot as hip
import utils
import numpy as np
from streamlit_extras.app_logo import add_logo
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

add_logo("airviz_image.png", height=30)
utils.add_navigation()


def conc_dataset_description():
    st.write(
        """
    #### Description ####

    The "annual_conc_by_monitor" dataset from the EPA offers an extensive and detailed record of annual air quality measurements captured by monitoring stations located throughout the United States.

    """
    )

    column_explanations = {
        "State Code": "A numerical code representing the state where the monitoring site is located.",
        "County Code": "A numerical code representing the county where the monitoring site is situated.",
        "Site Num": "A unique identifier for the monitoring site.",
        "Parameter Code": "A numerical code representing the specific pollutant being measured",
        "Latitude": "The geographical latitude coordinates of the monitoring site.",
        "Longitude": "The geographical longitude coordinates of the monitoring site.",
        "Parameter Name": "The name of the measured parameter",
        "Sample Duration": "The duration of the sample collection",
        "Pollutant Standard": "The air quality standard for the pollutant being monitored.",
        "Method Name": "The method used for monitoring.",
        "Year": "The year in which the data was collected.",
        "Units of Measure": "The unit of measurement for the pollutant concentration (e.g., 'Parts per billion').",
        "Observation Count": "The total count of observations from the monitor.",
        "Observation Percent": "The percentage of observations available from the monitor.",
        "Arithmetic Mean": "The average concentration measured at the monitoring site.",
        "Arithmetic Standard Dev": "The standard deviation of the measured concentrations.",
        "1st Max Value": "The highest observed concentration within the dataset.",
        "99th Percentile": "The concentration value below which 99% of the data falls.",
        "98th Percentile": "The concentration value below which 98% of the data falls.",
        "95th Percentile": "The concentration value below which 95% of the data falls.",
        "90th Percentile": "The concentration value below which 90% of the data falls.",
        "75th Percentile": "The concentration value below which 75% of the data falls.",
        "50th Percentile": "The median concentration, representing the value below which 50% of the data falls.",
        "10th Percentile": "The concentration value below which 10% of the data falls.",
        "State Name": "The name of the state where the monitoring site is located.",
        "County Name": "The name of the county where the monitoring site is situated.",
    }

    selected_column = st.selectbox("**Select a column to learn more about**", list(column_explanations.keys()))
    if selected_column:
        st.write(column_explanations[selected_column])


def conc_dataset_plot_corr_heatmap(df, numerical_columns):
    fig, ax = plt.subplots()
    ax = sns.heatmap(df[numerical_columns].corr(), cmap="coolwarm")
    st.pyplot(fig)
    st.write(
        """
    There is a strong correlation between arithmetic mean and percentiles as expected. There is not much correlation between other columns.

    """
    )


def conc_dataset_plot_missing_values(df, params):
    col1, col2 = st.columns(2)
    with col1:
        parameter = st.selectbox("Select the Parameter to visualize ", params, index=params.index("Ozone"))
    with col2:
        state_list = df["State Name"].unique().tolist() + ["All"]
        selected_state = st.selectbox("Select State", state_list, index=4)

    filtered_df = df[(df["Parameter Name"] == parameter) & (df["State Name"] == selected_state)]

    if filtered_df is not None and not filtered_df.empty:
        fig, ax = plt.subplots()
        ax = sns.heatmap(filtered_df.isnull().T, cbar=True, cmap="flare", xticklabels=False, yticklabels=True)

        ax.set_xlabel("Data Points")
        ax.set_title(f"Missing Values Heatmap for {parameter} in {selected_state}")
        cbar = ax.collections[0].colorbar
        cbar.set_ticks([0, 1])
        cbar.set_ticklabels(["Not Missing", "Missing"])
        st.pyplot(fig)
    else:
        st.write(
            """
        *There are no data points for this selection. Please choose other States/Parameters.*

        """
        )

    st.write(
        """
    There are missing values in the columns Pollutant Standard and Method Name. Both the columns have been ignored in further analysis. There are no missing values in other columns. It should also be noted that pollutant standard is not applicable for all Parameters(Ex: Wind Speed, Pressure). 

    """
    )


def conc_dataset_plot_yearly_coverage(df, params):
    col3, col4 = st.columns(2)
    with col3:
        parameter = st.selectbox(
            "Select the Parameter to visualize ", params, index=params.index("Ozone"), key="tab_conc4"
        )
    with col4:
        columns = [
            "Observation Count",
            "Observation Percent",
            "Arithmetic Mean",
            "Arithmetic Standard Dev",
            "1st Max Value",
            "99th Percentile",
            "98th Percentile",
            "95th Percentile",
            "90th Percentile",
            "75th Percentile",
            "50th Percentile",
            "10th Percentile",
        ]
        numerical_column = st.selectbox("Select a column:", columns, index=8, key="tab_conc4_col4")

    filtered_df = df[(df["Parameter Name"] == parameter)]
    if filtered_df is not None and not filtered_df.empty:
        fig, ax = plt.subplots()
        ax = sns.histplot(filtered_df[numerical_column], bins=20, kde=True, color="skyblue")
        ax.lines[0].set_color("violet")
        ax.set_xlabel(f"{numerical_column} Values")
        ax.set_ylabel("Frequency")
        ax.set_title(f"Histogram of {numerical_column} for {parameter}")

        ax.grid(True, linestyle="--", alpha=0.3)
        st.pyplot(fig)
    else:
        st.write(
            """
        *There are no data points for this selection. Please choose other Parameters.*

        """
        )

    st.write(
        """
    We can analyse how are values of a specific parameter is distributed from the above plot.

    """
    )


def conc_dataset_plot_statewise_coverage(df, params):
    col5, col6 = st.columns(2)
    with col5:
        parameter = st.selectbox(
            "Select the Parameter to visualize ", params, index=params.index("Ozone"), key="tab_conc5"
        )
    with col6:
        columns = [
            "Observation Count",
            "Observation Percent",
            "Arithmetic Mean",
            "Arithmetic Standard Dev",
            "1st Max Value",
            "99th Percentile",
            "98th Percentile",
            "95th Percentile",
            "90th Percentile",
            "75th Percentile",
            "50th Percentile",
            "10th Percentile",
        ]
        numerical_column = st.selectbox("Select a column:", columns, index=8, key="tab_conc4_col5")

    filtered_df = df[(df["Parameter Name"] == parameter)]
    if filtered_df is not None and not filtered_df.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        ax = sns.set_style("whitegrid")
        ax = sns.boxplot(
            data=filtered_df,
            x=numerical_column,
            y="State Name",
            linewidth=0,
            flierprops={"markersize": 1},
            palette="rocket",
        )
        ax.set_xlabel(f"{numerical_column} Values")
        ax.set_ylabel("State Name")
        ax.set_title(f"Boxplot of {numerical_column} by State for {parameter}")
        ax.tick_params(axis="y", labelsize=8)
        st.pyplot(fig)
    else:
        st.write(
            """
        *There are no data points for this selection. Please choose other Parameters.*

        """
        )
    st.write(
        """
    We can analyse how are values of a specific parameter changes with respect to state from the above plot.
    It can be observed that for Ozone the values are higher for higly populated states in the east coast... escpecially California.


    """
    )
    plt.close()
    plt.clf()
    sns.set(style="whitegrid")


def perform_eda_of_conc_dataset():
    conc_dataset_description()
    st.write(
        """
    #### Visualizations ####
    """
    )
    numerical_columns = list(df.select_dtypes(include=np.number).columns.values)
    tab_conc1, tab_conc2, tab_conc3, tab_conc4, tab_conc5 = st.tabs(
        ["Summary Statistics", "Correlation", "Missing Values", "Histogram", "State-wise"]
    )
    with tab_conc1:
        st.table(df.describe())

    with tab_conc2:
        conc_dataset_plot_corr_heatmap(df, numerical_columns)

    with tab_conc3:
        conc_dataset_plot_missing_values(df, params)

    with tab_conc4:
        conc_dataset_plot_yearly_coverage(df, params)

    with tab_conc5:
        conc_dataset_plot_statewise_coverage(df, params)


def aqi_dataset_description():
    st.write(
        """
    #### Description ####

    The "annual_aqi_by_county" dataset from the EPA offers an extensive and detailed record of countywise air quality index.

    """
    )
    column_explanations = {
        "State": "The specific state within the United States where the air quality data was recorded.",
        "County": "The county or local jurisdiction within the state where the air quality data was collected.",
        "Year": "The year for which the air quality measurements are reported, allowing for time-series analysis and trend identification.",
        "Days with AQI": "The number of days in a year for which an Air Quality Index value is available, indicating the frequency of air quality monitoring.",
        "Good Days": "The count of days within the year when air quality is categorized as 'Good' according to the AQI, indicating clean and healthy air conditions.",
        "Moderate Days": "The count of days categorized as 'Moderate' on the AQI scale, signifying air quality that may be acceptable but can have moderate health concerns for some people.",
        "Unhealthy for Sensitive Groups Days": "The number of days during which air quality is considered 'Unhealthy for Sensitive Groups' on the AQI scale, highlighting concerns for individuals with respiratory conditions or other sensitivities.",
        "Unhealthy Days": "The count of days with 'Unhealthy' air quality, indicating air pollution levels that may have adverse health effects on the general population.",
        "Very Unhealthy Days": "The number of days when air quality is categorized as 'Very Unhealthy' on the AQI scale, indicating a high risk to the general population's health.",
        "Hazardous Days": "The count of days with 'Hazardous' air quality, representing the most severe level of air pollution that poses significant health risks to all individuals.",
        "Max AQI": "The highest recorded AQI value within the year, indicating the peak level of air pollution experienced.",
        "90th Percentile AQI": "The AQI value that exceeds 90% of the daily AQI values for the year, providing a measure of air quality above which most days fall.",
        "Median AQI": "The median AQI value for the year, representing the middle point in the range of daily AQI values.",
        "Days CO": "The number of days with carbon monoxide (CO) as a primary pollutant contributing to the AQI.",
        "Days NO2": "The count of days when nitrogen dioxide (NO2) is a primary pollutant affecting air quality and contributing to the AQI.",
        "Days Ozone": "The number of days with ozone (O3) as a primary pollutant influencing the AQI.",
        "Days PM2.5": "The count of days when fine particulate matter (PM2.5) is a primary pollutant impacting air quality and the AQI.",
        "Days PM10": "The number of days when larger particulate matter (PM10) is a primary pollutant contributing to the AQI.",
    }
    selected_column = st.selectbox("**Select a column to learn more about**", list(column_explanations.keys()))
    if selected_column:
        st.write(column_explanations[selected_column])


def aqi_dataset_plot_corr_heatmap(df_aqi, numerical_columns_aqi):
    fig, ax = plt.subplots()
    ax = sns.heatmap(df_aqi[numerical_columns_aqi].corr(), cmap="coolwarm")
    st.pyplot(fig)


def aqi_dataset_plot_missing_values(df_aqi):
    fig, ax = plt.subplots()
    ax = sns.heatmap(df_aqi.isnull().T, cbar=True, cmap="flare", xticklabels=False, yticklabels=True)

    ax.set_xlabel("Data Points")
    ax.set_title("Missing Values Heatmap")

    cbar = ax.collections[0].colorbar
    cbar.set_ticks([0, 1])
    cbar.set_ticklabels(["Not Missing", "Missing"])
    st.pyplot(fig)
    st.write(
        """
    There are no missing values in the dataset

    """
    )


def aqi_dataset_plot_yearly_coverage(df_aqi):
    columns = [
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
    ]
    numerical_column = st.selectbox("Select a column:", columns, index=8, key="tab_aqi4_col4")

    fig, ax = plt.subplots()
    ax = sns.histplot(df_aqi[numerical_column], bins=20, kde=True, color="skyblue")
    ax.lines[0].set_color("violet")
    ax.set_xlabel(f"{numerical_column} Values")
    ax.set_ylabel("Frequency")
    ax.set_title(f"Histogram of {numerical_column}")

    ax.grid(True, linestyle="--", alpha=0.3)
    st.pyplot(fig)

    st.write(
        """
    We can analyse how are values of a specific parameter is distributed from the above plot.

    """
    )


def aqi_dataset_plot_statewise_coverage(df_aqi):
    columns = [
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
    ]
    numerical_column = st.selectbox("Select a column:", columns, index=8, key="tab_aqi5_col6")

    fig, ax = plt.subplots(figsize=(10, 8))
    ax = sns.set_style("whitegrid")
    ax = sns.violinplot(data=df_aqi, x=numerical_column, y="State", linewidth=0, palette="rocket")
    ax.set_xlabel(f"{numerical_column} Values")
    ax.set_ylabel("State Name")
    ax.set_title(f"Violinplot of {numerical_column} by State")
    ax.tick_params(axis="y", labelsize=8)
    st.pyplot(fig)
    st.write(
        """
    We can analyse how are values of a specific parameter changes with respect to state from the above plot.


    """
    )
    plt.close()
    plt.clf()


def perform_eda_of_aqi_dataset():
    aqi_dataset_description()
    st.write(
        """
    ### Visualizations ###
    """
    )
    numerical_columns_aqi = list(df_aqi.select_dtypes(include=np.number).columns.values)
    tab_aqi1, tab_aqi2, tab_aqi3, tab_aqi4, tab_aqi5 = st.tabs(
        ["Summary Statistics", "Correlation", "Missing Values", "Histogram", "State-wise"]
    )
    with tab_aqi1:
        st.table(df_aqi.describe())

    with tab_aqi2:
        aqi_dataset_plot_corr_heatmap(df_aqi, numerical_columns_aqi)

    with tab_aqi3:
        aqi_dataset_plot_missing_values(df_aqi)

    with tab_aqi4:
        aqi_dataset_plot_yearly_coverage(df_aqi)

    with tab_aqi5:
        aqi_dataset_plot_statewise_coverage(df_aqi)


if "df" in st.session_state:
    df = st.session_state.df
else:
    df = utils.load_data("dataset/refined/annual_conc_by_monitor.parquet")
    st.session_state.df = df

if "df_aqi" in st.session_state:
    df_aqi = st.session_state.df_aqi
else:
    df_aqi = utils.load_data("dataset/refined/annual_aqi_by_county.csv")
    st.session_state.df_aqi = df_aqi

if "geojson_data" in st.session_state:
    geojson_data = st.session_state.geojson_data
else:
    with open("geojson/USA_state.geojson", "r") as geojson_file:
        geojson_data = json.load(geojson_file)
        st.session_state.geojson_data = geojson_data

# df.replace([np.inf, -np.inf], np.nan, inplace=True)
# df_aqi.replace([np.inf, -np.inf], np.nan, inplace=True)

mapbox_layout = utils.mapbox_layout
params = utils.params

st.header("Exploratory data analysis (EDA)")

st.subheader("About the dataset")
st.write(
    """
    The [EPA Air Quality Dataset](https://www.epa.gov/outdoor-air-quality-data) is a valuable resource provided by the United States Environmental Protection Agency (EPA) that offers a comprehensive and detailed record of air quality measurements across the United States.
    With a wide range of spatial and temporal granularity, the EPA's air quality dataset allows us to track air quality levels over time and across different locations, helping us understand the impact of air pollution on public health and the environment.
    Whether you're interested in studying long-term trends, assessing the effectiveness of air quality regulations, or simply gaining insights into local air quality, this dataset is an essential tool for making informed decisions and taking action to protect the air we breathe.
    
    """
)

st.subheader("Datasets Used")

tab_conc, tab_aqi = st.tabs(["Annual Concentration", "Annual AQI"])
with tab_conc:
    perform_eda_of_conc_dataset()
with tab_aqi:
    perform_eda_of_aqi_dataset()

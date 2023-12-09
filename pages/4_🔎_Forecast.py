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
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
import warnings
from sklearn.metrics import mean_squared_error, mean_absolute_error

warnings.filterwarnings("ignore", category=FutureWarning)

add_logo("airviz_image.png", height=30)
utils.add_navigation()


def write_intro():
    st.header("Forecast trends")
    st.write(
        """
    Forecasting pollutant trends is a crucial practice in environmental science, involving the analysis of historical data to predict future air pollutant concentrations. This process guides proactive decision-making, facilitating effective pollution control measures and timely public advisories for improved air quality and environmental health.
    """
    )



def write_explainations(parameter):
    st.write(
        """
    #### Impact and significance:
    """)
    if parameter=="Ozone":
        st.write(
            """
        The reduction in surface-level ozone levels year by year is a positive trend attributed to successful air quality management efforts. This decline is primarily due to the implementation of stringent emission controls and regulations targeting ozone precursors such as nitrogen oxides (NOx) and volatile organic compounds (VOCs). These measures have been effective in curbing industrial emissions, improving vehicle efficiency, and promoting cleaner technologies.

        The positive impact on the environment is substantial. Lower surface-level ozone levels contribute to enhanced respiratory health, reduced cardiovascular risks, and improved overall air quality. Additionally, decreased ozone concentrations benefit ecosystems, as high ozone levels can harm vegetation and ecosystems by inhibiting plant growth and disrupting ecological balances. The ongoing efforts to reduce surface-level ozone reflect a commitment to sustainable environmental practices and public well-being.
        """
        )

    elif parameter=="Carbon monoxide":
        st.write(
        """
        The consistent decline in carbon monoxide (CO) levels over the years is a favorable outcome attributed to successful emission reduction strategies and advancements in technology. Stringent regulations on vehicle emissions, industrial processes, and residential combustion have significantly contributed to this positive trend.

        The reduction in CO levels is beneficial for both human health and the environment. Lower concentrations of CO improve air quality and reduce the risk of adverse health effects associated with CO exposure. CO is a harmful gas that, when inhaled, can interfere with the body's ability to transport oxygen, leading to respiratory and cardiovascular issues. The decline in CO levels signifies improved combustion efficiency and cleaner energy sources, ultimately contributing to a healthier and more sustainable environment. This positive trend underscores the effectiveness of emission control measures and highlights the ongoing commitment to mitigating air pollution for the well-being of communities and ecosystems alike.
        """
        )

    elif parameter=="Sulfur dioxide":
        st.write(
        """
        The decrease in sulfur dioxide (SO2) levels over the years signifies a positive shift in environmental outcomes. This decline is largely a result of strict regulations and technological advancements aimed at reducing sulfur emissions from industrial processes, power plants, and transportation. The widespread adoption of cleaner fuels and emission control technologies, such as flue gas desulfurization systems, has played a pivotal role in mitigating SO2 pollution.

        This reduction in SO2 has significant benefits for both human health and the environment. Lower SO2 levels contribute to improved air quality, leading to decreased respiratory issues and cardiovascular risks in human populations. Additionally, it helps prevent acid rain formation, safeguarding ecosystems, aquatic life, and soil quality. The positive trend in reducing sulfur dioxide emissions reflects successful environmental policies and a commitment to sustainable practices, promoting a healthier and more balanced environment for current and future generations.
        """
        )

    elif parameter=="Nitrogen dioxide (NO2)":
        st.write(
        """
        The decrease in nitrogen dioxide (NO2) levels over recent years signifies successful initiatives in air quality management. This reduction is primarily a result of stricter regulations on emissions from industrial processes and transportation sources. Implementation of cleaner technologies, adoption of emission control technologies in vehicles, and improved fuel quality have contributed to lowering NO2 concentrations.

        The positive impact on the environment and public health is noteworthy. Lower NO2 levels lead to improved respiratory conditions, reduced risks of respiratory illnesses, and an overall enhancement of air quality. Moreover, the decline in NO2 emissions contributes to mitigating the adverse effects of nitrogen deposition on ecosystems, protecting vegetation, and supporting ecological balance.

        The decreasing trend in NO2 levels underscores a commitment to sustainable practices, highlighting the effectiveness of regulatory measures and technological advancements in reducing a significant air pollutant. This trend is indicative of a collective effort to create a healthier and more environmentally sustainable future.
        """
        )

    elif parameter=="PM10 Total 0-10um STP":
        st.write(
        """
        The reduction in PM10 (Particulate Matter with a diameter of 10 micrometers or smaller, Standard Temperature and Pressure) levels year by year is a positive outcome resulting from effective air quality management strategies. This decline can be attributed to the implementation of stringent regulations and practices aimed at mitigating sources of particulate matter, such as industrial emissions, vehicular exhaust, and other combustion processes.

        The positive environmental impact of decreasing PM10 levels is significant. Lower concentrations of PM10 contribute to improved respiratory health, as these particles can penetrate deep into the lungs, causing respiratory problems and other health issues. Furthermore, reduced PM10 levels have positive implications for environmental quality, safeguarding ecosystems and preventing adverse effects on soil, water, and vegetation.

        The ongoing efforts to decrease PM10 levels underscore a commitment to sustainable air quality practices, fostering a healthier environment for both human populations and ecosystems. This trend signifies progress in addressing pollution sources and implementing measures to enhance air quality, ultimately benefiting public health and the well-being of the broader ecosystem.
        """
        )

    elif parameter=="PM10-2.5 - Local Conditions":
        st.write(
        """
        The decline in PM10-2.5 (particulate matter with a diameter between 2.5 and 10 micrometers) levels at the local level signals positive advancements in air quality management. This reduction is often a result of targeted interventions, including stricter industrial emission controls, improved traffic management, and public awareness initiatives. Local authorities have implemented measures to mitigate sources of PM10-2.5, such as industrial processes, construction activities, and road dust.

        The improvement in local PM10-2.5 levels carries significant environmental and public health benefits. Lower concentrations reduce respiratory and cardiovascular risks, particularly in vulnerable populations. Additionally, it protects the environment by minimizing the negative impact of particulate matter on air quality, visibility, and ecosystems. The decline in PM10-2.5 underscores the success of community-based initiatives and regulatory measures aimed at fostering cleaner, healthier local environments. Continued efforts in this direction are crucial for sustaining these positive trends and ensuring long-term air quality improvements.
        """
        )

    elif parameter=="PM2.5 - Local Conditions":
        st.write(
        """
        The reduction in local PM2.5 levels over recent years signals positive advancements in local air quality management. This decline can be attributed to targeted measures addressing the sources of fine particulate matter, including industrial emissions, vehicular pollution, and combustion processes. Local authorities have implemented regulations and initiatives to control emissions from these sources, leading to a decrease in PM2.5 concentrations.

        The positive impact on local conditions is noteworthy. Lower PM2.5 levels contribute to improved respiratory health, particularly benefiting vulnerable populations such as children and the elderly. Reduced exposure to fine particulate matter is associated with lower risks of respiratory and cardiovascular diseases. Furthermore, improved air quality positively influences the aesthetics of the local environment, enhancing visibility and overall well-being.

        Local efforts to decrease PM2.5 levels align with broader environmental goals, promoting sustainable development and prioritizing the health of communities. Continued vigilance and proactive measures will be essential to sustain and further improve local air quality conditions.
        """
        )

    elif parameter=="Acceptable PM2.5 AQI & Speciation Mass":
        st.write(
        """
        Decreasing PM2.5 (Particulate Matter ≤ 2.5 micrometers) Air Quality Index (AQI) levels indicate successful measures in reducing fine particle pollution. Tightened regulations targeting industrial emissions and improved technologies contribute to lower PM2.5 concentrations. This reduction benefits public health by minimizing respiratory and cardiovascular risks and improves environmental quality. Speciation mass analysis aids in understanding PM2.5 composition, facilitating targeted pollution control. These efforts demonstrate a commitment to sustainable practices and overall well-being.
        """
        )

    elif parameter=="Lead (TSP) STP":
        st.write(
        """
        While surface-level ozone reduction signifies positive strides in air quality, a similar positive trend can be observed in the decline of lead levels, particularly in Total Suspended Particles (TSP) and Suspended Total Particles (STP). This decrease is primarily a result of regulatory measures and environmental policies that restrict lead emissions from various sources such as industrial activities, leaded gasoline usage, and manufacturing processes.

        The phase-out of leaded gasoline, a major contributor to airborne lead, has played a crucial role in this reduction. Additionally, advancements in industrial processes, the use of unleaded alternatives, and the enforcement of strict emission standards contribute to the diminishing lead concentrations in the atmosphere.

        The environmental benefits of decreasing lead levels are significant. Lower lead emissions lead to improved air quality, reducing the risk of lead exposure to both humans and ecosystems. Exposure to lead is associated with adverse health effects, especially on the nervous system, and can have harmful consequences for wildlife and plant life. The decline in lead levels is a positive indicator of successful environmental regulations and efforts to safeguard public health and ecological balance.
        """
        )
def get_options_for_forecasting(df,params):
    forepolcol1,forepolcol2,forepolcol3=st.columns([2,2,3])

    with forepolcol1:
        model_type = st.selectbox("Choose model",
                [
                    "Prophet",
                    "Arima",
                ],
                index=0
            )
        state_list = ["All"] +df["State Name"].unique().tolist()
        selected_state = st.selectbox("Select State", state_list, index=5)

    with forepolcol2:
        ignored_params=["Barometric pressure", "Relative Humidity ", "Dew Point", "Outdoor Temperature", "Wind Direction - Resultant", "Wind Speed - Resultant"]
        relevant_params= [param for param in params if param not in ignored_params]
        parameter = st.selectbox("Select the Parameter to visualize", relevant_params, index=params.index("Ozone"))
        county_list = ["All"]+ df[df["State Name"] == selected_state]["County Name"].unique().tolist()
        selected_county = st.selectbox("Select County", county_list, index=0)
        
    with forepolcol3:  
        year_range = st.slider(
                "Select years to consider for training data",
                min_value=int(df["Year"].min()),
                max_value=int(2021),
                value=[1985,2015],
                key="train_year",
            )
        pred_year=st.slider(
                "Number of years to predict in the future",
                min_value=1,
                max_value=20,
                value=5,
                key="pred_year",
            )
    return model_type, parameter, year_range, pred_year, selected_state, selected_county

def extract_filtered_df(df,parameter,year_range,selected_state, selected_county):
    available_measurement_types=df[df["Parameter Name"] == parameter]["Sample Duration"].unique()
    if "1 HOUR" in available_measurement_types:
        measurement_type="1 HOUR"
    else:
        measurement_type=available_measurement_types[0]
    aggregation = {
        f"Arithmetic Mean": "mean",
    }
    p_df = df[df["Parameter Name"] == parameter]
    year_df = p_df[(p_df["Year"] >= year_range[0]) & (p_df["Year"] <= 2022)]
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
            county_df[(county_df["Sample Duration"] == measurement_type)]
            .groupby(["Year"])
            .agg(aggregation)
            .reset_index()
        )
    return filtered_df

def estimate_and_print_metrics(actual_values,predicted_values):

    min_length = min(len(actual_values), len(predicted_values))

    if min_length>=1:
        # Trim the arrays to the minimum length
        actual_values = actual_values[:min_length]
        predicted_values = predicted_values[:min_length]
        # Calculate RMSE
        rmse = np.sqrt(mean_squared_error(actual_values, predicted_values))
        range_y = np.max(actual_values) - np.min(actual_values)
        nrmse = rmse / range_y if range_y > 0 else 0

        mape = np.mean(np.abs((actual_values - predicted_values) / actual_values)) * 100
        st.write(
            f"""
            ##### Model Metrics

            Normalized RMSE (NRMSE):  **{round(nrmse, 4)}**

            Mean Absolute Percentage Error (MAPE):  **{round(mape, 4)}%**
            """)


def forecast_and_plot_using_prophet(temp_df,model_type,parameter,year_range,pred_year):
    model = Prophet(changepoint_prior_scale=0.1)
    training_data=temp_df[temp_df['ds'].dt.year <= year_range[1]]
    testing_data=temp_df[temp_df['ds'].dt.year > year_range[1]]
    model.fit(training_data)

    # Create a DataFrame with future dates for prediction
    future = model.make_future_dataframe(periods=pred_year, freq='Y')  # Forecast for the next 5 years
    forecast = model.predict(future).tail(pred_year)

    # Ensure predicted values do not go below zero
    forecast['yhat'] = forecast['yhat'].clip(lower=0)
    forecast['yhat_lower'] = forecast['yhat_lower'].clip(lower=0)
    forecast['yhat_upper'] = forecast['yhat_upper'].clip(lower=0)

    # Create a Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=training_data['ds'], y=training_data['y'], mode='markers+lines', name='Actual Train data', marker=dict(color='blue')))
    fig.add_trace(go.Scatter(x=testing_data['ds'], y=testing_data['y'], mode='markers+lines', name='Actual Test data', marker=dict(color='green')))
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast['ds'], forecast['ds'][::-1]]),
        y=pd.concat([forecast['yhat_upper'], forecast['yhat_lower'][::-1]]),
        fill='toself',
        fillcolor='rgba(255, 165, 0, 0.2)',
        line=dict(color='rgba(255, 255, 255, 0)'),
        name='Uncertainty Band'
    ))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='markers+lines', name='Prophet Forecast', line=dict(dash='dash', color='orange')))


    # Update layout
    fig.update_layout(
        title=f'{model_type} Forecasting for {parameter} from {year_range[1]} to {str(year_range[1]+pred_year)}',
        xaxis=dict(title='Year'),
        yaxis=dict(title=f'{parameter}'),
        legend=dict(x=1, y=1, traceorder='normal', orientation='v')
    )


    st.plotly_chart(fig, use_container_width=True)
    actual_values = testing_data['y'].values
    predicted_values = forecast['yhat'].values
    estimate_and_print_metrics(actual_values,predicted_values)


def forecast_and_plot_using_arima(temp_df,model_type,parameter,year_range,pred_year):

    training_data=temp_df[temp_df['ds'].dt.year <= year_range[1]]
    testing_data=temp_df[temp_df['ds'].dt.year > year_range[1]]
    order = (1, 1, 1)  # You may need to choose appropriate values for the order parameter
    model_arima = ARIMA(training_data['y'], order=order)
    results = model_arima.fit()

    # Forecast for the next 5 years with a smaller uncertainty band
    forecast_steps = pred_year
    forecast_arima = results.get_forecast(steps=forecast_steps)
    forecast_mean = forecast_arima.predicted_mean.values
    forecast_std = forecast_arima.se_mean.values  # Standard error

    # Ensure predicted values do not go below zero
    forecast_mean = np.maximum(forecast_mean, 0)
    confidence_interval_multiplier = 1.0  # Adjust this multiplier for the desired uncertainty band size
    forecast_upper = np.maximum(forecast_mean + confidence_interval_multiplier * forecast_std, 0)
    forecast_lower = np.maximum(forecast_mean - confidence_interval_multiplier * forecast_std, 0)

    future_dates = pd.date_range(start=training_data['ds'].max(), periods=forecast_steps + 1, freq='Y')[1:]
    forecast_df_arima = pd.DataFrame({'ds': future_dates, 'yhat': forecast_mean, 'yhat_upper': forecast_upper, 'yhat_lower': forecast_lower})

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=training_data['ds'], y=training_data['y'], mode='markers+lines', name='Actual Train data', marker=dict(color='blue')))
    fig.add_trace(go.Scatter(x=testing_data['ds'], y=testing_data['y'], mode='markers+lines', name='Actual Test data', marker=dict(color='green')))
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast_df_arima['ds'], forecast_df_arima['ds'][::-1]]),
        y=pd.concat([forecast_df_arima['yhat_upper'], forecast_df_arima['yhat_lower'][::-1]]),
        fill='toself',
        fillcolor='rgba(255, 165, 0, 0.2)',
        line=dict(color='rgba(255, 255, 255, 0)'),
        name='Uncertainty Band'
    ))
    fig.add_trace(go.Scatter(x=forecast_df_arima['ds'], y=forecast_df_arima['yhat'], mode='markers+lines', name='ARIMA Forecast', line=dict(dash='dash', color='orange')))

    fig.update_layout(
        title=f'{model_type} Forecasting for {parameter} from {year_range[1]} to {str(year_range[1]+pred_year)}',
        xaxis=dict(title='Year'),
        yaxis=dict(title=f'{parameter}'),
        legend=dict(x=1, y=1, traceorder='normal', orientation='v')
    )

    # Show the plot
    st.plotly_chart(fig, use_container_width=True)
    actual_values = testing_data['y'].values
    predicted_values = forecast_df_arima['yhat'].values
    estimate_and_print_metrics(actual_values,predicted_values)

def forecast_pollutant_trends(df, params):
    model_type, parameter, year_range, pred_year, selected_state, selected_county=get_options_for_forecasting(df, params)
    filtered_df=extract_filtered_df(df,parameter,year_range,selected_state, selected_county)
    original_df = pd.DataFrame(filtered_df)

    # Rename columns to 'ds' and 'y' as required by Prophet
    temp_df = original_df.rename(columns={'Year': 'ds', 'Arithmetic Mean': 'y'})
    temp_df['ds'] = pd.to_datetime(temp_df['ds'].astype(str) + '-12-31')

    if temp_df['ds'] is None or len(temp_df['ds'])<2:
        st.write(
        """
        There are less than 2 data points in the given range. Please choose a different option
        """
        )
    else:
        if model_type=="Prophet":
            forecast_and_plot_using_prophet(temp_df,model_type,parameter,year_range,pred_year)

        if model_type=="Arima":
            forecast_and_plot_using_arima(temp_df,model_type,parameter,year_range,pred_year)
    show_metrics_info = st.checkbox('Learn about mertics used', key="metrics_")
    if show_metrics_info:
        st.write(
            """
            - **RMSE:** Measures the average prediction error. Lower values indicate better accuracy.
            - **Normalized RMSE:** RMSE normalized by the range of the target variable. Useful for comparing models across different scales.
            - **MAPE:** Measures the average percentage difference between predicted and actual values. Lower values indicate better accuracy.
            """
        )
    write_explainations(parameter)

def get_options_for_forecasting_aqi(df_aqi):
    foreaqicol1,foreaqicol2,foreaqicol3=st.columns([2,2,3])

    with foreaqicol1:
        model_type = st.selectbox("Choose model",
                [
                    "Prophet",
                    "Arima",
                ],
                index=0,
                key="model_aqi"
            )
        state_list = ["All"]+ df_aqi["State"].unique().tolist()
        selected_state = st.selectbox("Select State", state_list, index=2, key="state_aqi")

    with foreaqicol2:
        parameter = st.selectbox("Select the Parameter to visualize", ["Max AQI","Median AQI"], index=1)
        county_list = ["All"]+ df_aqi[df_aqi["State"] == selected_state]["County"].unique().tolist()
        selected_county = st.selectbox("Select County", county_list, index=0, key="county_aqi")
        
    with foreaqicol3:  
        year_range = st.slider(
                "Select years to consider for training data",
                min_value=int(df["Year"].min()),
                max_value=int(2021),
                value=[1985,2015],
                key="train_year_aqi",
            )
        pred_year=st.slider(
                "Number of years to predict in the future",
                min_value=1,
                max_value=20,
                value=5,
                key="pred_year_aqi",
            )
    return model_type, parameter, year_range, pred_year, selected_state, selected_county

def extract_filtered_df_aqi(df_aqi,year_range,selected_state, selected_county):
    aggregation = {
        f"Max AQI": "max",
        f"Median AQI": "mean"
    }
    year_df = df_aqi[(df_aqi["Year"] >= year_range[0]) & (df_aqi["Year"] <= 2022)]
    if selected_state == "All":
        filtered_df = (
            year_df.groupby(["Year"]).agg(aggregation).reset_index()
        )
    elif selected_county == "All":
        state_df = year_df[year_df["State"] == selected_state]
        filtered_df = (
            state_df.groupby(["Year"]).agg(aggregation).reset_index()
        )
    else:
        state_df = year_df[year_df["State"] == selected_state]
        county_df = state_df[state_df["County"] == selected_county]
        filtered_df = (
            county_df.groupby(["Year"]).agg(aggregation).reset_index()
        )
    return filtered_df

def forecast_and_plot_aqi_using_prophet(temp_df_aqi,model_type,parameter,year_range,pred_year):
    training_data=temp_df_aqi[temp_df_aqi['ds'].dt.year <= year_range[1]]
    testing_data=temp_df_aqi[temp_df_aqi['ds'].dt.year > year_range[1]]
    model = Prophet(changepoint_prior_scale=0.1)
    model.fit(training_data)

    # Create a DataFrame with future dates for prediction
    future = model.make_future_dataframe(periods=pred_year, freq='Y')  # Forecast for the next 5 years
    forecast = model.predict(future).tail(pred_year)

    # Ensure predicted values do not go below zero
    forecast['yhat'] = forecast['yhat'].clip(lower=0)
    forecast['yhat_lower'] = forecast['yhat_lower'].clip(lower=0)
    forecast['yhat_upper'] = forecast['yhat_upper'].clip(lower=0)

    # Create a Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=training_data['ds'], y=training_data['y'], mode='markers+lines', name='Actual', marker=dict(color='blue')))
    fig.add_trace(go.Scatter(x=testing_data['ds'], y=testing_data['y'], mode='markers+lines', name='Actual Test data', marker=dict(color='green')))

    fig.add_trace(go.Scatter(
        x=pd.concat([forecast['ds'], forecast['ds'][::-1]]),
        y=pd.concat([forecast['yhat_upper'], forecast['yhat_lower'][::-1]]),
        fill='toself',
        fillcolor='rgba(255, 165, 0, 0.2)',
        line=dict(color='rgba(255, 255, 255, 0)'),
        name='Uncertainty Band'
    ))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='markers+lines', name='Prophet Forecast', line=dict(dash='dash', color='orange')))


    # Update layout
    fig.update_layout(
        title=f'{model_type} Forecasting for {parameter} from {year_range[1]} to {str(year_range[1]+pred_year)}',
        xaxis=dict(title='Year'),
        yaxis=dict(title=f'{parameter}'),
        legend=dict(x=1, y=1, traceorder='normal', orientation='v')
    )


    st.plotly_chart(fig, use_container_width=True)

    actual_values = testing_data['y'].values
    predicted_values = forecast['yhat'].values
    estimate_and_print_metrics(actual_values,predicted_values)
    
def forecast_and_plot_aqi_using_arima(temp_df_aqi,model_type,parameter,year_range,pred_year):
    training_data=temp_df_aqi[temp_df_aqi['ds'].dt.year <= year_range[1]]
    testing_data=temp_df_aqi[temp_df_aqi['ds'].dt.year > year_range[1]]
    order = (1, 1, 1)  # You may need to choose appropriate values for the order parameter
    model_arima = ARIMA(training_data['y'], order=order)
    results = model_arima.fit()

    # Forecast for the next 5 years with a smaller uncertainty band
    forecast_steps = pred_year
    forecast_arima = results.get_forecast(steps=forecast_steps)
    forecast_mean = forecast_arima.predicted_mean.values
    forecast_std = forecast_arima.se_mean.values  # Standard error

    # Ensure predicted values do not go below zero
    forecast_mean = np.maximum(forecast_mean, 0)
    confidence_interval_multiplier = 1.0  # Adjust this multiplier for the desired uncertainty band size
    forecast_upper = np.maximum(forecast_mean + confidence_interval_multiplier * forecast_std, 0)
    forecast_lower = np.maximum(forecast_mean - confidence_interval_multiplier * forecast_std, 0)

    future_dates = pd.date_range(start=training_data['ds'].max(), periods=forecast_steps + 1, freq='Y')[1:]
    forecast_df_arima = pd.DataFrame({'ds': future_dates, 'yhat': forecast_mean, 'yhat_upper': forecast_upper, 'yhat_lower': forecast_lower})

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=training_data['ds'], y=training_data['y'], mode='markers+lines', name='Actual', marker=dict(color='blue')))
    fig.add_trace(go.Scatter(x=testing_data['ds'], y=testing_data['y'], mode='markers+lines', name='Actual Test data', marker=dict(color='green')))
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast_df_arima['ds'], forecast_df_arima['ds'][::-1]]),
        y=pd.concat([forecast_df_arima['yhat_upper'], forecast_df_arima['yhat_lower'][::-1]]),
        fill='toself',
        fillcolor='rgba(255, 165, 0, 0.2)',
        line=dict(color='rgba(255, 255, 255, 0)'),
        name='Uncertainty Band'
    ))
    fig.add_trace(go.Scatter(x=forecast_df_arima['ds'], y=forecast_df_arima['yhat'], mode='markers+lines', name='ARIMA Forecast', line=dict(dash='dash', color='orange')))

    fig.update_layout(
        title=f'{model_type} Forecasting for {parameter} from {year_range[1]} to {str(year_range[1]+pred_year)}',
        xaxis=dict(title='Year'),
        yaxis=dict(title=f'{parameter}'),
        legend=dict(x=1, y=1, traceorder='normal', orientation='v')
    )

    # Show the plot
    st.plotly_chart(fig, use_container_width=True)

    actual_values = testing_data['y'].values
    predicted_values = forecast_df_arima['yhat'].values
    estimate_and_print_metrics(actual_values,predicted_values)

def forecast_aqi_trends(df_aqi):
    model_type, parameter, year_range, pred_year, selected_state, selected_county=get_options_for_forecasting_aqi(df_aqi)
    filtered_df = extract_filtered_df_aqi(df_aqi,year_range,selected_state, selected_county)
    original_df = pd.DataFrame(filtered_df)


    # Rename columns to 'ds' and 'y' as required by Prophet
    temp_df_aqi = original_df.rename(columns={'Year': 'ds', f"{parameter}": 'y'})
    temp_df_aqi['ds'] = pd.to_datetime(temp_df_aqi['ds'].astype(str) + '-12-31')

    if temp_df_aqi['ds'] is None or len(temp_df_aqi[temp_df_aqi['ds'].dt.year <= year_range[1]]['ds'])<2:
        st.write(
        """
        There are less than 2 data points in the given range. Please choose a different option
        """
        )
    else:
        if model_type=="Prophet":
            forecast_and_plot_aqi_using_prophet(temp_df_aqi,model_type,parameter,year_range,pred_year)

        if model_type=="Arima":
            forecast_and_plot_aqi_using_arima(temp_df_aqi,model_type,parameter,year_range,pred_year)

    show_metrics_info = st.checkbox('Learn about mertics used', key="metrics_aqi")
    if show_metrics_info:
        st.write(
            """
            - **RMSE:** Measures the average prediction error. Lower values indicate better accuracy.
            - **Normalized RMSE:** RMSE normalized by the range of the target variable. Useful for comparing models across different scales.
            - **MAPE:** Measures the average percentage difference between predicted and actual values. Lower values indicate better accuracy.
            """
        )
    st.write(
        """
    #### Impact and significance:
    """)
    st.write(
        """
    The recent Air Quality Index (AQI) trend predictions indicate improving air quality conditions. These forecasts offer valuable insights for informed decision-making, helping stakeholders and the public anticipate and respond to changing pollution levels. The positive trend underscores advancements in pollution control efforts, contributing to a healthier environment.
    """
    )

def forcast_trends(df,df_aqi,params):
    foretab1, foretab2= st.tabs(["Pollutant Trends", "AQI Trend"])
    with foretab1:
        forecast_pollutant_trends(df,params)
    with foretab2:    
        forecast_aqi_trends(df_aqi)

    

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

params = utils.params

write_intro()
forcast_trends(df,df_aqi,params)

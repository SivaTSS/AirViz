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
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from xgboost import XGBRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score


add_logo("airviz_image.png", height=30)
utils.add_navigation()


def write_intro():
    st.header("Predict AQI")
    st.write(
        """
    In our ever-changing world, predicting the Air Quality Index (AQI) has become essential to safeguard public health and the environment. As we contend with the impacts of urbanization and industrialization, it's crucial to comprehend and anticipate fluctuations in AQI. Taking a proactive stance, driven by advanced technologies and collaborative efforts, enables us to make informed decisions. This approach ensures that we can implement measures effectively, contributing to a cleaner and healthier future for everyone.
    
    """
    )


def train_and_evaluate_model(df_aqi):
    st.subheader("Model Builder")
    st.write(
        f"""
    This section of the application serves as a tool to construct a model and assess its performance.
    """
    )
    modelcol1, modelcol2 = st.columns([4, 3])
    with modelcol1:
        model_type = st.selectbox(
            "Choose model",
            ["Linear Regressor", "XGBoost Regressor", "Lasso Regressor", "Ridge Regressor", "Support Vector Regressor"],
            index=0,
            key="model_aqi",
        )
        test_size = st.slider("Select test set size", min_value=0.1, max_value=0.9, value=0.2)
    with modelcol2:
        feature_names = st.multiselect(
            "Select features to model:",
            ["Days CO", "Days NO2", "Days Ozone", "Days PM2.5", "Days PM10"],
            default=["Days CO", "Days NO2", "Days Ozone", "Days PM2.5", "Days PM10"],
        )

    col_to_pred = "Median AQI"
    df_temp_aqi = df_aqi.copy()  # [df_aqi["Year"]==year]
    df_temp_aqi = df_temp_aqi[feature_names + ["Year"] + [col_to_pred]]

    feature_columns = df_temp_aqi.drop(col_to_pred, axis=1)
    target_column = df_temp_aqi[col_to_pred]
    X_train, X_test, y_train, y_test = train_test_split(
        feature_columns, target_column, test_size=test_size, random_state=42
    )

    if model_type == "Linear Regressor":
        model = LinearRegression()

    elif model_type == "Lasso Regressor":
        # You can specify the alpha parameter for L1 regularization
        alpha = 1.0  # You may adjust the value
        model = Lasso(alpha=alpha)

    elif model_type == "XGBoost Regressor":
        # You can specify hyperparameters based on your requirements
        model = XGBRegressor()

    elif model_type == "Ridge Regressor":
        # You can specify the alpha parameter for L2 regularization
        alpha = 1.0  # You may adjust the value
        model = Ridge(alpha=alpha)

    elif model_type == "Support Vector Regressor":
        # You can specify hyperparameters based on your requirements
        model = SVR()

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    norm_rmse = rmse / (np.max(y_test) - np.min(y_test))

    # Display metrics
    st.write(
        f"""
        ##### Model Metrics

        Normalized RMSE: **{str(round(norm_rmse, 4))}**

        R-squared: **{str(round(r2, 4))}**
        """
    )
    show_metrics_info = st.checkbox("Learn about mertics used")
    if show_metrics_info:
        st.write(
            """
            - **RMSE:** Measures the average prediction error. Lower values indicate better accuracy.
            - **Normalized RMSE:** RMSE normalized by the range of the target variable. Useful for comparing models across different scales.
            - **R-squared (R²):** Represents the proportion of variance in the dependent variable explained by the model. Closer to 1 is better.
            """
        )
    st.write(
        """ 
        Even thought the R-square is low for the above models, it is able to approximately grasp the general trend of AQI.
        """
    )
    return model, feature_names


def predict_on_new_data(model, df_aqi, feature_names):
    st.subheader("Predict AQI on custom data")
    st.write(
        f"""
    The below fields are prefilled with average values in USA. Try out different values for your location and get to know the Median AQI.
    """
    )
    predcol1, predcol2, predcol3 = st.columns(3)
    with predcol1:
        days_co = st.number_input(
            "Days of excess CO", min_value=0, max_value=365, value=int(np.mean(df_aqi["Days CO"])), step=5
        )
        days_no2 = st.number_input(
            "Days of excess NO2", min_value=0, max_value=365, value=int(np.mean(df_aqi["Days NO2"])), step=5
        )
    with predcol2:
        days_ozone = st.number_input(
            "Days of excess Ozone", min_value=0, max_value=365, value=int(np.mean(df_aqi["Days Ozone"])), step=5
        )
        days_pm25 = st.number_input(
            "Days of excess PM2.5", min_value=0, max_value=365, value=int(np.mean(df_aqi["Days PM2.5"])), step=5
        )
    with predcol3:
        days_pm10 = st.number_input(
            "Days of excess PM10", min_value=0, max_value=365, value=int(np.mean(df_aqi["Days PM10"])), step=5
        )

    # Create a DataFrame with user input
    new_dict = dict()

    for feature_name in feature_names:
        if feature_name == "Days CO":
            new_dict[feature_name] = [days_co]
        elif feature_name == "Days NO2":
            new_dict[feature_name] = [days_no2]
        elif feature_name == "Days Ozone":
            new_dict[feature_name] = [days_ozone]
        elif feature_name == "Days PM2.5":
            new_dict[feature_name] = [days_pm25]
        elif feature_name == "Days PM10":
            new_dict[feature_name] = [days_pm10]
    new_dict["Year"] = [2010]
    new_data = pd.DataFrame(new_dict)
    new_predictions = model.predict(new_data)
    if new_predictions[0] < 50:
        st.markdown(
            f"""
            ##### <span style="color: green;">The Median AQI for the given values is **{str(round(new_predictions[0], 4))}**. The air quality is good most of the days.</span>
            """,
            unsafe_allow_html=True,
        )
    elif new_predictions[0] < 100:
        st.write(
            f"""
            ##### <span style="color: orange;">The Median AQI for the given values is **{str(round(new_predictions[0], 4))}**. The air quality is moderate most of the days.</span>
        """,
            unsafe_allow_html=True,
        )
    elif new_predictions[0] < 150:
        st.write(
            f"""
            ##### <span style="color: red;">The Median AQI for the given values is **{str(round(new_predictions[0], 4))}**. The air quality is Unhealthy for Sensitive Groups most of the days.</span>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.write(
            f"""
            ##### <span style="color: brown;">The Median AQI for the given values is **{str(round(new_predictions[0], 4))}**. The air quality is Unhealthy most of the days.</span>
        """,
            unsafe_allow_html=True,
        )


def train_and_predict_model_for_aqi(df_aqi):
    model, feature_names = train_and_evaluate_model(df_aqi)
    predict_on_new_data(model, df_aqi, feature_names)


if "df_aqi" in st.session_state:
    df_aqi = st.session_state.df_aqi
else:
    df_aqi = utils.load_data("dataset/refined/annual_aqi_by_county.csv")
    st.session_state.df_aqi = df_aqi

params = utils.params

write_intro()
train_and_predict_model_for_aqi(df_aqi)

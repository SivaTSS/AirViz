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
from sklearn.preprocessing import OneHotEncoder
from sklearn.neural_network import MLPRegressor


add_logo("airviz_image.png", height=30)
utils.add_navigation()

def write_intro():
    st.header("Predict AQI")
    st.write(
        """
    In our evolving world, predicting Air Quality Index (AQI) has become imperative for safeguarding public health and the environment. As we grapple with the consequences of urbanization and industrialization, understanding and anticipating AQI fluctuations is crucial. This proactive approach, fueled by advanced technologies and collaborative efforts, empowers us to take informed measures, ensuring a cleaner, healthier future for all."""
    )

def train_and_evaluate_model(df_aqi):
    st.subheader("Train Model")

    modelcol1,modelcol2=st.columns([4,3])
    with modelcol1:
        model_type = st.selectbox("Choose model",
                [
                    "XGBoost Regressor",
                    "Linear Regressor",
                    "Lasso Regressor",
                    "Ridge Regressor",
                    "Support Vector Regressor"
                ],
                index=0,
                key="model_aqi"
            )
        test_size = st.slider("Select test set size", min_value=0.1, max_value=0.9, value=0.2)
    with modelcol2:
        feature_names=st.multiselect(
            "Select features to model:",
            ['Days CO', 'Days NO2',
       'Days Ozone', 'Days PM2.5', 'Days PM10'],
            default=['Days CO', 'Days NO2',
       'Days Ozone', 'Days PM2.5', 'Days PM10'],
        )

        
        

    col_to_pred="Median AQI"
    df_temp_aqi = df_aqi.copy()#[df_aqi["Year"]==year]
    df_temp_aqi = df_temp_aqi[feature_names+["Year"]+[col_to_pred]]

    feature_columns = df_temp_aqi.drop(col_to_pred, axis=1)
    target_column = df_temp_aqi[col_to_pred]
    X_train, X_test, y_train, y_test = train_test_split(feature_columns, target_column, test_size=test_size, random_state=42)

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

    st.write(
        f"""
        ##### Model Metrics
        Root Mean Squared Error (RMSE): **{str(round(rmse,4))}**, R-squared: **{str(round(r2,4))}**
        """)
    return model

def predict_on_new_data(model,df_aqi):
    st.subheader("Precict AQI on custom data")
    predcol1,predcol2,predcol3=st.columns(3)

    with predcol1:
        days_co = st.number_input("Days CO", min_value=0, max_value=365, value=int(np.mean(df_aqi["Days CO"])), step=5)
        days_no2 = st.number_input("Days NO2", min_value=0, max_value=365, value=int(np.mean(df_aqi["Days NO2"])), step=5)
    with predcol2:
        days_ozone = st.number_input("Days Ozone", min_value=0, max_value=365, value=int(np.mean(df_aqi["Days Ozone"])), step=5)
        days_pm25 = st.number_input("Days PM2.5", min_value=0, max_value=365, value=int(np.mean(df_aqi["Days PM2.5"])), step=5)
    with predcol3:
        days_pm10 = st.number_input("Days PM10", min_value=0, max_value=365, value=int(np.mean(df_aqi["Days PM10"])), step=5)

    # Create a DataFrame with user input
    new_data = pd.DataFrame({
        'Days CO': [days_co],
        'Days NO2': [days_no2],
        'Days Ozone': [days_ozone],
        'Days PM2.5': [days_pm25],
        'Days PM10': [days_pm10],
        'Year': [2010],
    })

    new_predictions = model.predict(new_data)

    st.write(
        f"""
    The Median AQI for the given values is **{str(round(new_predictions[0],4))}**
    """)

def train_and_predict_model_for_aqi(df_aqi):

    model=train_and_evaluate_model(df_aqi)
    predict_on_new_data(model,df_aqi)

    

if "df_aqi" in st.session_state:
    df_aqi = st.session_state.df_aqi
else:
    df_aqi = utils.load_data("dataset/refined/annual_aqi_by_county.csv")
    st.session_state.df_aqi = df_aqi

params = utils.params

write_intro()
train_and_predict_model_for_aqi(df_aqi)

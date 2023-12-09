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

st.subheader("Conclusion")
st.write(
    """
In conclusion, air quality metrics are crucial tools for assessing and understanding the state of our atmosphere. They provide valuable information about the presence of various air pollutants and help individuals, communities, and policymakers make informed decisions to protect public health and the environment.

By measuring and monitoring parameters such as particulate matter, ground-level ozone, carbon monoxide, sulfur dioxide, and nitrogen dioxide, air quality metrics offer a clear picture of air quality in a specific location. This information empowers us to take appropriate actions, from limiting outdoor activities on days with poor air quality to implementing policies and practices aimed at reducing pollution sources.

As we continue to face environmental challenges and the potential health impacts of air pollution, the use of air quality metrics becomes increasingly important. By staying informed and utilizing this data, we can work toward cleaner air, healthier lives, and a more sustainable future for our planet.

"""
)

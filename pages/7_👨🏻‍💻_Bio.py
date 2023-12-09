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

st.write(
    """
### Subramaniya Siva T S

#### About Me
Hello! I'm Subramaniya Siva T S, a passionate and driven individual currently pursuing a Master's degree in Data Science. With a strong foundation in both theoretical knowledge and practical application, I am dedicated to exploring the vast and dynamic field of data science.

#### Education
Master of Science in Data Science [Michigan State University, USA]

#### Skills
Programming: C++, Python, MATLAB, R, HTML, SQL

Softwares/Frameworks: Pytorch, TensorFlow, sklearn, OpenCV, Streamlit, Flask


#### Connect with Me
I'm always open to connecting with like-minded individuals, professionals, and researchers. Feel free to reach out to me via [LinkedIn](https://www.linkedin.com/in/subramaniya-siva-t-s/), and let's explore the possibilities of collaboration and knowledge exchange!

"""
)

import streamlit as st
import datetime
import numpy as np
import pandas as pd

# from data_cleaning import data_all



st.markdown('# Map Test')
df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(df)




from st_aggrid import AgGrid
st.markdown('# Fancy Dataframe Test')
df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')
AgGrid(df)
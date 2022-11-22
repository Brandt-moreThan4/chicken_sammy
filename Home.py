from pathlib import Path
import json
import pandas as pd
from datetime import datetime
from typing import List
import streamlit as st
import plotly.express as px
from data_cleaning import gdata
import streamlit.components.v1 as components



INTRO_MD = '''
## A Chicken Sammy Adventure
##### *Boldly Going Where None Have Gone Before*
#
## Analysis
 '''

st.markdown(INTRO_MD)


df = gdata.df_msg

st.markdown('### Wordiest Individuals')
char_counts = df.groupby('name')['char_count'].mean().sort_values(ascending=False).to_frame().iloc[:15].reset_index()
fig1 = px.bar(char_counts,x='name',y='char_count')
st.plotly_chart(fig1)

st.markdown('### Most Messages')
msg_counts = df.groupby('name')['created_at'].count().sort_values(ascending=False).to_frame().iloc[:15].reset_index()
fig2 = px.bar(msg_counts,x='name',y='created_at')
st.plotly_chart(fig2)

st.markdown('### Hall of Fame: Most Liked Messages')

print(f'Home: {datetime.now()}')
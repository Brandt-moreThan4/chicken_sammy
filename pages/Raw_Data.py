
import streamlit as st
from data_cleaning import data_all
import pandas as pd


def convert_df(df:pd.DataFrame):
    return df.to_csv().encode('utf-8')

st.markdown('## Member Data')
st.write(data_all.df_members)

st.download_button(
    "Press to Download Member Data",
    convert_df(data_all.df_members),
    "members.csv",
    "text/csv",
    key='member-data'
)

st.markdown('## MSG Data: (Bug in Displayhere)')
st.download_button(
    "Press to Download Message Data",
    convert_df(data_all.df_msg),
    "messages.csv",
    "text/csv",
    key='msg-data'
)
# st.write(gdata.df_msg)


st.markdown('## Muted People')
st.write(data_all.df_members.query('muted == True'))
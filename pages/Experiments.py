import streamlit as st
import datetime
from data_cleaning import data_all

d_start = st.date_input(
    "Enter Start Date",
    datetime.date(2019, 7, 6))

st.write('Your birthday is:', d_start)

def convert_df(df):
    return df.to_csv().encode('utf-8')


csv = convert_df(data_all.df_members)

st.download_button(
    "Press to Download",
    convert_df(data_all.df_members),
    "members.csv",
    "text/csv",
    key='browser-data'
)
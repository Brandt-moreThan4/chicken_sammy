import streamlit as st
import datetime

d_start = st.date_input(
    "Enter Start Date",
    datetime.date(2019, 7, 6))

st.write('Your birthday is:', d_start)


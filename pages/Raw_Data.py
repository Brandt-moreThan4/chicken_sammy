import streamlit as st
from data_cleaning import data


st.markdown('## Member Data')
st.write(data.df_members)

st.markdown('## MSG Data')
st.write(data.df_msg)


st.markdown('## Muted People')
st.write(data.df_members.query('muted == True'))
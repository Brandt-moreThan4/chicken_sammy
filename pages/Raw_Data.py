import streamlit as st
from data_cleaning import gdata


st.markdown('## Member Data')
st.write(gdata.df_members)

st.markdown('## MSG Data')
st.write(gdata.df_msg)


st.markdown('## Muted People')
st.write(gdata.df_members.query('muted == True'))

import streamlit as st
from data_cleaning import data_all



st.markdown('## Member Data')
st.write(data_all.df_members)

st.markdown('## MSG Data: (Bug here)')
# st.write(gdata.df_msg)


st.markdown('## Muted People')
st.write(data_all.df_members.query('muted == True'))
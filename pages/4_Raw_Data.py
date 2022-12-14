
from datetime import datetime
import streamlit as st
from data_cleaning import data_all
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder



def convert_df(df:pd.DataFrame):
    return df.to_csv().encode('utf-8')



st.markdown('## Member Data')

grid_options = GridOptionsBuilder.from_dataframe(data_all.df_members)
grid_options.configure_pagination(15)
grid_options = grid_options.build()
AgGrid(data_all.df_members,height=500,gridOptions=grid_options)

st.download_button(
    "Press to Download Member Data",
    convert_df(data_all.df_members),
    "members.csv",
    "text/csv",
    key='member-data'
)

st.markdown('## MSG Data')
st.download_button(
    "Press to Download Message Data",
    convert_df(data_all.df_msg),
    "messages.csv",
    "text/csv",
    key='msg-data'
)

# You have to do a copy of the df because AgGrid mutates the df inplace.
grid_options = GridOptionsBuilder.from_dataframe(data_all.df_msg.copy())
grid_options.configure_pagination(20)
grid_options = grid_options.build()
AgGrid(data_all.df_msg.copy(),height=500,gridOptions=grid_options)


st.markdown('## Muted People')
st.write(data_all.df_members.query('muted == True'))

print(f'Cleaning: {datetime.now()}')
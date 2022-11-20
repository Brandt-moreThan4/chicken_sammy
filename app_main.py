from pathlib import Path
import json
import pandas as pd
from datetime import datetime
from typing import List
import streamlit as st
import plotly.express as px

DATA_PATH = Path('data') / '53526472'
MESSAGE_PATH = DATA_PATH / 'message.json'
CONVO_PATH = DATA_PATH / 'conversation.json'

with MESSAGE_PATH.open(encoding='utf-8') as f:
    msg_data = json.load(f)
    df_data_msg = pd.DataFrame(msg_data)

with CONVO_PATH.open(encoding='utf-8') as f:
    convo_data:dict = json.load(f)
    # df_convo= pd.DataFrame(convo_data)
df_data_msg.head(2)
members:dict = convo_data['members']
df_members = pd.DataFrame(members)
df_members.head(3)
id_map:pd.Series = df_members[['user_id','name']].set_index('user_id')['name']
df_id_map = df_members[['user_id','name']]
# How many muted?
# df_members[df_members.muted == True]
# df_data_msg[df_data_msg.system]

def has_image(data:List[dict]) -> bool:
    contains_image = False   
    for dicky in data:
       if dicky['type'] == 'image':
           contains_image = True
    return contains_image
# Attachmeent ype?

# print(len(df_data_msg))
COLS_TO_KEEP = ['attachments', 'created_at', 'favorited_by', 'name',  'sender_type', 'system','text', 'user_id', 'event']
df = df_data_msg[COLS_TO_KEEP].copy()
df = df[df.system == False].copy() # Don't care about system messages for this analysis.
df['created_at'] = df.created_at.apply(datetime.utcfromtimestamp)
df['like_count'] = df.favorited_by.apply(len)
df['has_attachement'] = df.attachments.apply( lambda x: len(x) > 0)
df['attachement_num'] = df.attachments.apply( lambda x: len(x))
df['has_image'] = df.attachments.apply(has_image)
df['char_count'] = df.text.apply(lambda x: len(x) if not x is None else False )
df['date_month'] = pd.PeriodIndex(year=df['created_at'].dt.year,month=df['created_at'].dt.month,freq='M')
# Add date cols:

df = df.merge(df_members[['user_id','nickname','name']],on='user_id',validate='m:1',how='left')

COLS_TO_DROP = ['system']
df = df.drop(columns=COLS_TO_DROP)



d = df.groupby('name_y')['char_count'].mean().sort_values(ascending=False).to_frame().iloc[:10].reset_index()

fig = px.bar(d,x='name_y',y='char_count')

st.plotly_chart(fig)
st.write(d)
print('done')
from pathlib import Path
import json
import pandas as pd
from datetime import datetime
from typing import List
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit.components.v1 as components



class DataCalcs:
    def calculate_properties(self):
        self.member_count = len(self.members_data)
        self.msg_count = len(self.df_msg)
        self.member_names = self.df_members.name.unique().tolist()

    def most_liked_msg(self) -> pd.Series:
        return self.df_msg.sort_values('like_count').iloc[-1]


class DataWrangler(DataCalcs):
    DATA_PATH = Path('data') / '53526472'
    MESSAGE_PATH = DATA_PATH / 'message.json'
    CONVO_PATH = DATA_PATH / 'conversation.json'   
    ENCODING = 'utf-8'

    def __init__(self,load_data=True) -> None:
        if load_data:
            self.load_all_data()
        self.calculate_properties()

    def load_all_data(self):
        self.load_convo_data()
        self.load_message_data()
        self.clean_data()

    def calculate_properties(self):
        self.member_count = len(self.members_data)
        self.msg_count = len(self.df_msg)
        self.member_names = self.df_members.name.unique().tolist()


    def load_message_data(self):
        with self.MESSAGE_PATH.open(encoding=self.ENCODING) as f:
            self.msg_data:dict = json.load(f)
        
        self.df_data_msg = pd.DataFrame(self.msg_data)

    def load_convo_data(self):
        with self.CONVO_PATH.open(encoding=self.ENCODING) as f:
            self.convo_data:dict = json.load(f)
      
        self.members_data:dict = self.convo_data['members']
        self.df_members = pd.DataFrame(self.members_data).set_index('user_id')
        self.id_map:pd.Series = self.df_members['name']
        self.df_id_map = self.id_map.reset_index()

    def clean_data(self):

        MSG_COLS_TO_KEEP = ['attachments', 'created_at', 'favorited_by', 'name',  'sender_type', 'system','text', 'user_id', 'event']        
        df = self.df_data_msg[MSG_COLS_TO_KEEP].copy()
        df = df[df.system == False].copy() # Don't care about system messages for this analysis.
        df['created_at'] = df.created_at.apply(datetime.utcfromtimestamp)
        df['like_count'] = df.favorited_by.apply(len)
        df['has_attachement'] = df.attachments.apply( lambda x: len(x) > 0)
        df['attachement_num'] = df.attachments.apply( lambda x: len(x))
        df['has_image'] = df.attachments.apply(has_image)
        df['char_count'] = df.text.apply(lambda x: len(x) if not x is None else False )
        df['date_month'] = pd.PeriodIndex(year=df['created_at'].dt.year,month=df['created_at'].dt.month,freq='M')
        df = df.rename(columns={'name':'msg_name'}) # So we don't get it confused with the permanent name in convo data
        # Combine with member data:
        df = df.merge(self.df_members[['nickname','name']],left_on='user_id',right_index=True,validate='m:1',how='left')
        COLS_TO_DROP = ['system']
        df.drop(columns=COLS_TO_DROP)       

        self.df_msg = df




class PersonData(DataCalcs):
    def __init__(self,user_id:str,data_all:DataWrangler) -> None:
        self.user_id = user_id

        df_msg_all = data_all.df_msg
        self.df_msg = df_msg_all[df_msg_all.user_id == user_id]
        self.member_info = data_all.df_members[data_all.df_members.index == user_id]
        self.name = self.member_info.name
    



def has_image(data:List[dict]) -> bool:
    contains_image = False   
    for dicky in data:
       if dicky['type'] == 'image':
           contains_image = True
    return contains_image


gdata = DataWrangler()

person = PersonData('5994102',gdata)

print('lol')
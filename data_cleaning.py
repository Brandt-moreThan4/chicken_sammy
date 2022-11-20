from pathlib import Path
import json
import pandas as pd
from datetime import datetime
from typing import List
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt




class GroupMeData:
    DATA_PATH = Path('data') / '53526472'
    MESSAGE_PATH = DATA_PATH / 'message.json'
    CONVO_PATH = DATA_PATH / 'conversation.json'   
    ENCODING = 'utf-8'

    def __init__(self,load_data=True) -> None:
        self.msg_data = {}

        if load_data:
            self.load_all_data()

    def load_all_data(self):
        self.load_convo_data()
        self.load_message_data()
        self.clean_data()

        self.member_count = len(self.members_data)
        self.msg_count = len(self.df_msg)



    def load_message_data(self):
        with self.MESSAGE_PATH.open(encoding=self.ENCODING) as f:
            self.msg_data:dict = json.load(f)
        
        self.df_data_msg = pd.DataFrame(self.msg_data)

    def load_convo_data(self):
        with self.CONVO_PATH.open(encoding=self.ENCODING) as f:
            self.convo_data:dict = json.load(f)
      
        self.members_data:dict = self.convo_data['members']
        self.df_members = pd.DataFrame(self.members_data)
        self.id_map:pd.Series = self.df_members[['user_id','name']].set_index('user_id')['name']
        self.df_id_map = self.df_members[['user_id','name']]

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
        df = df.merge(self.df_members[['user_id','nickname','name']],on='user_id',validate='m:1',how='left')
        COLS_TO_DROP = ['system']
        df.drop(columns=COLS_TO_DROP)       

        self.df_msg = df

    # @property
    # def member_count(self) -> int:
    #     return len(self.members_data)

def has_image(data:List[dict]) -> bool:
    contains_image = False   
    for dicky in data:
       if dicky['type'] == 'image':
           contains_image = True
    return contains_image


gdata = GroupMeData()
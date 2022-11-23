from pathlib import Path
import json
import pandas as pd
from datetime import datetime
from typing import List
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
# import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import FreqDist



def has_image(data:List[dict]) -> bool:
    contains_image = False   
    for dicky in data:
       if dicky['type'] == 'image':
           contains_image = True
    return contains_image

class DataCalcs:
    def calculate_properties(self):
        self.member_count = len(self.members_data)
        self.msg_count = len(self.df_msg)
        self.member_names = self.df_members.name.unique().tolist()
        self.all_text = ''.join(self.df_msg.text)

    def most_liked_msg(self) -> "Message":
        return Message(self.df_msg.sort_values('like_count').iloc[-1])

    def most_liked_msgs(self,msg_num:int=5)-> list["Message"]:
        msg_num = min(msg_num,self.msg_count-1) # don't over-index
        df = self.df_msg.sort_values('like_count',ascending=False).iloc[:msg_num]
        return df.apply(Message,axis=1) # Convert to messages


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

        MSG_COLS_TO_KEEP = ['created_at','name','text','attachments', 'favorited_by', 'sender_type', 'system', 'user_id', 'event','id']        
        df = self.df_data_msg[MSG_COLS_TO_KEEP].copy()
        df = df[df.system == False].copy() # Don't care about system messages for this analysis.
        df = df[df.sender_type == 'user'].copy() # Only look at users
        df['created_at'] = df.created_at.apply(datetime.utcfromtimestamp)
        df['like_count'] = df.favorited_by.apply(len)
        df['has_attachement'] = df.attachments.apply( lambda x: len(x) > 0)
        df['attachement_num'] = df.attachments.apply( lambda x: len(x))
        df['has_image'] = df.attachments.apply(has_image)
        df['char_count'] = df.text.apply(lambda x: len(x) if not x is None else False )
        df['text'] = df['text'].fillna('')
        df['tokens'] = [word_tokenize(msg) for msg in df.text.array]
        # df['date_month'] = pd.PeriodIndex(year=df['created_at'].dt.year,month=df['created_at'].dt.month,freq='M')
        df = df.rename(columns={'name':'msg_name','id':'msg_id'}) # Be more explicit

        # Combine with member data:
        df = df.merge(self.df_members[['nickname','name']],left_on='user_id',right_index=True,validate='m:1',how='left')
        COLS_TO_DROP = ['system','sender_type']
        df = df.drop(columns=COLS_TO_DROP)       

        self.df_msg = df


gdata = DataWrangler()

class Person(DataCalcs):
    def __init__(self,user_id:str,data_all:DataWrangler=gdata) -> None:

        self.user_id = user_id
        self.all_data = data_all
        df_msg_all = data_all.df_msg
        self.df_msg = df_msg_all[df_msg_all.user_id == user_id]
        self.member_info = data_all.df_members[data_all.df_members.index == user_id]
        self.name = self.member_info.name
    

class Message:
    def __init__(self,row:pd.Series) -> None:
        self.text:str = row['text']

        self.created_at:datetime = row['created_at']
        self.sender_name: str = row['msg_name']
        self.sender_id:str = row['user_id']
        self.msg_id = row['msg_id']
        self.likes:int = row['like_count']
        self._permname:str = row['name']
        self.nickname:str = row['nickname']
        self.liked_by:List[str] = row['favorited_by']
        self.char_count:int = row['char_count']
        self.has_image:bool = row['has_image']
        self.attachments:list[Attachment] = [Attachment(data) for data in row['attachments']]

    @property
    def images(self) -> list["Attachment"]:
        return [attachment for attachment in self.attachments if attachment.is_image]

    def html_display(self) -> str:
        html_block = f'<div><p><b>{self.nickname}</b></p><i><q>{self.text}</q></i></div>'
        if self.has_image:
            # Grab the first image for now:
            img = self.images[0]
            img_html = f'''<div><img height="300" src="{img.image_url}" alt="Sammy Image"></div>'''

            html_block += img_html
        return html_block
            


class Attachment:
    def __init__(self,attachment:dict) -> None:
        self.data = attachment
        self.type:str = attachment['type']
        self.is_image:bool = False

        if self.type == 'image':
             self.is_image:bool = True
             self.image_url:str = attachment['url']
             self.image_id:str = self.extract_imag_id(self.image_url)

    @staticmethod
    def extract_imag_id(image_url:str) -> str:
        return image_url[(image_url.rfind('.')+1):]






person = Person('5994102',gdata)
msg = person.most_liked_msg()

print('lol')
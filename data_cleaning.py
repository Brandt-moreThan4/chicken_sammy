from pathlib import Path
import json
import pandas as pd
from datetime import datetime
import calendar
import spacy
from spacy.tokens import Token
import utils
from collections import Counter
import matplotlib.pyplot as plt

nlp = spacy.load('en_core_web_sm')


def has_image(data:list[dict]) -> bool:
    contains_image = False   
    for dicky in data:
       if dicky['type'] == 'image':
           contains_image = True
    return contains_image

def extract_imag_id(image_url:str) -> str:
    return image_url[(image_url.rfind('.')+1):]

class DataCalcs:

    def __init__(self) -> None:
        self.member_count = None
        self.msg_count = None
        self.member_names = None
        self.all_text = None
        self._cleaned_tokens =  None
        self._descriptive_tokens = None
        self._common_descriptive_words = None       
        self.avg_likes = None

    # def calculate_properties(self):
    #     self.member_count = len(self.members_data)
    #     self.msg_count = len(self.df_msg)
    #     self.member_names = self.df_members.name.unique().tolist()
    #     self.all_text = '. '.join(self.df_msg.text)

    def most_liked_msg(self) -> "Message":
        return Message(self.df_msg.sort_values('like_count').iloc[-1])

    def most_liked_msgs(self,msg_num:int=5)-> list["Message"]:
        msg_num = min(msg_num,self.msg_count-1) # don't over-index
        df = self.df_msg.sort_values('like_count',ascending=False).iloc[:msg_num]
        return df.apply(Message,axis=1) # Convert to messages

    def get_avg_likes(self) -> float:
        self.avg_likes = self.df_msg.like_count.mean()
        return self.avg_likes


    @property
    def cleaned_tokens(self) -> pd.DataFrame:
        if self._cleaned_tokens is None:
            self._cleaned_tokens = utils.get_cleaned_tokens(self.all_text)
        return self._cleaned_tokens        

    @property
    def descriptive_tokens(self) -> list[str]:
        if self._descriptive_tokens is None:
            self._descriptive_tokens = utils.get_descriptive_tokens(self.cleaned_tokens)
        return self._descriptive_tokens

    @property
    def common_descriptive_words(self) -> pd.DataFrame:
        if self._common_descriptive_words is None:
            self._common_descriptive_words = utils.get_most_common_words(self.descriptive_tokens)
        return self._common_descriptive_words

    def get_word_cloud(self):
        fig, ax = utils.get_word_cloud(tokens=self.descriptive_tokens)
        return (fig, ax)


class DataWrangler(DataCalcs):
    DATA_PATH = Path('data') / '53526472'
    MESSAGE_PATH = DATA_PATH / 'message.json'
    CONVO_PATH = DATA_PATH / 'conversation.json'   
    ENCODING = 'utf-8'

    def __init__(self,load_data=True) -> None:
        super().__init__()
        if load_data:
            self.load_all_data()
        self.member_count = len(self.members_data)
        self.msg_count = len(self.df_msg)
        self.member_names = self.df_members.name.unique().tolist()
        self.all_text = '. '.join(self.df_msg.text)

    def load_all_data(self):
        self.load_convo_data()
        self.load_message_data()
        self.clean_data()


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
        # df['tokens'] = [[(token.text) for token in nlp.tokenizer(msg)] for msg in df.text.array]
        df['date_month'] = df.created_at.dt.year.astype(str) + '-'+ df.created_at.dt.month.apply(lambda x: calendar.month_abbr[x])
        df = df.rename(columns={'name':'msg_name','id':'msg_id'}) # Be more explicit

        # Combine with member data:
        df = df.merge(self.df_members[['nickname','name']],left_on='user_id',right_index=True,validate='m:1',how='left')
        COLS_TO_DROP = ['system','sender_type']
        df = df.drop(columns=COLS_TO_DROP)       

        self.df_msg = df
        # Also want to save an version of the messages that has the favorite column exploded:
        self.df_msg_favs = df.explode('favorited_by')


data_all = DataWrangler()


class Person(DataCalcs):
    def __init__(self,user_id:str) -> None:
        super().__init__()
        self.user_id:str = user_id
        self.data_all:DataWrangler = data_all

        df_msg_all = data_all.df_msg
        self.df_msg:pd.DataFrame = df_msg_all[df_msg_all.user_id == user_id]

        member_info = data_all.df_members.loc[user_id]
        self.muted:bool = member_info['muted']
        self.nickname:str = member_info['nickname']
        self.name:str = member_info['name']
        self.image_url:str = member_info['image_url']
        self.image_id:str = extract_imag_id(self.image_url)
        self.first_msg_date:datetime = self.df_msg.created_at.min()

        # Grab the messages that belong to this person
        self.messages:list[Message] = list(filter(lambda msg: msg.sender_id == user_id,all_msgs))
        self.msg_count = len(self.messages)
        self.all_text = '. '.join(self.df_msg.text)   

    def __repr__(self) -> str:
        return f'{self.name}: {self.first_msg_date}'
      

    def get_most_liked_person(self):
        df_msg_favs = data_all.df_msg_favs
        self.most_liked =  Person(df_msg_favs[df_msg_favs.favorited_by == self.user_id].user_id.value_counts().index[0])
        return self.most_liked

    def get_biggest_admirer(self):
        df_msg_favs = data_all.df_msg_favs
        # All admirerers: df_msg_favs[df_msg_favs.user_id == self.user_id].favorited_by.value_counts().index[0]
        self.biggest_admirer = Person(df_msg_favs[df_msg_favs.user_id == self.user_id].favorited_by.value_counts().index[0])
        return self.biggest_admirer

    def html_display(self) -> str:
        html_block = (
            f'<h5>{self.nickname}</h5>'
            f'<img height="150" src="{self.image_url}" alt="Profile Image">'
        )

        return html_block
    

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
        self.liked_by:list[str] = row['favorited_by']
        self.char_count:int = row['char_count']
        self.has_image:bool = row['has_image']
        self.attachments:list[Attachment] = [Attachment(data) for data in row['attachments']]

    def __repr__(self) -> str:
        return f'{self.created_at} --{self.sender_name} -- {self.text}'

    @property
    def images(self) -> list["Attachment"]:
        return [attachment for attachment in self.attachments if attachment.is_image]

    def html_display(self) -> str:
        html_block = f'<div><p><b>{self.nickname}</b>: {self.created_at.date()}</p><i>{self.text}</i></div><br>'

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
             self.image_id:str = extract_imag_id(self.image_url)



all_msgs:list["Message"] = data_all.df_msg.apply(Message,axis=1).to_list()
all_people:list[Person] = [Person(user_id) for user_id in data_all.df_members.index]

hubbell = Person('5994102')
# hubbell.common_descriptive_words.iloc[:10]


# fig, ax = hubbell.get_word_cloud()
# plt.show()

print(f'Cleaning: {datetime.now()}')
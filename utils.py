'''To Do: AgBuilder function'''

import pandas as pd
import streamlit as st

def convert_df(df:pd.DataFrame):
    return df.to_csv().encode('utf-8')


def is_token_allowed(token):
     '''
         Only allow valid tokens which are not stop words
         and punctuation symbols.
     '''
     if (not token or not token.string.strip() or
         token.is_stop or token.is_punct):
         return False
     return True

def preprocess_token(token):
    # Reduce token to its lowercase lemma form
    return token.lemma_.strip().lower()


def write_spaces(space_number:int=1):
    for _ in range(space_number):
        st.write('')
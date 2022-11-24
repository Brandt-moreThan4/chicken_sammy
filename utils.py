'''To Do: AgBuilder function'''

import pandas as pd
import streamlit as st
import spacy
from spacy.tokens import Token
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

nlp = spacy.load('en_core_web_sm')

def convert_df(df:pd.DataFrame):
    return df.to_csv().encode('utf-8')

def write_spaces(space_number:int=1):
    for _ in range(space_number):
        st.write('')

def is_token_allowed(token:Token) -> bool:
    '''
        Only allow valid tokens which are not stop words, punctuation symbols, or spaces.
    '''

    if token.is_stop or token.is_punct or  token.is_space:
        return False
    else:
        return True


def get_cleaned_tokens(text:str) -> list[Token]:
    # Remove stop words and punctuation
    clean_tokens = [token for token in nlp(text) if is_token_allowed(token)]
    return clean_tokens

def get_descriptive_tokens(tokens:list[Token]) -> list[str]:
    '''Return only adjectives or adverbs from the token list. Also, convert them to lower cased, stripped strings.'''
    tags = ['ADJ','ADV']
    descriptive_tokens = [token.text.strip().lower() for token in tokens if token.pos_ in tags]
    return descriptive_tokens

def get_most_common_words(tokens:list[str]) -> pd.DataFrame:

    freq_adj = Counter(tokens)
    word_freqs = pd.DataFrame((freq_adj.most_common(len(freq_adj))),columns=['word','freq'])
    return word_freqs


def get_word_cloud(text:str=None,tokens:list[str]=None):
    '''Create a word cloud of the adjectives and adverbs from the input text. 
    ## Returns a pyplot (fig, ax)'''

    if tokens is not None:
        text = ' '.join(tokens)

    # Create the wordcloud object
    wordcloud = WordCloud(background_color = 'white',
                        width = 512,
                        height = 384
                            ).generate(text)

    fig, ax = plt.subplots()
    ax.imshow(wordcloud)
    ax.axis("off")
    ax.margins(x=0, y=0)
    return fig, ax
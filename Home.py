from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
from data_cleaning import data_all, word_freqs, tokens_adj
# import streamlit.components.v1 as components
text = ' '.join(tokens_adj)


INTRO_MD = '''
## A Chicken Sammy Adventure
##### *Boldly Going Where None Have Gone Before*
#
### Overview
 '''

st.markdown(INTRO_MD)

text = ' '.join(tokens_adj)

# Create the wordcloud object
wordcloud = WordCloud(background_color = 'white',
                    width = 512,
                    height = 384
                        ).generate(text)

fig, ax = plt.subplots()
ax.imshow(wordcloud)
ax.axis("off")
ax.margins(x=0, y=0)
# plt.show()
st.pyplot(fig)

df = data_all.df_msg

st.markdown('### Wordiest Individuals')
char_counts = df.groupby('name')['char_count'].mean().sort_values(ascending=False).to_frame().iloc[:15].reset_index()
fig1 = px.bar(char_counts,x='name',y='char_count')
st.plotly_chart(fig1)

st.markdown('### Most Messages')
msg_counts = df.groupby('name')['created_at'].count().sort_values(ascending=False).to_frame().iloc[:15].reset_index()
fig2 = px.bar(msg_counts,x='name',y='created_at')
st.plotly_chart(fig2)

st.markdown('### Hall of Fame: Most Liked Messages')
msg_num = st.number_input("**Select the number of most-liked messages you want to see:**",1,10,3)
msgs = data_all.most_liked_msgs(msg_num)

for msg in msgs:
    st.markdown(msg.html_display(),unsafe_allow_html=True)
    st.markdown('<hr>',unsafe_allow_html=True)


print(f'Home: {datetime.now()}')
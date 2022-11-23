import streamlit as st
from data_cleaning import gdata, Person
import pandas as pd
import streamlit.components.v1 as components


st.markdown('### Individual Analysis')

members = sorted(gdata.member_names)
members.remove('.') # It makes the UI look back.
name_select = st.selectbox('Who who you like to get deep into?',members)

st.write('Excellent choice, you selected', name_select)

user_id = gdata.id_map[gdata.id_map == name_select].index[0]
person = Person(user_id,gdata)

st.markdown('#### Basic Stats')
# Active Since
# Message Count
# yata yata
st.markdown("#### Your Most Liked Message")
msg = person.most_liked_msg()
msg_text = f'<i><q>{msg.text}</q></i>'
components.html(msg_text,scrolling=True,height=150)
if msg.has_image:
    # Grab the first image for now:
    img = msg.images[0]
    img_html = f''' <img height="300" src="{img.image_url}" alt="Sammy Image"> '''
    components.html(img_html,height=300)

# st.write(msg.text)
# st.info(msg.text)
# st.success(msg.text)

# st.write(msg.to_frame())

st.markdown('#### Your most liked person')
st.markdown('#### Person who likes you the most')
st.markdown('#### ')
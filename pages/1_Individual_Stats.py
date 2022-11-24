import streamlit as st
from data_cleaning import data_all, Person
import pandas as pd
import streamlit.components.v1 as components


st.markdown('### Individual Analysis')

members = sorted(data_all.member_names)
members.remove('.') # It makes the UI look back.
name_select = st.selectbox('Who who you like to get deep into?',members)

user_id = data_all.id_map[data_all.id_map == name_select].index[0]
person = Person(user_id)
components.html(person.html_display(),height=200)

st.markdown('#### Basic Stats')
# Active Since
# Message Count
# yata yata

st.markdown("#### Your Most Liked Message")
msg = person.most_liked_msg()
st.markdown(msg.html_display(),unsafe_allow_html=True)
# st.markdown('<hr>',unsafe_allow_html=True)



st.markdown('#### Your most liked person')
components.html(person.get_most_liked_person().html_display(),height=200)

st.markdown('#### Person who likes you the most')
components.html(person.get_biggest_admirer().html_display(),height=200)

st.markdown("#### See All Messages")
st.markdown("#### See Top N Messages")
msg_number = st.number_input("Select the number of most-liked Messages you want to see:",1,10)

most_liked_msgs = person.most_liked_msgs(msg_number)
for msg in most_liked_msgs:
    st.markdown(msg.html_display(),unsafe_allow_html=True)
    st.markdown('<hr>',unsafe_allow_html=True)

st.markdown('#### ')
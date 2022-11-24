from datetime import datetime
import streamlit as st
from data_cleaning import data_all, Person
import pandas as pd
import utils


st.markdown('### Individual Analysis')

members = sorted(data_all.member_names)
members.remove('.') # It makes the UI look back.
name_select = st.selectbox('Who who you like to get **deep** into?',members,index=members.index('Stallion Green'))

user_id = data_all.id_map[data_all.id_map == name_select].index[0]
person = Person(user_id)
st.markdown(person.html_display(),unsafe_allow_html=True)
utils.write_spaces(1)

st.markdown('#### Basic Stats')

cols = st.columns(3)

cols[0].metric(label="Active Since", value=str(person.first_msg_date.date()))
cols[1].metric(label="Number of Messages", value=person.msg_count)
cols[2].metric(label="Average Likes Per Message", value=round(person.get_avg_likes(),2))

# st.markdown('##### Most Commonly Used Words')
# st.write(person.common_descriptive_words.iloc[:10])
fig, ax = person.get_word_cloud()
st.pyplot(fig)

utils.write_spaces(2)


st.markdown("#### Your Most Liked Message")
msg = person.most_liked_msg()
st.markdown(msg.html_display(),unsafe_allow_html=True)
utils.write_spaces(1)


st.markdown('#### Your most liked person')
st.markdown(person.get_most_liked_person().html_display(),unsafe_allow_html=True)
utils.write_spaces(2)

st.markdown('#### Person who likes you the most')
st.markdown(person.get_biggest_admirer().html_display(),unsafe_allow_html=True)
utils.write_spaces(2)


st.markdown("#### See Top Messages")
msg_number = st.number_input("Select the number of most-liked Messages you want to see:",1,10)

most_liked_msgs = person.most_liked_msgs(msg_number)
for msg in most_liked_msgs:
    st.markdown(msg.html_display(),unsafe_allow_html=True)
    st.markdown('<hr>',unsafe_allow_html=True)

st.markdown('#### ')


st.markdown("#### See All Messages?")
show_all:bool = st.checkbox('Show All Messages')
if show_all:
    for msg in person.messages:
        st.markdown(msg.html_display(),unsafe_allow_html=True)
        st.markdown('<hr>',unsafe_allow_html=True)


print(f'Cleaning: {datetime.now()}')
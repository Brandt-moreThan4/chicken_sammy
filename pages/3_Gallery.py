from datetime import datetime
import streamlit as st
from PIL import Image


st.markdown('## Coming Soon')
st.markdown('#### A Small Taste:')

# components.html('<img height="300" src="sammy_icon2.png" alt="Sammy Image">',height=300)
st.image(Image.open('sammy_icon2.png'))


st.markdown('#### Upload your own')
uploaded_file = st.file_uploader("Choose a file")

st.markdown('#### Take your own')
picture = st.camera_input("Take a picture")

if picture:
    st.image(picture)

print(f'Cleaning: {datetime.now()}')
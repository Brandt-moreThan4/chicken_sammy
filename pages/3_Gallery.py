from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components


st.markdown('## Coming Soon')
st.markdown('#### A Small Taste:')

components.html('<img height="300" src="https://github.com/Brandt-moreThan4/chicken_sammy/blob/v2/data/sample_images/156842797118905542_1200x1200.437da0a46bc84c24a4e5a359e3fe071c.jpeg?raw=true" alt="Sammy Image">',height=300)


st.markdown('#### Upload your own')
uploaded_file = st.file_uploader("Choose a file")

st.markdown('#### Take your own')
picture = st.camera_input("Take a picture")

if picture:
    st.image(picture)

print(f'Cleaning: {datetime.now()}')
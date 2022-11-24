import streamlit as st
import utils

st.markdown("### Let's find the best sammy for you  ")
utils.write_spaces(2)


with st.form("my_form"):
    st.markdown("##### Recommendation Inputs")
    input_msg = 'Please input some of the features you are looking for in a Sammy. Separeted by semicolons:'
    default_features = 'spicy; wet; thick'
    desired_features = st.text_input(input_msg,default_features)

   # Every form must have a submit button.
    submitted = st.form_submit_button("Generate Recommendation")

if submitted:
    st.markdown("#### Recommended Sammys")
    st.write("Haven't figured out how to do this yet...")

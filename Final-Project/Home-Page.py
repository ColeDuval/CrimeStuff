import streamlit as st
import pandas as pd
import csv as csv
import numpy as np
import pydeck as pdk
import random as rd
from PIL import Image

st.set_page_config(
    page_title="Home Page",
    page_icon="Final-Project/Icons/blobfish.png",
)
pagestyle = '''
<style>
[data-testid="stAppViewContainer"] {
background-color: #ffffff;
opacity: 0.8;
background-image:  linear-gradient(135deg, #ffe2e2 25%, transparent 25%), linear-gradient(225deg, #ffe2e2 25%, transparent 25%), linear-gradient(45deg, #ffe2e2 25%, transparent 25%), linear-gradient(315deg, #ffe2e2 25%, #ffffff 25%);
background-position:  10px 0, 10px 0, 0 0, 0 0;
background-size: 10px 10px;
background-repeat: repeat;
}
[data-testid="stHeader"] {
background-color: rgba(0,0,0,0);
}
[data-testid="stSidebar"] {
background-color: #FFB2B2;
}
}
</style>
'''
st.markdown(pagestyle, unsafe_allow_html=True)  # Sets The overall styling for the website by injecting CSS
st.title('Welcome to My Website!')  # Prints a title
st.subheader('What is the purpose of this website?')  # Prints a header
st.write('the purpose of this website is to use and analyze Boston police crime data and display it to the end user of this website in a interactive fashion, to this end add this website consists of three different pages each with its own unique function and  way to interact with the data.')
st.subheader('A Little Bit About Me') # Prints a header
st.write('My name is Cole Duval Im currently 21 years old and I currently go to Bentley  university studying to get my undergraduate in computer information systems. I am on the cross country team at Bentley and Im also in several clubs I love getting outside and being active and my favorite activities include running coding and playing the guitar. ')
st.image('Final-Project/Icons/IMG_9903.jpg', caption='a picture of me',width=200) # shows an image of me
tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
   st.header("A cat")
   st.write("https://coleduval-crimestuff-final-projectpagespivot-table-llxeb1.streamlit.app/")

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

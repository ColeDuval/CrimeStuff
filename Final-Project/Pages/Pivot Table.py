import streamlit as st
import pandas as pd
import csv as csv
import numpy as np
from matplotlib import pyplot as plt
import random as rd
st.set_page_config(
    page_title="Pivot Tables",
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
st.markdown(pagestyle, unsafe_allow_html=True)
file = open(r'C:\Users\Cole\PycharmProjects\pythonProject\Final-Project\BostonCrime2021_7000_sample.csv')  # Opens crime data file
namefile = open(r'C:\Users\Cole\PycharmProjects\pythonProject\Final-Project\Pages\BostonPoliceDistricts.csv')  # Opens District name File
frame = pd.read_csv(file)  # Reads the Crime File
namelist = []  # Makes a name list
namedic = {}  # Makes a name dictionary
nameframe = pd.read_csv(namefile)  # Reads the name file
x = 0  # Sets a counter value
range = range(0,len(nameframe.District))  # Sets a range for all the districts in the name frame
for row in nameframe.District:
    name = nameframe.loc[(nameframe['District'] == row),['District_Name']]  # sets name equal to the district name
    for b in range:
        name = str(name).replace(str('District_Name'),'')  # gets rid of the string District_Name
        if name.find(str(b)) > 0:  # for where find b is grater than 0
            namedic[row] = str(name).replace(str(b),'')  # remove b from the string name
for i in frame.DISTRICT:
    if i not in namedic:
            namelist.append('Unspecified')  # sets the value of Unspecified for rows without a district
    else:
        for d in namedic:
            if d == i:
               namelist.append(namedic[d])  # adds the district name for rows that have a district
frame['District_Name'] = namelist  # creates a new colum that has the district names for each row in the frame
crimetypes = []
for i in frame.OFFENSE_DESCRIPTION:  # make a list of all crime names
    if i not in crimetypes:
        crimetypes.append(i)
district = []
for i in frame.District_Name:  # make a list of all distract names
    if i not in district:
        district.append(i)
with st.sidebar:  # makes a sidebar with two multiselect fields
    options = st.multiselect('What are the Crimes you want to see',crimetypes)
    options1 = st.multiselect('Where Crimes you want to see',district)

st.title("Pivot Table Example")
if len(options1) != 0 and len(options) != 0:
    crimeinbostoncomplex = frame.loc[frame.lat != 0][frame.lon != 0][frame.OFFENSE_DESCRIPTION.isin(options)][frame.District_Name.isin(options1)][['INCIDENT_NUMBER','MONTH','District_Name']]  # filters data and returns these columns
    piv1 = (np.round(pd.pivot_table(crimeinbostoncomplex, values='INCIDENT_NUMBER',
                                    index=['MONTH'],
                                    columns=['District_Name'],
                                    aggfunc='count', fill_value=0),2))  # makes a  pivot table
    fig2 = plt.figure(figsize=(15,8))
    ax1 = fig2.add_axes([0.1,0.1,.8,0.8])
    month = [1,2,3,4,5,6]
    x = 0

    for i in options1:
        plt.plot(month,piv1[i])  # plots the table
        x = x + 1
    plt.title("Crimes per Month by District Line Chart:")
    plt.xlabel("Month")
    plt.ylabel("Number of Crimes")
    plt.legend(labels = options1, loc = 'upper right')
    st.header('Pivot Table Graph:')
    st.pyplot(fig2)  # plots the graph
    st.subheader('what does this graph show?')
    st.write('This graph created by using a pivot table maps the total number of crimes per month for each district giving the user the option to pick what crimes they want to see as well as what districts they would like to see')
    piv2 = (np.round(pd.pivot_table(crimeinbostoncomplex, values='INCIDENT_NUMBER',
                                    index=['MONTH'],
                                    columns=['District_Name'],
                                    aggfunc='count', fill_value=0),2))
    st.header('Pivot Table:')
    st.write(piv2)
    st.subheader('what does this pivot table show?')
    st.write('the graph above is created using the data within this pivot table, which itself can be manipulated by the user depending on the inputs that they decide to select.')
else:
    st.write('please input values')

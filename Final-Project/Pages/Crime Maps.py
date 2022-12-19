import streamlit as st
import pandas as pd
import csv as csv
import numpy as np
import pydeck as pdk
import random as rd

st.set_page_config(
    page_title="Crime Maps",
    page_icon="Final-Project/Icons/icons8-map-marker-50.png",
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
st.markdown(pagestyle, unsafe_allow_html=True)  # Sets the styling of the page
file = open(r'C:\Users\Cole\PycharmProjects\pythonProject\Final-Project\BostonCrime2021_7000_sample.csv')
namefile = open(r'C:\Users\Cole\PycharmProjects\pythonProject\Final-Project\Pages\BostonPoliceDistricts.csv')
frame = pd.read_csv(file)  # Opens the crime data
nameframe = pd.read_csv(namefile)  # Opens the name data
crimetypes = []
sub_df_list =[]
layer_list =[]
namelist = []
namedic = {}
x = 0
range = range(0,len(nameframe.District))
for row in nameframe.District:  # Sets a range for all the districts in the name frame
    name = nameframe.loc[(nameframe['District'] == row),['District_Name']] # sets name equal to the district name
    for b in range:
        name = str(name).replace(str('District_Name'),'')  # gets rid of the string District_Name
        if name.find(str(b)) > 0:  # for where find b is grater than 0
            namedic[row] = str(name).replace(str(b),'')  # remove b from the string name
for i in frame.DISTRICT:
    if i not in namedic:
            namelist.append('Unspecified')  # sets the value of Unspecified for rows without a district
    else:
        for d in namedic:  # adds the district name for rows that have a district
            if d == i:
               namelist.append(namedic[d])
frame['District_Name'] = namelist # creates a new colum that has the district names for each row in the frame
for i in frame.OFFENSE_DESCRIPTION:
    if i not in crimetypes:
        crimetypes.append(i)
print(crimetypes)
district = []
for i in frame.District_Name:
    if i not in district:
        district.append(i)
with st.sidebar: # create a sidebar that has a select box that depending on what is selected will show different types of criteria which will be used to sort the data which will then be shown in the maps
    options3 = st.selectbox(
    'How would you like to be contacted?',
    ('Type', 'District', 'Type and District'))
    if options3 == 'Type':
        options = st.multiselect('What are the Crimes you want to see',crimetypes)
    elif options3 == 'District':
        options1 = st.multiselect('Where Crimes you want to see',district)
    else:
        options1 = st.multiselect('Where Crimes you want to see',district)
        options = st.multiselect('What are the Crimes you want to see',crimetypes)
diclist = {}
x = 0
for i in frame.DISTRICT:
    if i not in diclist:
        diclist[i] = x
        x = x + 1
view_state = pdk.ViewState(
                latitude=42.3601,
                longitude=-71.0589,
                zoom=11,
                pitch=0,)  # Create an initial view state for all the maps
if options3 == 'Type': # if the user selects type
    crimeinbostonbasic = frame.loc[frame.lat != 0][frame.lon != 0][frame.OFFENSE_DESCRIPTION.isin(options)][['lat','lon']]
    st.title("Crimes by Type")
    st.header('Hexagon Map')
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/outdoors-v11',
        initial_view_state=pdk.ViewState(
            latitude=42.3601,
            longitude=-71.0589,
            zoom=11,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
               'HexagonLayer',
               data=crimeinbostonbasic,
               get_position='[lon, lat]',
               radius=200,
               elevation_scale=4,
               elevation_range=[0, 1000],
               pickable=True,
               extruded=True,
            ),

            pdk.Layer(
                'ScatterplotLayer',
                data=crimeinbostonbasic,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
                pickable=True,
            ),
        ],))
    for i in options:
        subframe = frame.loc[(frame['lat'] != 0)&(frame['lon'] != 0)&(frame['OFFENSE_DESCRIPTION'] == i),['OFFENSE_DESCRIPTION','lon','lat']]
        sub_df_list.append(subframe)
    for sub_df in sub_df_list:  # makes a sub layer of the map that contains all of the information on a specific type of crime that is committed returning the type of crime and the longitude and latitude which then can be used to create sublayers of the map which then will be used to plot each of these sub layers and label them according to their respective crime types
        layer = pdk.Layer(type = 'ScatterplotLayer',
                      data=sub_df,
                      get_position='[lon, lat]',
                      get_radius=300,
                        get_color=[rd.randint(0,255),rd.randint(0,255),rd.randint(0,255)],
                      pickable=True
                      )
        layer_list.append(layer)
    tool_tip = {"html": "Crime Name:<br/> <b>{OFFENSE_DESCRIPTION}</b> <br/></b>",
            "style": { "backgroundColor": "orange",
                        "color": "white"}
          }
    map = pdk.Deck(
                map_style='mapbox://styles/mapbox/outdoors-v11',
                initial_view_state=view_state,
                layers=[layer_list[0:]],
                tooltip = tool_tip
                        )
    st.subheader('What does this map show?')
    st.write('This map shows which areas have the highest frequency of crimes by not only plotting 2D dots but also plotting 3D figures depending on the frequency of crimes within that specific area.')
    st.header('Sorted Map')
    st.pydeck_chart(map) #prints the map to streamlit
    st.subheader('What does this map show?')
    st.write('This map, as the name suggests, sorts all of the crimes and plots them based on the criteria specified by the user-specified, in this case, the type of crime being committed. It not only plots these points with different colors depending on the type of crime, but it also labels them so that when the user hovers over each point, it will give the type of crime that was committed.')
    for i in options: # makes lists of evrey data pint used in the map and displays them by type
        if len(frame.loc[(frame['lat'] != 0)&(frame['lon'] != 0)&(frame['OFFENSE_DESCRIPTION'] == i),['OFFENSE_DESCRIPTION','DISTRICT','lat','lon']] != 0):
            st.header(i)
            newframe = frame.loc[(frame['lat'] != 0)&(frame['lon'] != 0)&(frame['OFFENSE_DESCRIPTION'] == i),['OFFENSE_DESCRIPTION','DISTRICT','lat','lon']]
            st.write(newframe)
if options3 == "District":
    crimeinbostonbasic1 = frame.loc[frame.lat != 0][frame.lon != 0][frame.District_Name.isin(options1)][['lat','lon']]
    st.title("Crimes by District")
    st.subheader('Hexagon Map')
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/outdoors-v11',
        initial_view_state=pdk.ViewState(
            latitude=42.3601,
            longitude=-71.0589,
            zoom=11,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
               'HexagonLayer',
               data=crimeinbostonbasic1,
               get_position='[lon, lat]',
               radius=200,
               elevation_scale=4,
               elevation_range=[0, 1000],
               pickable=True,
               extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=crimeinbostonbasic1,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],))  # makes a Hexagon map for the data selected
    for i in options1:
            subframe = frame.loc[(frame['lat'] != 0)&(frame['lon'] != 0)&(frame['District_Name'] == i),['District_Name','lon','lat']]
            sub_df_list.append(subframe)
    for sub_df in sub_df_list: # makes a sub layer of the map that contains all of the information on a specific district that the crime is committed returning the district and the longitude and latitude which then can be used to create sublayers of the map which then will be used to plot each of these sub layers and label them according to their respective district
        layer = pdk.Layer(type = 'ScatterplotLayer',
                      data=sub_df,
                      get_position='[lon, lat]',
                      get_radius=300,
                        get_color=[rd.randint(0,255),rd.randint(0,255),rd.randint(0,255)],
                      pickable=True
                      )
        layer_list.append(layer)
    view_state = pdk.ViewState(
                latitude=42.3601,
                longitude=-71.0589,
                zoom=11,
                pitch=0,)
    tool_tip = {"html": "District Name:<br/> <b>{District_Name}</b> <br/></b>",
                "style": { "backgroundColor": "orange",
                            "color": "white"}
              }
    map = pdk.Deck(
            map_style='mapbox://styles/mapbox/outdoors-v11',
            initial_view_state=view_state,
            layers=[layer_list[0:]],
            tooltip = tool_tip
                    )
    st.subheader('What does this map show?')
    st.write('This map shows which areas have the highest frequency of crimes by not only plotting 2D dots but also plotting 3D figures depending on the frequency of crimes within that specific area.')
    st.header('Sorted Map')
    st.pydeck_chart(map)
    st.subheader('What does this map show?')
    st.write('This map, as the name suggests, sorts all of the crimes and plots them based on the criteria specified by the user-specified, in this case, the district it was committed in. It not only plots these points with different colors depending on the district, but it also labels them so that when the user hovers over each point, it will give the district that the crime was committed in.')
    for i in options1: # shoes frames of the selected data by district
        if len(frame.loc[(frame['lat'] != 0)&(frame['lon'] != 0)&(frame['District_Name'] == i),['OFFENSE_DESCRIPTION','District_Name','lat','lon']] != 0):
            st.header(i)
            newframe = frame.loc[(frame['lat'] != 0)&(frame['lon'] != 0)&(frame['District_Name'] == i),['OFFENSE_DESCRIPTION','District_Name','lat','lon']]
            st.write(newframe)
elif options3 == "Type and District":
    crimeinbostoncomplex = frame.loc[frame.lat != 0][frame.lon != 0][frame.OFFENSE_DESCRIPTION.isin(options)][frame.District_Name.isin(options1)][['lat','lon']]
    st.title("Crimes by Type and District")
    st.subheader('Hexagon Map')
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/outdoors-v11',
        initial_view_state=pdk.ViewState(
            latitude=42.3601,
            longitude=-71.0589,
            zoom=11,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
               'HexagonLayer',
               data=crimeinbostoncomplex,
               get_position='[lon, lat]',
               radius=200,
               elevation_scale=4,
               elevation_range=[0, 1000],
               pickable=True,
               extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=crimeinbostoncomplex,
                get_position='[lon, lat]',
                get_color='[200, 40, 0, 160]',
                get_radius=200,
            ),
        ],))  # makes a Hexagon map for the data selected
    for i in options:
        for x in options1:
                subframe = frame.loc[(frame['lat'] != 0)&(frame['lon'] != 0)&(frame['OFFENSE_DESCRIPTION']==i)&(frame['District_Name'] == x),['OFFENSE_DESCRIPTION','District_Name','lon','lat']]
                sub_df_list.append(subframe)
    for sub_df in sub_df_list: # makes a sub layer of the map that contains all of the information on a specific district that the crime is committed and the crime type returning the district, crimetype the longitude and latitude which then can be used to create sublayers of the map which then will be used to plot each of these sub layers and label them according to their respective district and crime type
        layer = pdk.Layer(type = 'ScatterplotLayer',
                      data=sub_df,
                      get_position='[lon, lat]',
                      get_radius=300,
                        get_color=[rd.randint(0,255),rd.randint(0,255),rd.randint(0,255)],
                      pickable=True
                      )
        layer_list.append(layer)
    view_state = pdk.ViewState(
                latitude=42.3601,
                longitude=-71.0589,
                zoom=11,
                pitch=0,)
    tool_tip = {"html": "District Name:<br/> <b>{District_Name}</b><br/>Offense Description: <br/> <b>{OFFENSE_DESCRIPTION}</b>",
                "style": { "backgroundColor": "orange",
                            "color": "white"}
              }
    map = pdk.Deck(
            map_style='mapbox://styles/mapbox/outdoors-v11',
            initial_view_state=view_state,
            layers=[layer_list[0:]],
            tooltip = tool_tip
                    )
    st.subheader('What does this map show?')
    st.write('This map shows which areas have the highest frequency of crimes by not only plotting 2D dots but also plotting 3D figures depending on the frequency of crimes within that specific area.')
    st.header('Sorted Map')
    st.pydeck_chart(map)
    st.subheader('What does this map show?')
    st.write('This map, as the name suggests, sorts all of the crimes and plots them based on the criteria specified by the user-specified, in this case, the type of crime being committed and the district it was committed in. It not only plots these points with different colors depending on the type of crime and district, but it also labels them so that when the user hovers over each point, it will give the type of crime and the district that was committed in.')
    for i in options:  # shows frames of the data sorted by crime type and district
        if len(frame.loc[(frame['lat'] != 0)&(frame['lon'] != 0)&(frame['OFFENSE_DESCRIPTION'] == i),['OFFENSE_DESCRIPTION','District_Name','lat','lon']] != 0):
            st.header(i)
        for x in options1:
            if len(frame.loc[(frame['lat'] != 0)&(frame['lon'] != 0)&(frame['District_Name'] == x)&(frame['OFFENSE_DESCRIPTION'] == i),['OFFENSE_DESCRIPTION','District_Name','lat','lon']] != 0):
                st.subheader(x)
                newframe = frame.loc[(frame['lat'] != 0)&(frame['lon'] != 0)&(frame['District_Name'] == x)&(frame['OFFENSE_DESCRIPTION'] == i),['OFFENSE_DESCRIPTION','District_Name','lat','lon']]
                st.write(newframe)


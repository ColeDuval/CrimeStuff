import streamlit as st
import pandas as pd
import csv as csv
import numpy as np
from matplotlib import pyplot as plt


st.set_page_config(
    page_title="Crime Charts",
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
list = []
file = open(r'C:\Users\Cole\PycharmProjects\pythonProject\Final-Project\BostonCrime2021_7000_sample.csv')
frame = pd.read_csv(file)
def time(frame,x, y):  # defines the time functoin
    frame.sort_values('HOUR',ascending=True)
    poggers = frame["HOUR"].value_counts()
    return poggers
with st.sidebar:
    timeframe = st.slider("Pick Your Time Frame", 0, 24, (0, 24))
    x = timeframe[0]
    y = timeframe[1]
    pog = time(frame,x,y)
    def listmaker(value, num1, num2, type = 'l'):  # defines the listmaker function
        labelist = []
        sizelist = []
        if type == 'l':
            for i in range(num1,num2):
                hours = {0:'1 AM',1:'2 AM',2:'3 AM',3:'4 AM',4:'5 AM',5:'6 AM',6:'7 AM',7:'8 AM',8:'9 AM',9:'10 AM',10:'11 AM',11:'12 PM',12:'1 PM',13:'2 PM',14:'3 PM',15:'4 PM',16:'5 PM',17:'6 PM',18:'7 PM',19:'8 PM',20:'9 PM',21:'10 PM',22:'11 PM',23:'12 AM',}
                labelist.append(hours[i]) # make a list of hours
            return labelist
        elif type == 's':
            for i in range(num1,num2):
                sizelist.append(value[i]) # makes a list of counts
            return sizelist
labelist = listmaker(pog,x,y,'l')  # make a list of the labels
sizelist = listmaker(pog,x,y,'s')  # make a list of the counts

fig = plt.figure(figsize=(12,12),linewidth=10, edgecolor="#31333F",facecolor="#ffe2e2")
ax1 = fig.add_axes([0.1,0.1,.8,0.8])
ax1 = plt.pie(sizelist,  labels=labelist, autopct='%1.1f%%',
        shadow=True, startangle=90)  # makes a pie chart
st.title("Crimes committed within a range of Time:")
st.header("Pie Chart:")
st.pyplot(fig)  # plots the pie chart
fig1 = plt.figure(figsize=(15,8),linewidth=10,edgecolor="#31333F",facecolor="#ffe2e2")
ax1 = fig1.add_axes([0.1,0.1,.8,0.8])
x = np.arange(len(labelist))
plt.xticks(x, labelist)
st.subheader('What does this chart show?')
st.write('This pie chart represents the percent of total crimes each hour accounts for within the range of hours selected by the user.')
st.subheader('Possible Uses?')
st.write('Through this pie chart, we are able to see which hours of the day have the most crimes committed within them this piece of information is very insightful especially for law enforcement agencies because it helps them meet the demand for officers during hours that have the highest the number of crimes being committed')
st.header("Bar Chart:")
ax2 = plt.bar(height=sizelist,x = labelist)  # makes a bar chart
plt.xlabel("Time of Day")
plt.ylabel("Number of Crimes")
st.pyplot(fig1)  # plots a bar chart
x = 0
agsize = []
for i in sizelist:
    x = x + i
    agsize.append(x)
avgvale = []
x = 0
y = 1
for i in agsize:
    x = i+x
    avgvale.append(x/y)
    y = y + 1
fig2 = plt.figure(figsize=(15,8),linewidth=10,edgecolor="#31333F",facecolor="#ffe2e2")
ax1 = fig2.add_axes([0.1,0.1,.8,0.8])
plt.plot(labelist,agsize,color = 'red')  # make a line
plt.plot(labelist,avgvale,color = 'green') # make a line
st.subheader('What does this chart show?')
st.write('This bar chart is a visual representation of the total count of crimes committed within each hour of the day within the range of hours selected by the end user.')
st.subheader('Possible Uses?')
st.write('Again much like the pie chart the bar chart shows which hours of the day have the most crimes committed within them furthermore it also shows the hours of the day that have the least amount of crimes committed in them both of these pieces of information along with the trend it shows are both extremely informative pieces of information.')
st.subheader("Line Chart:")
plt.xlabel("Time of Day")
plt.ylabel("Number of Crimes")
plt.legend(labels = ['Total Crimes', 'Total Avrage Crimes'])
st.pyplot(fig2)  # graphs the lines
st.subheader('What does this chart show?')
st.write('This line plot shows two different lines the line in red represents the total aggregated number of crimes for each hour of the range specified by the end user the second line in green represents the average total crimes committed within the range specified by the user.')
st.subheader('Possible Uses?')
st.write('By looking at the total crimes line we can see the rate at which the total number of crimes Is changing the steeper the slope the higher change in the number of crimes per hour. Furthermore we can see that on average the average number of total crimes is increasing due to the fact that the total amount of crime is increasing which causes the total average crimes per hour to increase as well.')


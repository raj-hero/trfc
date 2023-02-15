# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


st.title('Dynamic PCU estimation - Group5')

# # Importing the raw data

st.header('The input data provided')
df = pd.read_excel('/Users/bikulborthakur/Downloads/submission/traffic_data.xlsx')
df

#df.columns

new_df = df.copy()

df.drop(df.columns.difference(['Lane', 'Vehicle Type', 'Entry time', 'Exit time', 'Duration']), 1, inplace=True)
#df

df.dropna(inplace=True)
#df
st.header('Finding the Gap')
df['Gap'] = np.nan
for i in range(len(df)):
    if 300*(i+1) <=26100:
        df['Gap'][i] = 300*(i+1)
df

# # FINDING ENTRY AND EXIT FLOW TOTAL AND INTERVAL WISE
st.header('Finding speed')

df['Speed'] = (62/df['Duration'])*18/5
df

st.header('Finding the Cummulative entry flow')
df['Cumulative entry flow'] = 0
for i in range(87):
    for j in range(len(df)):
        if df['Entry time'][j] <= df['Gap'][i]:
           df['Cumulative entry flow'][i] = df['Cumulative entry flow'][i]+1
df    

st.header('Finding the Cummulative exit flow')
df['Cumulative exit flow'] = 0
for i in range(87):
    for j in range(len(df)):
        if df['Exit time'][j] <= df['Gap'][i]:
           df['Cumulative exit flow'][i] = df['Cumulative exit flow'][i]+1
df

st.header('Finding the entry flow interval')
df['entry flow interval'] = df['Cumulative entry flow'].shift(0).diff()
df['entry flow interval'][0] = 52
df

st.header('Finding the exit flow interval')
df['exit flow interval'] = df['Cumulative exit flow'].shift(0).diff()
df['exit flow interval'][0] = 49
df

# # SMS Calculation

st.header('Finding travel time in 1 min')
df['Travel time in 1 min'] = 0.0
for i in range(87):
    for j in range(len(df)):
        if df['Exit time'][j] <= df['Gap'][i]:
           df['Travel time in 1 min'][i] = df['Travel time in 1 min'][i]+df['Duration'][j]
        else:
            break
df

st.header("Finding travel time interval wise")
df['Travel time interval wise'] = df['Travel time in 1 min'].shift(0).diff()
df['Travel time interval wise'][0] = df['Travel time in 1 min'][0]
df

st.header('Finding the average travel time in 1 min')
df['Average travel time every 1 min'] = df['Travel time interval wise']/df['exit flow interval']
df

st.header('Finding the Space Mean Speed')
df['SMS'] = (62/df['Average travel time every 1 min'])*18/5
df

st.header('Finding the Exit flow per hour')
df['Exit flow per hour'] = df['exit flow interval']*60
df

# # Frequency distribution of each type of vehicle travelling on the lane (both cumulative and interval wise)

st.header('Finding the frequency of small cars')
df['Small car'] = 0
for i in range(87):
    for j in range(len(df)):
        if df['Exit time'][j] <= df['Gap'][i] and df['Vehicle Type'][j]==1:
           df['Small car'][i] = df['Small car'][i]+1
#         else:
#             val = j
#             break
df

#st.header('Finding the frequency of small car')
df['Small car interval wise'] = df['Small car'].shift(0).diff()
df['Small car interval wise'][0] = 8
df.drop(['Small car'], axis=1)

#st.header('Finding the frequency of Big Car')
df['Big car'] = 0
for i in range(87):
    for j in range(len(df)):
        if df['Exit time'][j] <= df['Gap'][i] and df['Vehicle Type'][j]==2:
           df['Big car'][i] = df['Big car'][i]+1
df['Big car interval wise'] = df['Big car'].shift(0).diff()
df['Big car interval wise'][0] = 8
df.drop(['Big car'], axis=1)

#st.header('Finding the frequency of Two Wheeler')
df['Two wheeler'] = 0
for i in range(87):
    for j in range(len(df)):
        if df['Exit time'][j] <= df['Gap'][i] and df['Vehicle Type'][j]==3:
           df['Two wheeler'][i] = df['Two wheeler'][i]+1
df['Two wheeler interval wise'] = df['Two wheeler'].shift(0).diff()
df['Two wheeler interval wise'][0] = 26
df.drop(['Two wheeler'], axis=1)


df['LCV'] = 0
for i in range(87):
    for j in range(len(df)):
        if df['Exit time'][j] <= df['Gap'][i] and df['Vehicle Type'][j]==4:
           df['LCV'][i] = df['LCV'][i]+1
df['LCV interval wise'] = df['LCV'].shift(0).diff()
df['LCV interval wise'][0] = df['LCV'][0]
df.drop(['LCV'], axis=1)

st.header('Frequency of various type of vehicles interval wise')
df['Bus'] = 0
for i in range(87):
    for j in range(len(df)):
        if df['Exit time'][j] <= df['Gap'][i] and df['Vehicle Type'][j]==5:
           df['Bus'][i] = df['Bus'][i]+1
df['Bus interval wise'] = df['Bus'].shift(0).diff()
df['Bus interval wise'][0] = df['Bus'][0]
# df.drop(['LCV'], axis=1)
df

# # Finding cumulative and interval wise speed of all types of vehicles

st.header('Finding the Cummlative and interval wise speed of Small Car')
df['Cumulative Speed Small car'] = 0.000
for i in range(87):
    for j in range(len(df)):
        if df['Exit time'][j] <= df['Gap'][i] and df['Vehicle Type'][j]==1:
           df['Cumulative Speed Small car'][i] = df['Cumulative Speed Small car'][i]+df['Speed'][j]
df['Cumulative Speed Small car interval wise'] = df['Cumulative Speed Small car'].shift(0).diff()
df['Cumulative Speed Small car interval wise'][0] = df['Cumulative Speed Small car'][0]
# df.drop(['LCV'], axis=1)
df        

st.header('Cummlative and interval wise speed of Big Car')
df['Cumulative Speed Big car'] = 0.000
for i in range(87):
    for j in range(len(df)):
        if df['Exit time'][j] <= df['Gap'][i] and df['Vehicle Type'][j]==2:
           df['Cumulative Speed Big car'][i] = df['Cumulative Speed Big car'][i]+df['Speed'][j]
df['Cumulative Speed Big car interval wise'] = df['Cumulative Speed Big car'].shift(0).diff()
df['Cumulative Speed Big car interval wise'][0] = df['Cumulative Speed Big car'][0]
# df.drop(['LCV'], axis=1)
df 

st.header("Cummlative and interval Speed of two Wheelers")
df['Cumulative Speed 2 wheeler'] = 0.000
for i in range(87):
    for j in range(len(df)):
        if df['Exit time'][j] <= df['Gap'][i] and df['Vehicle Type'][j]==3:
           df['Cumulative Speed 2 wheeler'][i] = df['Cumulative Speed 2 wheeler'][i]+df['Speed'][j]
df['Cumulative Speed 2 wheeler interval wise'] = df['Cumulative Speed 2 wheeler'].shift(0).diff()
df['Cumulative Speed 2 wheeler interval wise'][0] = df['Cumulative Speed 2 wheeler'][0]
# df.drop(['LCV'], axis=1)
df

st.header('Cummlative and interval wise Speed of LCV')
df['Cumulative Speed LCV'] = 0.000
for i in range(87):
    for j in range(len(df)):
        if df['Exit time'][j] <= df['Gap'][i] and df['Vehicle Type'][j]==4:
           df['Cumulative Speed LCV'][i] = df['Cumulative Speed LCV'][i]+df['Speed'][j]
df['Cumulative Speed LCV interval wise'] = df['Cumulative Speed LCV'].shift(0).diff()
df['Cumulative Speed LCV interval wise'][0] = df['Cumulative Speed LCV'][0]
# df.drop(['LCV'], axis=1)
df

st.header("Cummlative and interval wise Speed of Bus")
df['Cumulative Speed Bus'] = 0.000
for i in range(87):
    for j in range(len(df)):
        if df['Exit time'][j] <= df['Gap'][i] and df['Vehicle Type'][j]==5:
           df['Cumulative Speed Bus'][i] = df['Cumulative Speed Bus'][i]+df['Speed'][j]
df['Cumulative Speed Bus interval wise'] = df['Cumulative Speed Bus'].shift(0).diff()
df['Cumulative Speed Bus interval wise'][0] = df['Cumulative Speed Bus'][0]
# df.drop(['LCV'], axis=1)
df

#df.columns

# # Calculating average speed of vehicle in 5 minutes interval
st.header("Average Speed of Vehicles in 5 minutes interval")
df['Avg speed small car interval wise'] = df['Cumulative Speed Small car interval wise']/df['Small car interval wise']
df['Avg speed Big car interval wise'] = df['Cumulative Speed Big car interval wise']/df['Big car interval wise']
df['Avg speed 2 wheeler interval wise'] = df['Cumulative Speed 2 wheeler interval wise']/df['Two wheeler interval wise']
df['Avg speed LCV interval wise'] = df['Cumulative Speed LCV interval wise']/df['LCV interval wise']
df['Avg speed Bus interval wise'] = df['Cumulative Speed Bus interval wise']/df['Bus interval wise']
df

df = df.fillna(0, limit=87)
#df

# # Individual PCU calculation
st.header('PCU calculation of various types of vehicles')
df['Small Car PCU'] = (df['Avg speed small car interval wise']/df['Avg speed small car interval wise'])/(5.36/5.36)
df['Big car PCU'] = (df['Avg speed small car interval wise']/df['Avg speed Big car interval wise'])/(5.36/8.11)
df['2 wheeler PCU'] = (df['Avg speed small car interval wise']/df['Avg speed 2 wheeler interval wise'])/(5.36/1.2)
df['LCV PCU'] = (df['Avg speed small car interval wise']/df['Avg speed LCV interval wise'])/(5.36/12.81)
df['Bus PCU'] = (df['Avg speed small car interval wise']/df['Avg speed Bus interval wise'])/(5.36/24.54)
df

st.header('PCU table of vehicles')
cols = ['Small Car PCU','Big car PCU','2 wheeler PCU','LCV PCU','Bus PCU']
for i in range(87):
    for j in cols:
        if df[j][i] == np.inf:
            df[j][i] = 0
df

#df.columns

# ## Final PCU calculation
st.header('Final PCU calculation')
df['Final PCU'] = df['Small Car PCU']*df['Small car interval wise'] + df['Big car PCU']*df['Big car interval wise'] + df['2 wheeler PCU']*df['Two wheeler interval wise'] + df['LCV PCU']*df['LCV interval wise'] + df['Bus PCU']*df['Bus interval wise']
df

#df.columns

# # FINAL DATAFRAME WITH ALL VALUES

st.header('Final Dataframe with all the Values')
final_df = pd.DataFrame()
final_df['PCU per 5 min'] = df['Final PCU']
final_df['Total PCU per hour'] = df['Final PCU']*12
final_df['SMS'] = df['SMS']
final_df['Density'] = final_df['Total PCU per hour']/final_df['SMS']
final_df['Flow'] = df['Exit flow per hour']
final_df
st.header('Graph between Total PCU per hour and Density')
graph_df = pd.DataFrame({"Density" : [2,5,10,20,30,50,60,70,80,90,110,130,140,142]})
#graph_df

graph_df['Derived flow'] = (-0.2858 * graph_df.Density * graph_df.Density)+40.907*graph_df.Density
#graph_df

graph_df['SMS derived'] = graph_df['Derived flow']/graph_df['Density']
#graph_df

fig, ax= plt.subplots()
# graph_df.plot.scatter(x='Density', y='Total PCU per hour', ax=ax)
st.pyplot(fig)

with st.echo(code_location='below'):
    # import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    ax.scatter(
        final_df.iloc[:87]['Density'], 
        # final_df.iloc[:87]['Density'], 
        final_df.iloc[:87]['Total PCU per hour'],
            
    )

    ax.set_xlabel("Density")
    ax.set_ylabel("Total PCU per hour")

    st.write(fig)

#fig = plt.scatter(final_df.iloc[:87]['Density'], final_df.iloc[:87]['Total PCU per hour'])
#plt.show()
#ax = fig.add_subplot(1,1,1)
#ax.scatter(
#        df["Density"],
#       df["Total PCU per hour"],
#    )
#ax.set_xlabel("Acceleration")
#ax.set_ylabel("Miles per gallon")

#st.write(fig)
#final_df['Total PCU per hour'].describe()



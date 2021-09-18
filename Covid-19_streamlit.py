#!/usr/bin/env python
# coding: utf-8

# # Covid-19 Exploratory Data Analysis

# ## Imports
# 

from re import L

import pandas as pd
import numpy as np
import folium
import plotly.express as px
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import streamlit as st
import time
import json
import requests
from datetime import date
st.title("Covid-19 Exploratory Data Analysis 🦠")  
st.subheader("This is an Exploratory Data Analysis of Covid-19 data as of 1 Sept 2021")
url="https://raw.githubusercontent.com/priyaavec/streamlit-demo-deploy/master/states_india.geojson"
st.sidebar.title("Visualization Selector")
st.sidebar.markdown("Select the Charts/Plots accordingly:")



@st.cache(allow_output_mutation=True)
def load_data(nrows):
    data = pd.read_csv("Latest Covid-19 India Status.csv")
    return data
    
df = load_data(36)    
df['State/UTs'] = df['State/UTs'].replace(['Telengana'],'Telangana')


total_cases=df["Total Cases"].sum()


st.markdown("***")
# Prediciting the deaths and plotting against the actual Deaths.
X = df['Total Cases'].to_numpy()
y = df['Deaths'].to_numpy()
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
model = LinearRegression()
model.fit(X.reshape((len(X), 1)), y)
predictions = model.predict(X.reshape((len(X), 1)))
fig = go.Figure([go.Scatter(x=df['Total Cases'], y=df['Deaths'], mode='markers', text=df['State/UTs'], name='Actual Deaths'),
                 go.Scatter(x=df['Total Cases'], y=predictions, name='Predicted Deaths')])
fig.update_layout(title='Deaths vs Total Cases', xaxis_title='Total Cases', yaxis_title='Deaths')
st.subheader("Prediction of Deaths in India 📊")
st.plotly_chart(fig)
top_states=df.loc[df['State/UTs'].isin(['Maharashtra','Kerala',"Karnataka","Tamil Nadu","Andhra Pradesh"])]
st.markdown("***")
# Plotting the Total Cases in India.
st.title("Top 5 Covid Cases contributing States 📉 ")
st.text("Select the case type from the sidebar and uncheck hide")
select = st.sidebar.selectbox('Visualization type', ['Bar plot', 'Pie chart'], key='1')
select_case=st.sidebar.selectbox("Case type",["Total Cases","Active Cases","Deaths","Discharged"])
if not st.sidebar.checkbox("Hide", True, key='2'):
     if select == 'Pie chart':
           
            if(select_case=="Total Cases"):
               pie_fig=px.pie(top_states,names=top_states["State/UTs"],values=top_states["Total Cases"])
               st.plotly_chart(pie_fig)
            elif(select_case=="Active Cases"):
                pie_fig=px.pie(top_states,names=top_states["State/UTs"],values=top_states["Active"])
                st.plotly_chart(pie_fig)
            elif(select_case=="Deaths"):
                pie_fig=px.pie(top_states,names=top_states["State/UTs"],values=top_states["Deaths"])
                st.plotly_chart(pie_fig)    
            elif(select_case=="Discharged"):
                pie_fig=px.pie(top_states,names=top_states["State/UTs"],values=top_states["Active"])
                st.plotly_chart(pie_fig)      
     if select=='Bar plot':
            if(select_case=="Total Cases"):
              bar_fig=px.bar(data_frame=top_states,x="State/UTs",y="Total Cases") 
              st.plotly_chart(bar_fig)
            elif(select_case=="Active Cases"):
                bar_fig=px.bar(data_frame=top_states,x="State/UTs",y="Active") 
                st.plotly_chart(bar_fig)
            elif(select_case=="Deaths"):
                bar_fig=px.bar(data_frame=top_states,x="State/UTs",y="Deaths") 
                st.plotly_chart(bar_fig)    
            elif(select_case=="Discharged"):
                bar_fig=px.bar(data_frame=top_states,x="State/UTs",y="Discharged") 
                st.plotly_chart(bar_fig)
st.markdown("***")
# Plotting the Active ratio of cases all over India
st.title("What is the active ratio of cases all over India? 🔬")
active_fig=px.area(x="State/UTs",y="Active Ratio (%)",data_frame=df)
st.plotly_chart(active_fig)
st.markdown("***")
# Plotting the total cases vs discharge graph of all states.
st.title("What is the trend of total cases and discharged people in all states?💊")
discharge_fig= go.Figure([go.Bar(y=df['Total Cases'], name='Total Cases', hovertext=df['State/UTs'], x=df['State/UTs']),
                 go.Bar(y=df['Discharged'], name='Discharged', hovertext=df['State/UTs'], x=df['State/UTs'])])
fig.update_layout(barmode='group')
fig.update_layout(title='Total & Discharged Cases')
st.plotly_chart(discharge_fig)
st.markdown("***")
# Plotting the discharge ratio of all states.
st.title("What is the discharge ratio in all states all over India?🩹")
discharge_ratio_fig=px.line(x="State/UTs",y="Discharge Ratio (%)",data_frame=df)
st.plotly_chart(discharge_ratio_fig)
st.markdown("***")
# India Map

st.title("Statewise representation of Covid Cases in India as of 1 Sept 2021🧬")
select_radio=st.radio(
    "Select different cases:",
    ('Total Cases', 'Active', 'Discharged',"Deaths"))
ind_map=go.Figure(data=go.Choropleth(
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locationmode='geojson-id',
    locations=df['State/UTs'],
    z=df[select_radio],


    autocolorscale=False,
    colorscale='Reds',
    marker_line_color='peachpuff',

    colorbar=dict(
        len=0.45
    )
))

ind_map.update_geos(
    visible=False,
    projection=dict(
        type='conic conformal',
        parallels=[12.472944444, 35.172805555556],
        rotation={'lat': 24, 'lon': 80}
        
    ),
    lonaxis={'range': [68, 98]},
    lataxis={'range': [6, 38]},
    
)


ind_map.update_layout(
    geo=dict(scope="asia"),
    title=dict(
       
        xanchor='center',
        x=0.5,
        yref='paper',
        yanchor='bottom',
        y=1,
      
        pad={'b': 10}
    ),
    margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
    height=550,
    width=550,
    
)

st.plotly_chart(ind_map)
st.markdown("***")
# Active,discharge and death ratio
st.title("How is the active,discharge and death ratio all over India?💉")
select_ratio=st.radio(
    "Select different ratio:",
    ('Active ratio', 'Discharge ratio', 'Death ratio'))
if(select_ratio=='Active ratio'):    
   active_ratio_fig= px.pie(names="State/UTs",values="Active Ratio (%)",data_frame=df)
   st.plotly_chart(active_ratio_fig)
elif(select_ratio=="Discharge ratio"):
   discharge_ratio_pie_fig= px.pie(names="State/UTs",values="Discharge Ratio (%)",data_frame=df)
   st.plotly_chart(discharge_ratio_pie_fig)
elif(select_ratio=="Death ratio"):
    death_ratio_fig=px.pie(names="State/UTs",values="Death Ratio (%)",data_frame=df)
    st.plotly_chart(death_ratio_fig)    
st.markdown("***")
#Footer
st.write("Made with ❤️by Vinamra Gupta")
link = '[GitHub ](https://github.com/VinamraGuptaa)' "🔧"
st.markdown(link, unsafe_allow_html=True)
link = '[Linkedin](https://www.linkedin.com/in/vinamra-gupta-6908001a8/)' "📈"
st.markdown(link, unsafe_allow_html=True)
link = '[Medium](https://medium.com/@vinamragupta98)' "📰"
st.markdown(link, unsafe_allow_html=True)
     

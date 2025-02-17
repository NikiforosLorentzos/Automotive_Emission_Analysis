import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
@st.cache_data
def load_data():
    file_path = 'stats.ods'
    car_data = pd.read_excel(file_path, sheet_name=0, engine='odf')
    co2_data = pd.read_excel(file_path, sheet_name=2, engine='odf')

    car_data['Year'] = car_data['Date'].str.extract(r'(\d{4})').astype(int)
    yearly_car_data = car_data.groupby('Year').sum(numeric_only=True).reset_index()

    combined_data = pd.merge(yearly_car_data, co2_data, on='Year')
    return combined_data

data = load_data()

# Sidebar controls
st.sidebar.header('Filter by Year')
year_range = st.sidebar.slider('Select Year Range:', int(data['Year'].min()), int(data['Year'].max()), (2014, 2024))
filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]

# Plot car registrations
st.title('Car Registrations by Fuel Type and CO₂ Emissions Dashboard')
st.subheader('Car Registrations by Fuel Type')
fig, ax = plt.subplots(figsize=(12, 6))
for column in ['Petrol', 'Diesel', 'Hybrid electric (petrol)', 'Plug-in hybrid electric (petrol)', 'Battery electric']:
    ax.plot(filtered_data['Year'], filtered_data[column], marker='o', label=column)
ax.set_xlabel('Year')
ax.set_ylabel('Number of Cars (in thousands)')
ax.legend()
st.pyplot(fig)

# Plot CO2 emissions
st.subheader('CO₂ Emissions Over Time')
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(filtered_data['Year'], filtered_data['CO2(mil.tonnes)'], color='red', marker='o', label='CO₂ Emissions')
ax.set_xlabel('Year')
ax.set_ylabel('CO₂ Emissions (mil. tonnes)')
ax.legend()
st.pyplot(fig)

st.write('This dashboard allows users to interactively explore the relationship between car registrations and CO₂ emissions in the UK over time.')

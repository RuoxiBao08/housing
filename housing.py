import pandas as pd

# Load the dataset from the uploaded Excel file
file_path = '/mnt/data/housing(1).xlsx'  # Adjust the path as needed
df = pd.read_excel(file_path)

# Check the first few rows of the dataset to understand its structure
df.head()
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np

# Load the dataset
file_path = '/mnt/data/housing(1).xlsx'  # Adjust path as needed
df = pd.read_excel(file_path)

# Add a title to the Streamlit app
st.title("Housing Data Analysis")

# Sidebar filters
st.sidebar.header("Filters")

# Filter by location
location_type = st.sidebar.multiselect(
    "Select Location Type", df['location_type'].unique(), default=df['location_type'].unique()
)

# Filter by income level
income_level = st.sidebar.radio(
    "Select Income Level", ["Low (<2.5)", "Medium (2.5 - 4.5)", "High (>4.5)"]
)

# Filter the data based on the selections
if income_level == "Low (<2.5)":
    df = df[df['income'] < 2.5]
elif income_level == "Medium (2.5 - 4.5)":
    df = df[(df['income'] >= 2.5) & (df['income'] < 4.5)]
else:
    df = df[df['income'] >= 4.5]

df = df[df['location_type'].isin(location_type)]

# Price Slider
price_slider = st.slider("Select House Price Range", min_value=int(df['house_value'].min()), max_value=int(df['house_value'].max()))
filtered_data = df[df['house_value'] <= price_slider]

# Display filtered data
st.write(filtered_data)

# Display Map
st.subheader("Map of Housing Locations")
map_data = gpd.GeoDataFrame(filtered_data, geometry=gpd.points_from_xy(filtered_data['longitude'], filtered_data['latitude']))
st.map(map_data)

# Display Histogram
st.subheader("Histogram of Median House Values")
plt.figure(figsize=(10, 6))
plt.hist(filtered_data['house_value'], bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Median House Value')
plt.ylabel('Frequency')
plt.title('Histogram of Median House Value')
st.pyplot(plt)
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from opencage.geocoder import OpenCageGeocode
import time

# Configuration
file_path = '<FILENAME.CSV>'
api_key = '<OPENCAGE API KEY>'

# Load the data
data = pd.read_csv(file_path, delimiter=';')

# Ensure critical columns have no missing values
if data[['Name', 'Country', 'City', 'Address']].isnull().any().any():
    print("Error: Missing values found in the CSV data.")
else:
    print("No missing values found in critical columns.")

# Geocoding function to get coordinates with caching
coordinates_cache = {}

def get_coordinates(geocoder, country, city, address):
    query = f"{address}, {city}, {country}"
    if query in coordinates_cache:
        return coordinates_cache[query]
    
    try:
        results = geocoder.geocode(query)
        if results and len(results):
            coordinates = (results[0]['geometry']['lat'], results[0]['geometry']['lng'])
            coordinates_cache[query] = coordinates
            return coordinates
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)
        return get_coordinates(geocoder, country, city, address)
    
    coordinates_cache[query] = (np.nan, np.nan)
    return (np.nan, np.nan)

# Initialize geocoder with API key
geocoder = OpenCageGeocode(api_key)

# Apply geocoding to get coordinates
data['Coordinates'] = data.apply(lambda row: get_coordinates(geocoder, row['Country'], row['City'], row['Address']), axis=1)

# Separate latitude and longitude into new columns
data['Latitude'] = data['Coordinates'].apply(lambda x: x[0] if pd.notnull(x) else np.nan)
data['Longitude'] = data['Coordinates'].apply(lambda x: x[1] if pd.notnull(x) else np.nan)

# Apply some jitter to the coordinates
jitter_strength = 0.2  # When you have many stacked, increased this value to add more spacing
data['Latitude'] += np.random.uniform(-jitter_strength, jitter_strength, size=data.shape[0])
data['Longitude'] += np.random.uniform(-jitter_strength, jitter_strength, size=data.shape[0])

# Calculate counts for the table
country_counts = data.groupby('Country').agg(
    total=pd.NamedAgg(column='Name', aggfunc='count')
).reset_index()

# Sort the table by total count in descending order
country_counts = country_counts.sort_values(by='total', ascending=False)

# Create the map
fig_map = px.scatter_geo(
    data,
    lat='Latitude',
    lon='Longitude',
    color='Country',  # Different colors for each country
    hover_name='Name',
    hover_data={
        'Country': True,
        'City': True,
        'Address': True,
    },
    title='Locations Distribution by Country',
    projection='natural earth'
)

# Increase the size of the plotted dots here
fig_map.update_traces(marker=dict(size=8, line=dict(width=0.5, color='black')))

fig_map.update_geos(
    showcountries=True,
    countrycolor='Black',
    showsubunits=True,
    subunitcolor='Blue'
)

# Create the table for country statistics
table_country_counts = go.Figure(data=[go.Table(
    columnwidth=[0.15, 0.20],  # Adjust column widths here
    header=dict(
        values=["Country", "Count Locations"],
        font=dict(color='black', size=10),  # Set header font size, color below
        fill_color='lightgrey',
        align='left'
    ),
    cells=dict(
        values=[country_counts['Country'], country_counts['total']],
        font=dict(color='black', size=10),  # Set cells font size
        fill_color='rgba(255, 255, 255, 0.7)',
        align='left',
        height=20  # Set the height of the cells
    )
)])

# Put the stuff on the screen and position the table on the map
fig_map.add_trace(
    go.Table(
        columnwidth=[0.15, 0.25],  # Adjust column widths
        header=dict(
            values=["Country", "Count Locations"],
            font=dict(color='black', size=10),  # Set header font size
            fill_color='lightgrey',
            align='left'
        ),
        cells=dict(
            values=[country_counts['Country'], country_counts['total']],
            font=dict(color='black', size=10),  # Set cells font size
            fill_color='rgba(255, 255, 255, 0.7)',
            align='left',
            height=20  # Set the height of the cells
        ),
        domain=dict(x=[0, 0.2], y=[0, 1])  # Adjust the position and size of the table to full page height
    )
)

fig_map.update_layout(
    showlegend=False,
    title_text="Location Data Map" # Title of the page
)

fig_map.show()

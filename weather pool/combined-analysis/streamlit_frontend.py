import streamlit as st
import requests
import pandas as pd

st.title('🌍 Global Weather App with Nepal Cities')

# Fetch list of available cities from backend
try:
    response = requests.get('http://localhost:5000/cities')
    all_cities = response.json().get('cities', [])
    nepal_cities = [city for city in all_cities if city in [
        'Kathmandu', 'Pokhara', 'Lalitpur', 'Bharatpur', 'Biratnagar',
        'Birgunj', 'Dharan', 'Butwal', 'Hetauda', 'Nepalgunj',
        'Bhaktapur', 'Janakpur', 'Dhangadhi', 'Itahari', 'Tulsipur'
    ]]
except:
    all_cities = []
    nepal_cities = []

# Create tabs
tab1, tab2 = st.tabs(["Weather Lookup", "Nepal Weather"])

with tab1:
    st.subheader("Search Any City Worldwide")
    
    if all_cities:
        city = st.selectbox('Select or type a city:', all_cities)
    else:
        city = st.text_input('Enter a city name:', 'Kathmandu')

    if st.button('Get Weather'):
        try:
            response = requests.get(f'http://localhost:5000/weather/{city}')
            weather = response.json()
            
            st.subheader(f"Current Weather in {city}:")
            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature", f"{weather['temperature']}°F")
            col2.metric("Condition", weather['condition'])
            col3.metric("Humidity", f"{weather['humidity']}%")
            
            if 'note' in weather:
                st.info(weather['note'])
                
        except Exception as e:
            st.error(f"Error fetching weather data: {e}")

with tab2:
    st.subheader("Nepal Cities Weather Overview")
    
    if not nepal_cities:
        st.warning("Couldn't fetch Nepal cities data")
    else:
        # Display weather for all Nepal cities in a table
        weather_data = []
        for city in nepal_cities:
            try:
                response = requests.get(f'http://localhost:5000/weather/{city}')
                data = response.json()
                weather_data.append({
                    'City': city,
                    'Temperature (°F)': data['temperature'],
                    'Condition': data['condition'],
                    'Humidity (%)': data['humidity']
                })
            except:
                pass
        
        if weather_data:
            df = pd.DataFrame(weather_data)
            st.dataframe(df.style.highlight_max(axis=0, color='#90EE90'), use_container_width=True)
            
            # Show on map
            try:
                # Coordinates for Nepal cities (simplified)
                city_coords = {
                    'Kathmandu': (27.7172, 85.3240),
                    'Pokhara': (28.2096, 83.9856),
                    # Add coordinates for other Nepal cities...
                }
                
                map_data = pd.DataFrame([
                    {'lat': city_coords[row['City']][0], 'lon': city_coords[row['City']][1], 
                     'city': row['City'], 'temp': row['Temperature (°F)']}
                    for _, row in df.iterrows() if row['City'] in city_coords
                ])
                
                st.map(map_data, zoom=6,
                      use_container_width=True,
                      size='temp',
                      color='#0068c9')
            except:
                st.warning("Couldn't display map")
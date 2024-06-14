# csv-to-map
Simple python script that aims to geocode location data from a CSV file and visualize the results on a geographical map using Plotly. The map displays locations by country and includes a table with counts of locations per country.

  Features
	
    Geocoding: Convert addresses to geographical coordinates using the OpenCage Geocode API.
	A function get_coordinates is defined to fetch the geographical coordinates for each address. The function uses a cache to avoid redundant API calls.
    Data Visualization: Display locations on a world map with jitter to prevent overlap.
    Country Statistics: Show a table of the number of locations per country on the map.
    
  Requirements
	
    Python 3.x
    Pandas
    Plotly
    OpenCage Geocode
    -> pip install pandas plotly opencage

  Howto:
	
	Place your CSV file in the project directory. Ensure it has the columns Name, Country, City, and Address.
  	Update the file_path and api_key variables in the script with your CSV file name and OpenCage API key, respectively.
    file_path = 'yourfile.csv'
    api_key = 'your-opencage-api-key'
  
  Example CSV file:
	
    Name,Country,City,Address
    Location1,USA,New York,123 Main St
    Location2,Canada,Toronto,456 Queen St



  

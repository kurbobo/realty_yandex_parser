# import pandas as pd
import matplotlib.pyplot as plt
# import geopandas as gpd
import math
from geopy.geocoders import Nominatim
nom = Nominatim()
n = nom.geocode('Санкт-Петербург Орбели 27к6')
print(n.latitude, n.longitude)
# n = nom.geocode('Россия, Санкт-Петербург, ул Орбели, 27 к6')
# print(n.latitude, n.longitude)
# n = nom.geocode('Россия, Санкт-Петербург,улица Орбели, 27 к6')
# print(n.latitude, n.longitude)
# n = nom.geocode('Санкт-Петербург,улица Орбели, 27 к6')
# print(n.latitude, n.longitude)
# n = nom.geocode('СПб,улица Орбели, 27 к6')
# print(n.latitude, n.longitude)
# n = nom.geocode('Орбели, 27 к6')
# print(n.latitude, n.longitude)

import folium
from folium.plugins import MarkerCluster
import pandas as pd

map = folium.Map(location=[59.91665, 30.30645], zoom_start = 15, min_zoom=8, max_zoom=25)

# with open('cian.txt', 'a', encoding='utf-8') as output_file:
map.save("map1.html")